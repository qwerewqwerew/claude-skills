#!/usr/bin/env python3
"""fig_decode.mjs가 뽑은 JSON에서 디자인 토큰을 집계하고 테마 파일을 만든다.

    python fig_tokens.py message.json                      # 토큰만 출력
    python fig_tokens.py message.json -o tokens.json       # 토큰 저장
    python fig_tokens.py message.json --theme my-brand     # 테마 md까지 생성

## 추출 순서 — 이름이 있으면 이름을 믿는다

소스가 디자인 시스템 파일이면 토큰이 이름표와 함께 정리돼 있다. 그 경우 추정하지
않고 이름-값 쌍을 그대로 쓴다. 없을 때만 사용 빈도 기반으로 추정한다.

  1순위  이름표 있는 스와치: `color/bg/brand`, `gray/500` 같은 라벨 + 색 견본이
         한 셀에 들어 있는 프레임(Semantic/Row, Primitives/Row 등)
  2순위  Figma 변수(VARIABLE)의 색상값
  3순위  사용 빈도 추정 — 채도x명도x빈도가 가장 높은 색을 Primary로 보는 식

타이포도 같다. `Type/Display/Hero`, `Type/Body/Default` 처럼 이름 붙은 견본
프레임이 있으면 거기서 두께·자간·행간을 읽고, 없으면 최빈값을 쓴다.

## 고정 규칙

- 한글 폰트는 항상 "Noto Sans KR". 소스가 다른 폰트를 써도 바꾸지 않는다.
- 두께·자간·행간은 소스를 따른다. 단 **행간은 1.4를 하한**으로 올린다
  (웹 기준 행간을 슬라이드에 그대로 쓰면 좁아서 읽기 어렵다).
- 글자 크기는 소스가 아니라 슬라이드 스케일(골격 테마)을 쓴다. 소스가 웹이면
  본문 17px 같은 값이 1280x720 화면에서 너무 작다.
"""
import argparse
import collections
import colorsys
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 골격 테마는 stitch-ppt 스킬이 정본으로 갖고 있다(사본을 두면 두 벌이 갈라진다).
# 같은 플러그인 안의 형제 스킬이라 로컬 개발본이든 설치된 플러그인이든 이 상대
# 위치가 같다.
BASE_THEME_DIR = ROOT.parent / "stitch-ppt" / "references" / "themes"
BASE_THEME = BASE_THEME_DIR / "kiwik-card.md"

# 생성한 테마를 쓰는 곳. 플러그인은 버전별 디렉터리에 설치되므로 스킬 폴더 안에
# 쓰면 업데이트할 때 사용자가 만든 테마가 함께 지워진다. 버전과 무관한 사용자
# 폴더에 쓰고, PPT_THEME_DIR 로 바꿀 수 있게 둔다.
THEME_OUT_DIR = pathlib.Path(
    os.environ.get("PPT_THEME_DIR") or pathlib.Path.home() / ".claude" / "ppt-themes"
)

LINE_HEIGHT_MIN = 1.4          # 행간 하한
SEMANTIC_HINT = re.compile(r"^(color|bg|text|border|accent|brand)[/\-]", re.I)

# 골격(kiwik)에서 각 역할이 쓰는 HEX. 치환 기준점이다.
# 골격 파일이 각 슬롯에 실제로 쓰는 HEX. 치환은 이 값을 찾아 바꾸는 방식이라
# 골격에 없는 값은 조용히 무동작이 된다. 골격을 바꿀 때는 이 표도 함께 맞춘다.
# (build_theme이 시작할 때 빠진 슬롯을 경고로 알린다.)
BASE_SLOTS = {
    "Primary":     "#2C846A",
    "PrimaryLite": "#2D9F7A",
    "Contrast":    "#0E3327",
    "TextBody":    "#737373",
    # kiwik-card 골격에는 없다. 이 디자인은 카드 배경이 슬라이드 배경과 같은 흰색이고
    # 1px 테두리로만 구분하므로 별도 surface 색이 존재하지 않는다. 무동작이 정상이다.
    "Surface":     "#FAFAFA",
    "Background":  "#FFFFFF",
}

# 시맨틱 토큰 이름 → 스킬 슬롯. 앞에 있는 후보가 우선한다.
SEMANTIC_MAP = {
    "Primary":    ["color/bg/brand", "color/text/brand", "color/border/brand", "brand"],
    "Background": ["color/bg/base", "color/bg/subtle", "bg/base"],
    "Surface":    ["color/bg/surface", "color/bg/subtle", "bg/surface"],
    "TextStrong": ["color/text/primary", "text/primary"],
    "TextBody":   ["color/text/secondary", "color/text/muted", "text/secondary"],
    "OnPrimary":  ["color/text/on-brand", "color/text/inverse"],
    "PrimaryLite": ["color/bg/brand-tint", "blue/300"],
}


def hexof(c):
    return "#%02X%02X%02X" % tuple(
        max(0, min(255, round(float(c.get(k, 0)) * 255))) for k in "rgb"
    )


def base_latin_font(text, default="Noto Sans"):
    """골격 파일이 쓰는 라틴 폰트 이름을 읽는다.

    두 골격 모두 2절에 `- 라틴: <폰트> / 한글: ...` 줄을 갖고 있다. 이 줄이 기준이다.
    못 찾으면 예전 가정("Noto Sans")으로 되돌아가 기존 동작을 유지한다.
    """
    m = re.search(r"^-\s*라틴:\s*(.+?)\s*/", text, re.M)
    return m.group(1).strip() if m else default


def latin_re(font):
    """라틴 폰트 이름만 골라내는 정규식.

    `Noto Sans`는 한글 폰트 `Noto Sans KR`의 앞부분이기도 하다. 그냥 바꾸면
    `Roboto KR` 같은 없는 폰트가 만들어지므로 **뒤에 KR이 붙는 경우는 제외한다.**
    앞뒤 단어 경계를 둬서 `Inter`가 `Internal` 같은 낱말에 걸리지 않게 한다.
    """
    return re.compile(r"\b" + re.escape(font) + r"\b(?!\s*KR)")


def lh_ratio(lh, size):
    """행간을 배수로 환산한다. 못 하면 None.

    PIXELS  → value / fontSize
    PERCENT → value / 100
    RAW     → value 그대로 배수로 본다. 실제 파일(fig-kiwi v106)에서 RAW 값은
              1.2~1.5뿐이었고 해당 fontSize는 13~64px였다. px로도 %로도 성립하지
              않으므로 배수로 읽는 것이 유일하게 말이 된다. 이 단위를 버리면
              소스 행간이 실제보다 좁게 보고된다(v106 파일에서 22건이 버려졌다).
    """
    if not isinstance(lh, dict):
        return None
    units, val = lh.get("units"), lh.get("value")
    if val is None:
        return None
    try:
        val = float(val)
    except (TypeError, ValueError):
        return None
    if units == "PIXELS" and size:
        return val / float(size)
    if units == "PERCENT":
        return val / 100
    if units == "RAW":
        return val
    return None


def luma(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def vivid(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    _, s, v = colorsys.rgb_to_hsv(r, g, b)
    return s * v


class Doc:
    """노드 트리 탐색 도우미."""

    def __init__(self, nodes):
        self.nodes = nodes
        self.children = collections.defaultdict(list)
        for n in nodes:
            self.children[self._gk((n.get("parentIndex") or {}).get("guid"))].append(n)

    @staticmethod
    def _gk(g):
        return (g.get("sessionID"), g.get("localID")) if g else None

    def kids(self, n):
        return self.children[self._gk(n.get("guid"))]

    def descend(self, n, depth=0):
        for k in self.kids(n):
            yield k, depth
            yield from self.descend(k, depth + 1)

    @staticmethod
    def text(n):
        return ((n.get("textData") or {}).get("characters") or "").strip()

    @staticmethod
    def solid(n):
        for p in (n.get("fillPaints") or []):
            if p.get("type") == "SOLID" and p.get("visible", True):
                return hexof(p.get("color") or {})
        return None


def named_swatches(doc):
    """라벨 + 색 견본이 한 셀에 있는 구조에서 이름-색 쌍을 모은다."""
    found = {}
    for n in doc.nodes:
        if n.get("type") != "FRAME":
            continue
        for cell in doc.kids(n):
            label = swatch = None
            for c in doc.kids(cell):
                t = doc.text(c)
                if c.get("type") == "TEXT" and t and label is None:
                    label = t
                elif c.get("type") != "TEXT" and swatch is None:
                    swatch = doc.solid(c)
            if swatch is None:
                swatch = doc.solid(cell)
            if label and swatch and ("/" in label or SEMANTIC_HINT.match(label)):
                found.setdefault(label.strip(), swatch)
    return found


def variable_colors(doc):
    out = {}
    for n in doc.nodes:
        if n.get("type") != "VARIABLE":
            continue
        for e in (n.get("variableDataValues") or {}).get("entries", []):
            v = ((e.get("variableData") or {}).get("value") or {}).get("colorValue")
            if v:
                out.setdefault(n.get("name"), hexof(v))
    return out


def type_scale(doc):
    """`Type/...` 이름의 견본 프레임에서 두께·자간·행간을 읽는다."""
    scale = {}
    for n in doc.nodes:
        name = n.get("name") or ""
        if n.get("type") != "FRAME" or not name.startswith("Type/"):
            continue
        texts = [k for k, _ in doc.descend(n) if k.get("type") == "TEXT" and k.get("fontSize")]
        if not texts:
            continue
        big = max(texts, key=lambda k: k["fontSize"])
        fn = big.get("fontName") or {}
        ls = big.get("letterSpacing") or {}
        lh = big.get("lineHeight") or {}
        size = float(big["fontSize"])
        ratio = lh_ratio(lh, size) or 0.0
        scale[name] = {
            "family": fn.get("family"),
            "style": fn.get("style") or "Regular",
            "size": size,
            "letter_value": float(ls.get("value") or 0),
            "letter_units": ls.get("units") or "PERCENT",
            "line_ratio": round(ratio, 3) if ratio else None,
        }
    return scale


def radius_labels(doc):
    """`sm · 4px` 같은 라벨에서 라운드 값을 뽑는다."""
    out = {}
    for n in doc.nodes:
        if not str(n.get("name") or "").startswith("Radius"):
            continue
        for k, _ in doc.descend(n):
            t = doc.text(k)
            m = re.match(r"([\w-]+)\s*[·:\-]\s*(\d+(?:\.\d+)?)px", t)
            if m:
                out[m.group(1)] = float(m.group(2))
    return out


def usage_stats(doc):
    st = {
        "text_colors": collections.Counter(),
        "fill_colors": collections.Counter(),
        "fonts": collections.Counter(),
        "sizes": collections.Counter(),
        "letter": collections.Counter(),
        "line_px": [],
        "radius": collections.Counter(),
        "image_fills": 0,
    }
    for n in doc.nodes:
        t = n.get("type")
        for p in (n.get("fillPaints") or []):
            if not p.get("visible", True):
                continue
            if p.get("type") == "SOLID":
                h = hexof(p.get("color") or {})
                (st["text_colors"] if t == "TEXT" else st["fill_colors"])[h] += 1
            elif p.get("type") == "IMAGE":
                st["image_fills"] += 1
        if t == "TEXT":
            fn = n.get("fontName") or {}
            if fn.get("family"):
                st["fonts"][(fn["family"], fn.get("style") or "Regular")] += 1
            if n.get("fontSize"):
                st["sizes"][round(float(n["fontSize"]), 1)] += 1
            ls = n.get("letterSpacing") or {}
            if ls.get("units"):
                st["letter"][(round(float(ls.get("value") or 0), 2), ls["units"])] += 1
            r = lh_ratio(n.get("lineHeight") or {}, float(n.get("fontSize") or 0))
            if r:
                st["line_px"].append(r)
        for k in ("cornerRadius", "rectangleTopLeftCornerRadius"):
            if n.get(k):
                st["radius"][round(float(n[k]), 1)] += 1
    return st


def pick_colors(swatches, variables, st):
    """1순위 이름표 → 2순위 변수 → 3순위 빈도 추정."""
    pool = {**variables, **swatches}          # 스와치가 변수보다 우선
    lower = {k.lower(): v for k, v in pool.items()}
    src = {}
    roles = {}

    for role, candidates in SEMANTIC_MAP.items():
        for cand in candidates:
            if cand.lower() in lower:
                roles[role] = lower[cand.lower()]
                src[role] = f"이름표 {cand}"
                break

    fills, texts = st["fill_colors"], st["text_colors"]
    allc = fills + texts

    if "Primary" not in roles and allc:
        roles["Primary"] = max(allc, key=lambda h: vivid(h) * (1 + allc[h] ** 0.5))
        src["Primary"] = "빈도 추정"
    if "Background" not in roles:
        bright = [h for h in fills if luma(h) > 0.85]
        roles["Background"] = max(bright, key=lambda h: fills[h]) if bright else "#FFFFFF"
        src["Background"] = "빈도 추정"
    if "Surface" not in roles:
        pool2 = [h for h in fills if h != roles["Background"] and luma(h) > 0.8]
        roles["Surface"] = max(pool2, key=lambda h: fills[h]) if pool2 else roles["Background"]
        src["Surface"] = "빈도 추정"
    if "TextStrong" not in roles:
        roles["TextStrong"] = min(texts, key=luma) if texts else "#111111"
        src["TextStrong"] = "빈도 추정"
    if "TextBody" not in roles:
        rest = [h for h, _ in texts.most_common() if h != roles["TextStrong"]]
        roles["TextBody"] = rest[0] if rest else roles["TextStrong"]
        src["TextBody"] = "빈도 추정"
    if "PrimaryLite" not in roles:
        r, g, b = (int(roles["Primary"][i:i + 2], 16) / 255 for i in (1, 3, 5))
        h_, s_, v_ = colorsys.rgb_to_hsv(r, g, b)
        rr, gg, bb = colorsys.hsv_to_rgb(h_, max(0.0, s_ * 0.82), min(1.0, v_ * 1.12))
        roles["PrimaryLite"] = "#%02X%02X%02X" % (round(rr * 255), round(gg * 255), round(bb * 255))
        src["PrimaryLite"] = "Primary에서 계산"

    # Contrast: 다크 표지 배경. 이름표에 없으면 가장 어두운 색을 쓴다.
    dark_named = [v for k, v in pool.items() if luma(v) < 0.12]
    if dark_named:
        roles["Contrast"] = min(dark_named, key=luma)
        src["Contrast"] = "이름표 중 최암색"
    else:
        dark_fills = [h for h in fills if luma(h) < 0.3]
        roles["Contrast"] = (max(dark_fills, key=lambda h: fills[h]) if dark_fills
                             else min(allc, key=luma) if allc else "#111111")
        src["Contrast"] = "빈도 추정"

    # TextStrong과 Contrast가 같으면 표지 글자가 배경에 묻힌다. 더 어두운 쪽을 배경으로 민다.
    if roles.get("Contrast") == roles.get("TextStrong"):
        alt = sorted({v for v in pool.values() if luma(v) < 0.2}, key=luma)
        if alt and alt[0] != roles["TextStrong"]:
            roles["Contrast"] = alt[0]
            src["Contrast"] = "TextStrong과 중복되어 대체"
        else:
            r, g, b = (int(roles["TextStrong"][i:i + 2], 16) for i in (1, 3, 5))
            roles["Contrast"] = "#%02X%02X%02X" % (max(0, r - 12), max(0, g - 12), max(0, b - 8))
            src["Contrast"] = "TextStrong과 중복되어 어둡게 보정"

    return roles, src


def pick_type(scale, st):
    fams = collections.Counter()
    for (fam, style), c in st["fonts"].items():
        fams[fam] += c
    latin = next((f for f, _ in fams.most_common() if "Noto Sans KR" not in f), "Inter")

    def by(*keys):
        for k in keys:
            for name, v in scale.items():
                if name.lower().endswith(k):
                    return v
        return None

    heading = by("display/hero", "heading/h1")
    body = by("body/default", "body/small")

    if heading:
        heading_style = heading["style"]
        head_letter = (heading["letter_value"], heading["letter_units"])
        head_line = heading["line_ratio"]
    else:
        weights = collections.Counter()
        for (fam, style), c in st["fonts"].items():
            weights[style] += c
        heading_style = next((s for s, _ in weights.most_common()
                              if any(k in s for k in ("Bold", "Semi", "Black"))), "Bold")
        head_letter = st["letter"].most_common(1)[0][0] if st["letter"] else (0, "PERCENT")
        head_line = None

    if body:
        body_style = body["style"]
        body_letter = (body["letter_value"], body["letter_units"])
        body_line = body["line_ratio"]
    else:
        body_style = "Regular"
        body_letter = head_letter
        body_line = None

    if body_line is None:
        body_line = (sum(st["line_px"]) / len(st["line_px"])) if st["line_px"] else 1.5
    if head_line is None:
        head_line = body_line

    return {
        "korean_font": "Noto Sans KR",
        "latin_font": latin,
        "heading_style": heading_style,
        "body_style": body_style,
        "heading_letter": head_letter,
        "body_letter": body_letter,
        "heading_line_src": round(head_line, 2),
        "body_line_src": round(body_line, 2),
        "heading_line": round(max(head_line, LINE_HEIGHT_MIN), 2),
        "body_line": round(max(body_line, LINE_HEIGHT_MIN), 2),
        "scale_named": scale,
    }


def color_word(h):
    """HEX → 영어 색 이름. 프롬프트 본문의 색 단어를 바꾸는 데 쓴다."""
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hue, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.15:
        return "black" if v < 0.25 else ("white" if v > 0.9 else "gray")
    deg = hue * 360
    for hi, name in ((15, "red"), (45, "orange"), (70, "yellow"), (160, "green"),
                     (200, "teal"), (255, "blue"), (290, "violet"), (345, "pink")):
        if deg < hi:
            return name
    return "red"


def letter_css(v_u):
    v, u = v_u
    if u == "PERCENT":
        return "0" if abs(v) < 1e-9 else f"{v/100:+.3f}em"
    return "0" if abs(v) < 1e-9 else f"{v:+g}px"


def build_theme(tokens, theme_id, src_name):
    if not BASE_THEME.exists():
        sys.exit(f"골격 파일이 없습니다: {BASE_THEME}")
    text = BASE_THEME.read_text(encoding="utf-8")

    # 골격에 없는 슬롯 색은 치환이 무동작으로 지나간다. 조용히 넘어가면 생성된 테마에
    # 옛 색이 남아도 알아채지 못하므로 미리 알린다.
    missing = [f"{s}({h})" for s, h in BASE_SLOTS.items() if h not in text]
    if missing:
        print(f"알림: 골격 {BASE_THEME.name}에 없는 슬롯 색 — {', '.join(missing)}."
              f" 해당 슬롯은 치환되지 않는다.", file=sys.stderr)
    c, ty = tokens["colors"], tokens["typography"]

    mapping = {
        BASE_SLOTS["Primary"]:     c["Primary"],
        BASE_SLOTS["PrimaryLite"]: c["PrimaryLite"],
        BASE_SLOTS["Contrast"]:    c["Contrast"],
        BASE_SLOTS["TextBody"]:    c["TextBody"],
        BASE_SLOTS["Surface"]:     c["Surface"],
        BASE_SLOTS["Background"]:  c["Background"],
    }
    text = re.sub(r"#[0-9A-Fa-f]{6}",
                  lambda m: mapping.get(m.group(0).upper(), m.group(0)), text)

    # HEX만 바꾸면 프롬프트에 "green #3F63F4"처럼 모순된 지시가 남는다.
    # 골격이 쓰는 색 단어도 새 색 이름으로 함께 바꾼다.
    word = color_word(c["Primary"])
    if word != "green":
        text = re.sub(r"\bgreen\b", word, text)
        text = re.sub(r"\bGreen\b", word.capitalize(), text)
        text = text.replace("그린", {"blue": "파랑", "green": "초록", "red": "빨강",
                                     "teal": "청록", "violet": "보라", "pink": "핑크",
                                     "yellow": "노랑", "gray": "회색", "black": "검정",
                                     "white": "흰색"}.get(word, word))
    dark_word = color_word(c["Contrast"])
    if dark_word in ("black", "gray"):
        text = text.replace("dark charcoal", f"near-{dark_word}")
    # 골격이 쓰는 라틴 폰트를 파일에서 읽어 갈아 끼운다.
    # 예전에는 골격이 "Noto Sans"라고 가정하고 리터럴 4개를 바꿨는데, 다른 폰트로 쓴
    # 골격(예: Inter)을 넣으면 넷 다 맞지 않아 머리말만 새 폰트가 되고 본문은 옛 폰트로
    # 남는 모순된 테마가 나왔다. 이제 골격의 폰트를 읽어 그것만 바꾼다.
    base_latin = base_latin_font(text)
    latin = ty["latin_font"]
    if latin != base_latin:
        text = latin_re(base_latin).sub(latin, text)

    # 골격 표기는 콜론이 없다(`line-height 1.5`). 콜론 유무를 모두 받아 준다.
    head_ls = letter_css(ty["heading_letter"])
    text = re.sub(r"letter-spacing(:?)\s*-?[\d.]+(?:em|px)",
                  lambda m: f"letter-spacing{m.group(1)} {head_ls}", text)
    text = re.sub(r"line-height(:?)\s*[\d.]+",
                  lambda m: f"line-height{m.group(1)} {ty['body_line']}", text)

    # 한국어 2절 서술도 소스 값으로 맞춘다.
    text = re.sub(r"본문 16px\(행간 [\d.]+\)", f"본문 16px(행간 {ty['body_line']})", text)
    text = re.sub(r"제목 자간 [^,]+, 본문은 양쪽 정렬\(justify\)",
                  f"제목 자간 {head_ls}, 본문 자간 {letter_css(ty['body_letter'])}"
                  f" (행간 제목 {ty['heading_line']} / 본문 {ty['body_line']})", text)
    text = re.sub(r"- 제목·강조: Noto Sans KR Bold",
                  f"- 제목·강조: Noto Sans KR {ty['heading_style']}", text)
    text = re.sub(r"- 본문: Noto Sans KR Regular",
                  f"- 본문: Noto Sans KR {ty['body_style']}", text)

    if tokens["radius"]:
        r = tokens["radius"]
        text = re.sub(r"(rounded|radius) 16px", lambda m: f"{m.group(1)} {r:g}px", text)

    named = tokens["named_colors"]
    extra = ""
    if named:
        rows = "\n".join(f"| `{k}` | {v} |" for k, v in list(named.items())[:24])
        extra = ("\n### 소스에서 가져온 이름 있는 토큰\n\n"
                 "필요하면 아래 값에서 골라 위 표를 고친다.\n\n"
                 "| 토큰 이름 | 값 |\n|---|---|\n" + rows + "\n")

    head = f"""# 디자인: {theme_id} — {src_name} 추출본

`scripts/fig_decode.mjs` + `scripts/fig_tokens.py`가 Figma 소스에서 뽑아 만든 파일이다.
색·폰트 두께·자간·행간·라운드는 소스 값이고, 슬라이드 레이아웃(원형 9종)은
`{BASE_THEME.name}` 골격을 따른다. 소스에 슬라이드 프레임이 없어도 템플릿이
완성되도록 하기 위해서다.

- **출처**: {src_name} (Figma 로컬 사본)
- **한글 폰트**: {ty['korean_font']} 고정 / 라틴 {ty['latin_font']}
- **행간**: 소스 {ty['body_line_src']} → 적용 {ty['body_line']} (하한 {LINE_HEIGHT_MIN})
- **권장 흐름**: slide-prompts.md 기본형
{extra}"""
    text = re.sub(r"\A# 디자인: kiwik.*?(?=## 1\. 색상 토큰)", head + "\n", text, flags=re.S)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("message_json")
    ap.add_argument("-o", "--output")
    ap.add_argument("--theme")
    args = ap.parse_args()

    raw = json.loads(pathlib.Path(args.message_json).read_text(encoding="utf-8"))
    nodes = raw.get("message", {}).get("nodeChanges") or raw.get("nodeChanges") or []
    if not nodes:
        sys.exit("nodeChanges가 비어 있습니다.")

    doc = Doc(nodes)
    swatches = named_swatches(doc)
    variables = variable_colors(doc)
    scale = type_scale(doc)
    radii = radius_labels(doc)
    st = usage_stats(doc)

    colors, sources = pick_colors(swatches, variables, st)
    typo = pick_type(scale, st)
    radius = (radii.get("md") or radii.get("lg")
              or (st["radius"].most_common(1)[0][0] if st["radius"] else None))

    pages = [n.get("name") for n in nodes if n.get("type") == "CANVAS"]
    tokens = {
        "source": raw.get("meta", {}).get("file_name") or pathlib.Path(args.message_json).stem,
        "pages": pages,
        "colors": colors,
        "color_sources": sources,
        "named_colors": {**variables, **swatches},
        "typography": typo,
        "radius": radius,
        "radius_scale": radii,
        "images": {"image_fills": st["image_fills"],
                   "packed_images": len(raw.get("images") or [])},
    }

    print(f"소스: {tokens['source']}  |  페이지 {len(pages)}개")
    print(f"이름 있는 토큰: 스와치 {len(swatches)} + 변수 {len(variables)}")
    print("\n=== 색상 역할 ===")
    for k, v in colors.items():
        print(f"  {k:12} {v}   ({sources.get(k, '-')})")
    print("\n=== 타이포 ===")
    print(f"  한글 {typo['korean_font']} / 라틴 {typo['latin_font']}")
    print(f"  제목 {typo['heading_style']} 자간 {letter_css(typo['heading_letter'])} 행간 {typo['heading_line']}")
    print(f"  본문 {typo['body_style']} 자간 {letter_css(typo['body_letter'])} "
          f"행간 {typo['body_line']} (소스 {typo['body_line_src']})")
    if scale:
        print("  이름 있는 타입 스케일:")
        for n, v in scale.items():
            print(f"    {n:24} {v['style']:11} {v['size']:g}px  행간 {v['line_ratio']}")
    print(f"\n라운드 {radius}px {radius_fmt(radii)}")
    print(f"이미지 채움 {st['image_fills']}곳 / 내장 {tokens['images']['packed_images']}개")

    if args.output:
        pathlib.Path(args.output).write_text(
            json.dumps(tokens, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n토큰 저장: {args.output}")
    if args.theme:
        THEME_OUT_DIR.mkdir(parents=True, exist_ok=True)
        dst = THEME_OUT_DIR / f"{args.theme}.md"
        dst.write_text(build_theme(tokens, args.theme, tokens["source"]), encoding="utf-8")
        print(f"테마 생성: {dst}")


def radius_fmt(radii):
    return f"(스케일 {', '.join(f'{k}={v:g}' for k, v in radii.items())})" if radii else ""


if __name__ == "__main__":
    main()
