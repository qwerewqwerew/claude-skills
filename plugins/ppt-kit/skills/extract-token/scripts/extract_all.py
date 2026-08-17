#!/usr/bin/env python3
"""fig_decode.mjs가 뽑은 노드 트리에서 A~N 전량을 집계해 tokens.raw.json을 만든다.

    python extract_all.py message.json -o tokens.raw.json
    python extract_all.py message.json -o tokens.raw.json --schema schema.json

규격은 references/full-extract.md 4단계와 같다. 이 스크립트가 지키는 원칙:

  1. 버리지 않는다 — 용도에 맞춰 미리 줄이지 않는다. 숨김 페인트(visible=false)도
     hidden 표시를 달아 포함한다.
  2. 지어내지 않는다 — 값이 없으면 None이 아니라 "미확인"으로 적고, 찾아봤지만
     없던 필드는 notFound에 남긴다.
  3. 근거를 적는다 — 값마다 source(variable/style/label/infer)를 붙이고,
     infer로 잡힌 것은 needsConfirmation에 다시 모은다.
  4. 단위를 붙인다 — px/%/배수(ratio)/도(deg)를 명시하고, 색은 8자리 HEX와
     알파 분리값을 함께 적는다.

행간 배수(ratio) 환산은 fig_tokens.py의 관례를 그대로 따른다.
  PIXELS  → value / fontSize
  PERCENT → value / 100
  그 외(RAW 등) → "미확인" (fig_tokens.py는 0.0으로 떨어뜨리지만, 여기서는
  지어낸 0보다 미확인이 맞다. 원본 value/units는 그대로 남긴다.)
"""
import argparse
import collections
import json
import math
import pathlib
import sys
from datetime import datetime

UNKNOWN = "미확인"

# ── A~N 항목표. notFound/unclassifiedFields 판정의 기준이 된다. ──────────────
# full-extract.md 2단계의 필드명을 그대로 옮긴 것이다. 여기 없는 필드가 스키마에
# 나오면 unclassifiedFields로 보고된다(= Figma 버전이 올라가 필드가 늘어난 신호).
FIELD_GROUPS = {
    "B_color": [
        "fillPaints", "strokePaints", "backgroundPaints", "backgroundColor",
        "prototypeBackgroundColor",
    ],
    "C_typography": [
        "fontName", "fontSize", "lineHeight", "letterSpacing", "textTracking",
        "paragraphIndent", "paragraphSpacing", "listSpacing", "textCase",
        "textDecoration", "textAlignHorizontal", "textAlignVertical",
        "textAutoResize", "textTruncation", "hyperlink", "fontVariations",
        "detachOpticalSizeFromFontSize", "fontVariantCommonLigatures",
        "fontVariantContextualLigatures", "fontVariantDiscretionaryLigatures",
        "fontVariantHistoricalLigatures", "fontVariantOrdinal",
        "fontVariantSlashedZero", "fontVariantNumericFigure",
        "fontVariantNumericSpacing", "fontVariantNumericFraction",
        "fontVariantCaps", "fontVariantPosition", "toggledOnOTFeatures",
        "toggledOffOTFeatures", "textData", "textListData", "directionality",
    ],
    "D_radius": [
        "cornerRadius", "rectangleTopLeftCornerRadius", "rectangleTopRightCornerRadius",
        "rectangleBottomLeftCornerRadius", "rectangleBottomRightCornerRadius",
        "rectangleCornerRadiiIndependent", "cornerSmoothing", "arcData",
        "starInnerScale", "count",
    ],
    "E_stroke": [
        "strokeWeight", "strokeAlign", "strokeCap", "strokeJoin", "miterLimit",
        "dashPattern", "dashMode", "borderTopWeight", "borderBottomWeight",
        "borderLeftWeight", "borderRightWeight", "borderStrokeWeightsIndependent",
        "borderTopHidden", "borderBottomHidden", "borderLeftHidden",
        "borderRightHidden", "bordersTakeSpace",
    ],
    "F_effect": ["effects"],
    "G_layout": [
        "stackMode", "stackSpacing", "stackPadding", "stackHorizontalPadding",
        "stackVerticalPadding", "stackPaddingRight", "stackPaddingBottom",
        "stackAlign", "stackCounterAlign", "stackJustify", "stackPrimarySizing",
        "stackCounterSizing", "stackPrimaryAlignItems", "stackCounterAlignItems",
        "stackWidth", "stackHeight", "stackChildPrimaryGrow", "stackChildAlignSelf",
        "stackPositioning", "stackReverseZIndex", "fixedChildrenDivider",
        "size", "transform", "horizontalConstraint", "verticalConstraint",
        "proportionsConstrained",
    ],
    "H_grid": ["layoutGrids", "guides"],
    "I_display": [
        "opacity", "blendMode", "visible", "locked", "mask", "maskIsOutline",
        "exportContentsOnly", "backgroundEnabled", "backgroundOpacity",
        "frameMaskDisabled", "resizeToFit", "scrollDirection", "scrollBehavior",
        "scrollOffset", "sectionContentsHidden",
    ],
    "J_variable": ["variableData", "variableSetID", "variableDataValues"],
    "K_style": [
        "styleID", "styleType", "styleDescription", "isFillStyle", "isStrokeStyle",
        "isPublishable", "inheritFillStyleID", "inheritStrokeStyleID",
        "inheritTextStyleID", "inheritEffectStyleID", "inheritGridStyleID",
        "inheritExportStyleID", "inheritFillStyleIDForStroke",
        "inheritFillStyleIDForBackground", "sharedStyleReference",
        "sharedStyleMasterData",
    ],
    "L_component": [
        "symbolData", "symbolDescription", "componentKey", "originComponentKey",
        "componentPropDefs", "componentPropRefs", "componentPropAssignments",
        "isStateGroup", "stateGroupPropertyValueOrders", "overriddenSymbolID",
        "sharedSymbolReference", "publishFile", "publishID", "publishedVersion",
        "pluginRelaunchData",
    ],
    "M_export_motion": [
        "exportSettings", "prototypeInteractions", "interactionType",
        "transitionType", "transitionDuration", "easingType", "easingFunction",
        "transitionShouldSmartAnimate", "transitionTimeout", "navigationType",
        "overlayPositionType", "overlayBackgroundAppearance", "connectionType",
        "connectionURL", "prototypeDevice", "prototypeStartingPoint",
    ],
    "N_name": [
        "name", "htmlTag", "ariaRole", "accessibleLabel", "pluginData",
        "embedData", "linkPreviewData", "codeBlockLanguage", "widgetMetadata",
    ],
}
DECLARED = {f for fs in FIELD_GROUPS.values() for f in fs}

PAINT_ARRAY_FIELDS = ["fillPaints", "strokePaints", "backgroundPaints"]
PAINT_COLOR_FIELDS = ["backgroundColor", "prototypeBackgroundColor"]
SPACING_FIELDS = [
    "stackSpacing", "stackPadding", "stackHorizontalPadding", "stackVerticalPadding",
    "stackPaddingRight", "stackPaddingBottom",
]
RADIUS_FIELDS = [
    "cornerRadius", "rectangleTopLeftCornerRadius", "rectangleTopRightCornerRadius",
    "rectangleBottomLeftCornerRadius", "rectangleBottomRightCornerRadius",
]


# ── 값 변환 ────────────────────────────────────────────────────────────────
def hex8(c):
    """색을 8자리 HEX로. 알파 1.0도 생략하지 않는다."""
    if not isinstance(c, dict):
        return UNKNOWN
    ch = [max(0, min(255, round(float(c.get(k, 0) or 0) * 255))) for k in ("r", "g", "b")]
    a = c.get("a")
    ch.append(max(0, min(255, round(float(1 if a is None else a) * 255))))
    return "#%02X%02X%02X%02X" % tuple(ch)


def alpha_of(c):
    if not isinstance(c, dict):
        return UNKNOWN
    a = c.get("a")
    return 1.0 if a is None else round(float(a), 4)


def num(v):
    """실수를 보기 좋게. 정수면 정수로."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return UNKNOWN
    return int(f) if f == int(f) else round(f, 4)


def gradient_geometry(tr):
    """그라디언트 transform에서 각도와 시작·끝 좌표를 유도한다.

    Figma의 그라디언트 행렬은 오브젝트 정규좌표 → 그라디언트 공간 사상이다.
    따라서 역행렬로 (0,0.5)·(1,0.5)를 되돌리면 오브젝트 위의 시작·끝점이 나온다.
    **이 값은 원본이 아니라 유도값이다.** 행렬이 없거나 특이행렬이면 미확인으로 둔다.
    """
    if not isinstance(tr, dict):
        return {"angleDeg": UNKNOWN, "start": UNKNOWN, "end": UNKNOWN, "derived": True}
    try:
        a, b, tx = float(tr["m00"]), float(tr["m01"]), float(tr["m02"])
        c, d, ty = float(tr["m10"]), float(tr["m11"]), float(tr["m12"])
    except (KeyError, TypeError, ValueError):
        return {"angleDeg": UNKNOWN, "start": UNKNOWN, "end": UNKNOWN, "derived": True}
    det = a * d - b * c
    if abs(det) < 1e-12:
        return {"angleDeg": UNKNOWN, "start": UNKNOWN, "end": UNKNOWN, "derived": True}

    def inv(x, y):
        x, y = x - tx, y - ty
        return ((d * x - b * y) / det, (-c * x + a * y) / det)

    sx, sy = inv(0.0, 0.5)
    ex, ey = inv(1.0, 0.5)
    return {
        "angleDeg": round(math.degrees(math.atan2(ey - sy, ex - sx)), 2),
        "start": {"x": round(sx, 4), "y": round(sy, 4)},
        "end": {"x": round(ex, 4), "y": round(ey, 4)},
        "derived": True,
    }


def line_ratio(lh, size):
    """행간 배수와 그 환산 근거를 함께 돌려준다.

    PIXELS  → value / fontSize
    PERCENT → value / 100
    RAW     → value 그대로 배수로 본다.
              실제 파일(fig-kiwi v106)에서 RAW 값은 1.2 / 1.3 / 1.4 / 1.5 뿐이었고
              해당 fontSize는 13~64px였다. px로 보면 1.5px, %로 보면 1.5%가 되어
              성립하지 않으므로 배수로 읽는 것이 유일하게 말이 된다.
              다만 이것은 관측에 근거한 해석이므로 basis에 표시해 둔다.
    그 외    → 미확인.
    """
    if not isinstance(lh, dict):
        return UNKNOWN, UNKNOWN
    units, val = lh.get("units"), lh.get("value")
    if val is None:
        return UNKNOWN, UNKNOWN
    try:
        val = float(val)
    except (TypeError, ValueError):
        return UNKNOWN, UNKNOWN
    if units == "PIXELS" and size:
        return round(val / float(size), 4), "value / fontSize"
    if units == "PERCENT":
        return round(val / 100, 4), "value / 100"
    if units == "RAW":
        return round(val, 4), "RAW을 배수로 해석 (관측 근거 — 코드 주석 참조)"
    return UNKNOWN, UNKNOWN


def is_token_path(name):
    """이름이 토큰 경로인지 판정한다.

    `color/bg/brand`, `Primary / Default`, `Neutral / Gray Light`는 토큰 경로다.
    그런데 슬래시가 들어 있다고 다 토큰이 아니다. 실제 파일에서 이런 것들이
    잘못 걸렸다.

        '26 / 30'                  분수·점수 표기 (본문 텍스트)
        '5 / 5'                    위와 같음
        'apple.com/kr/environment' URL (본문 텍스트)

    이런 이름을 label로 승격하면 그 값이 needsConfirmation을 빠져나가 사용자
    확인을 못 받는다. 그래서 각 구간이 **글자로 시작하고 점을 포함하지 않을**
    때만 토큰 경로로 본다. 숫자로 시작하면 분수, 점이 있으면 URL로 본다.
    """
    if not name or "/" not in name or len(name) > 80 or name.lower().startswith("http"):
        return False
    parts = [p.strip() for p in name.split("/")]
    if len(parts) < 2 or not all(parts):
        return False
    return all(p[0].isalpha() and "." not in p for p in parts)


def name_source(node):
    """이 노드에서 나온 값의 출처를 정한다.

    우선순위는 full-extract.md 3단계와 같다.
      style — 공유 스타일이 붙어 있다
      label — 이름이 토큰 경로다(color/bg/brand). 토큰 이름의 근거로 본다
      infer — 위 어느 것도 아니다. 확인 대상이 된다
    (variable은 VARIABLE 노드에서 직접 나오므로 여기서 판정하지 않는다.)
    """
    if node.get("styleType") or node.get("styleID"):
        return "style"
    if is_token_path(node.get("name")):
        return "label"
    return "infer"


class Bag:
    """같은 값을 합치면서 등장 횟수와 출처, 나온 노드를 함께 모은다."""

    def __init__(self):
        self.rows = {}

    def add(self, key, payload, source, node_name):
        r = self.rows.get(key)
        if r is None:
            r = self.rows[key] = dict(payload, source=source, count=0, nodes=[])
        r["count"] += 1
        # 더 믿을 만한 출처가 나중에 나오면 승격한다(infer < label < style < variable).
        rank = {"infer": 0, "label": 1, "style": 2, "variable": 3}
        if rank.get(source, 0) > rank.get(r["source"], 0):
            r["source"] = source
        if node_name and len(r["nodes"]) < 8 and node_name not in r["nodes"]:
            r["nodes"].append(node_name)
        return r

    def list(self):
        return sorted(self.rows.values(), key=lambda r: -r["count"])


def main():
    ap = argparse.ArgumentParser(description="노드 트리에서 A~N 전량을 뽑아 tokens.raw.json을 만든다")
    ap.add_argument("message_json")
    ap.add_argument("-o", "--output", default="tokens.raw.json")
    ap.add_argument("--schema", help="fig_decode.mjs --schema 가 만든 schema.json")
    args = ap.parse_args()

    src = pathlib.Path(args.message_json)
    if not src.exists():
        sys.exit(f"입력 파일이 없습니다: {src}")
    blob = json.loads(src.read_text(encoding="utf-8"))
    message = blob.get("message") or {}
    nodes = message.get("nodeChanges") or []
    if not nodes:
        sys.exit("nodeChanges가 비어 있습니다. fig_decode.mjs 출력이 맞는지 확인하세요.")

    header = blob.get("header") or {}
    meta = blob.get("meta") or {}
    images = blob.get("images") or []

    schema_fields, enum_values, node_fields, unclassified_basis = [], {}, [], UNKNOWN
    if args.schema:
        sp = pathlib.Path(args.schema)
        if not sp.exists():
            sys.exit(f"스키마 파일이 없습니다: {sp}")
        sj = json.loads(sp.read_text(encoding="utf-8"))
        schema_fields = sj.get("allFieldNames") or []
        enum_values = sj.get("enumValues") or {}
        # 미분류 판정은 NodeChange의 최상위 필드로만 한다. allFieldNames에는 중첩
        # 구조체 멤버(Color.r, ColorStop.position 등)까지 섞여 있어서 그대로 쓰면
        # "새 필드가 생겼다"는 거짓 신호가 난다.
        for d in (sj.get("definitions") or []):
            if d.get("name") == "NodeChange":
                node_fields = [f.get("name") for f in (d.get("fields") or []) if f.get("name")]
                unclassified_basis = "NodeChange 최상위 필드"
                break
        if not node_fields and schema_fields:
            node_fields = schema_fields
            unclassified_basis = "allFieldNames(중첩 멤버 포함 — NodeChange 정의를 못 찾음)"

    seen_fields = set()
    by_type = collections.Counter()

    # guid → 노드. parentIndex.guid로 부모를 되짚어 "최상위 프레임"(부모가 CANVAS)을
    # 가려낸다. 실제 파일(v106)은 모든 노드가 guid/parentIndex를 갖고 있다.
    def gkey(g):
        return f"{g.get('sessionID')}:{g.get('localID')}" if isinstance(g, dict) else None

    by_guid = {}
    for n in nodes:
        if isinstance(n, dict) and gkey(n.get("guid")):
            by_guid[gkey(n["guid"])] = n

    def parent_of(n):
        pi = n.get("parentIndex")
        if not isinstance(pi, dict):
            return None
        return by_guid.get(gkey(pi.get("guid")))

    color, typo, radius, stroke, effect, spacing = Bag(), Bag(), Bag(), Bag(), Bag(), Bag()
    grid, layout, motion = Bag(), Bag(), Bag()
    variables, styles, components, exports, names = [], [], [], [], []
    pages, top_frames = [], []
    spacing_values = []

    def add_paint(paint, owner, field, node):
        if not isinstance(paint, dict):
            return
        ptype = paint.get("type") or UNKNOWN
        col = paint.get("color")
        entry = {
            "paintType": ptype,
            "field": field,
            "hex8": hex8(col) if isinstance(col, dict) else UNKNOWN,
            "alpha": alpha_of(col) if isinstance(col, dict) else UNKNOWN,
            "rgba": ({k: round(float(col.get(k, 0) or 0), 6) for k in "rgba"}
                     if isinstance(col, dict) else UNKNOWN),
            "opacity": num(paint["opacity"]) if "opacity" in paint else UNKNOWN,
            "blendMode": paint.get("blendMode", UNKNOWN),
            "hidden": paint.get("visible") is False,
        }
        stops = paint.get("stops")
        if isinstance(stops, list) and stops:
            entry["stops"] = [{
                "hex8": hex8(s.get("color")),
                "alpha": alpha_of(s.get("color")),
                "position": num(s.get("position")),
            } for s in stops if isinstance(s, dict)]
            entry["gradient"] = gradient_geometry(paint.get("transform"))
        if ptype == "IMAGE" or paint.get("imageScaleMode"):
            entry["image"] = {
                "scaleMode": paint.get("imageScaleMode", UNKNOWN),
                "rotation": num(paint["rotation"]) if "rotation" in paint else UNKNOWN,
                "scale": num(paint["scale"]) if "scale" in paint else UNKNOWN,
                "originalWidth": paint.get("originalImageWidth", UNKNOWN),
                "originalHeight": paint.get("originalImageHeight", UNKNOWN),
                "hash": (paint.get("image") or {}).get("hash", UNKNOWN)
                        if isinstance(paint.get("image"), dict) else paint.get("image", UNKNOWN),
            }
        if paint.get("filterColorAdjust") is not None:
            entry["filterColorAdjust"] = paint["filterColorAdjust"]
        key = json.dumps([entry["paintType"], entry["hex8"], entry.get("stops"),
                          entry["hidden"], field], sort_keys=True, ensure_ascii=False)
        color.add(key, entry, name_source(node), owner)

    for n in nodes:
        if not isinstance(n, dict):
            continue
        seen_fields.update(n.keys())
        ntype = n.get("type") or UNKNOWN
        by_type[ntype] += 1
        nm = n.get("name") or ""
        src_kind = name_source(n)

        # A — 페이지·최상위 프레임
        if ntype == "CANVAS":
            bg = n.get("backgroundColor")
            pages.append({"name": nm or UNKNOWN,
                          "background": hex8(bg) if isinstance(bg, dict) else UNKNOWN})
        if ntype in ("FRAME", "SECTION"):
            sz = n.get("size") or {}
            tr = n.get("transform") or {}
            par = parent_of(n)
            w = num(sz.get("x")) if sz else UNKNOWN
            h = num(sz.get("y")) if sz else UNKNOWN
            top_frames.append({
                "name": nm or UNKNOWN, "type": ntype,
                "width": w, "height": h, "sizeUnit": "px",
                "x": num(tr.get("m02")) if tr else UNKNOWN,
                "y": num(tr.get("m12")) if tr else UNKNOWN,
                "parent": (f"{par.get('type')}:{par.get('name')}" if par
                           else (UNKNOWN if n.get("parentIndex") else "(없음)")),
                # 부모가 CANVAS면 페이지 바로 아래 놓인 최상위 프레임이다.
                "isTopLevel": bool(par and par.get("type") == "CANVAS"),
                "aspect": (round(float(w) / float(h), 4)
                           if isinstance(w, (int, float)) and isinstance(h, (int, float)) and h
                           else UNKNOWN),
            })

        # B — 색
        for f in PAINT_ARRAY_FIELDS:
            for p in (n.get(f) or []):
                add_paint(p, nm, f, n)
        for f in PAINT_COLOR_FIELDS:
            if isinstance(n.get(f), dict):
                add_paint({"type": "SOLID", "color": n[f]}, nm, f, n)

        # C — 타이포
        if n.get("fontSize") is not None or n.get("fontName"):
            fn = n.get("fontName") or {}
            size = n.get("fontSize")
            lh = n.get("lineHeight") or {}
            ls = n.get("letterSpacing") or {}
            ot = {k: n[k] for k in FIELD_GROUPS["C_typography"]
                  if k.startswith("fontVariant") and k in n}
            td = n.get("textData") or {}
            entry = {
                "token": nm or UNKNOWN,
                "family": fn.get("family", UNKNOWN),
                "style": fn.get("style", UNKNOWN),
                "postscript": fn.get("postscript", UNKNOWN),
                "size": num(size) if size is not None else UNKNOWN,
                "sizeUnit": "px",
                "lineHeight": {"value": num(lh.get("value")) if lh else UNKNOWN,
                               "units": lh.get("units", UNKNOWN) if lh else UNKNOWN,
                               "ratio": line_ratio(lh, size)[0],
                               "ratioBasis": line_ratio(lh, size)[1]},
                "letterSpacing": {"value": num(ls.get("value")) if ls else UNKNOWN,
                                  "units": ls.get("units", UNKNOWN) if ls else UNKNOWN},
                "case": n.get("textCase", UNKNOWN),
                "decoration": n.get("textDecoration", UNKNOWN),
                "align": {"h": n.get("textAlignHorizontal", UNKNOWN),
                          "v": n.get("textAlignVertical", UNKNOWN)},
                "autoResize": n.get("textAutoResize", UNKNOWN),
                "truncation": n.get("textTruncation", UNKNOWN),
                "paragraphIndent": num(n["paragraphIndent"]) if "paragraphIndent" in n else UNKNOWN,
                "paragraphSpacing": num(n["paragraphSpacing"]) if "paragraphSpacing" in n else UNKNOWN,
                "listSpacing": num(n["listSpacing"]) if "listSpacing" in n else UNKNOWN,
                "openType": ot or UNKNOWN,
                "characters": td.get("characters", UNKNOWN) if isinstance(td, dict) else UNKNOWN,
                "hasStyleOverrides": bool(isinstance(td, dict) and td.get("styleOverrideTable")),
            }
            key = json.dumps([entry["family"], entry["style"], entry["size"],
                              entry["lineHeight"], entry["letterSpacing"], entry["case"]],
                             sort_keys=True, ensure_ascii=False)
            typo.add(key, entry, src_kind, nm)

        # D — 라운드·형태
        for f in RADIUS_FIELDS:
            if n.get(f) is not None:
                radius.add(f"{f}:{num(n[f])}",
                           {"field": f, "value": num(n[f]), "unit": "px",
                            "independent": n.get("rectangleCornerRadiiIndependent", UNKNOWN),
                            "cornerSmoothing": num(n["cornerSmoothing"]) if "cornerSmoothing" in n else UNKNOWN},
                           src_kind, nm)
        for f in ("arcData", "starInnerScale", "count"):
            if n.get(f) is not None:
                radius.add(f"{f}:{json.dumps(n[f], sort_keys=True, ensure_ascii=False)}",
                           {"field": f, "value": n[f], "unit": "deg/ratio/개"}, src_kind, nm)

        # E — 선·테두리
        for f in FIELD_GROUPS["E_stroke"]:
            if n.get(f) is not None:
                unit = "px" if "Weight" in f or f == "miterLimit" else "-"
                stroke.add(f"{f}:{json.dumps(n[f], sort_keys=True, ensure_ascii=False)}",
                           {"field": f, "value": num(n[f]) if unit == "px" else n[f],
                            "unit": unit}, src_kind, nm)

        # F — 그림자·블러
        for e in (n.get("effects") or []):
            if not isinstance(e, dict):
                continue
            off = e.get("offset") or {}
            entry = {
                "type": e.get("type", UNKNOWN),
                "hex8": hex8(e.get("color")) if isinstance(e.get("color"), dict) else UNKNOWN,
                "alpha": alpha_of(e.get("color")) if isinstance(e.get("color"), dict) else UNKNOWN,
                "offset": {"x": num(off.get("x")), "y": num(off.get("y")), "unit": "px"} if off else UNKNOWN,
                "radius": num(e["radius"]) if "radius" in e else UNKNOWN,
                "spread": num(e["spread"]) if "spread" in e else UNKNOWN,
                "radiusUnit": "px",
                "blendMode": e.get("blendMode", UNKNOWN),
                "showShadowBehindNode": e.get("showShadowBehindNode", UNKNOWN),
                "hidden": e.get("visible") is False,
            }
            effect.add(json.dumps(entry, sort_keys=True, ensure_ascii=False), entry, src_kind, nm)

        # G — 레이아웃 / 간격
        for f in SPACING_FIELDS:
            if n.get(f) is not None:
                v = num(n[f])
                spacing_values.append(v)
                spacing.add(f"{f}:{v}", {"field": f, "value": v, "unit": "px"}, src_kind, nm)
        lay = {f: n[f] for f in FIELD_GROUPS["G_layout"]
               if f in n and f not in ("size", "transform")}
        if lay:
            layout.add(json.dumps(lay, sort_keys=True, ensure_ascii=False),
                       {"props": lay}, src_kind, nm)

        # H — 그리드·가이드
        for g in (n.get("layoutGrids") or []):
            if isinstance(g, dict):
                entry = dict(g)
                if isinstance(g.get("color"), dict):
                    entry["hex8"] = hex8(g["color"])
                    entry["alpha"] = alpha_of(g["color"])
                grid.add(json.dumps(entry, sort_keys=True, ensure_ascii=False),
                         {"grid": entry, "unit": "px"}, src_kind, nm)
        if n.get("guides"):
            grid.add(f"guides:{nm}", {"guides": n["guides"], "unit": "px"}, src_kind, nm)

        # J — 변수
        if ntype == "VARIABLE" or n.get("variableData") or n.get("variableDataValues"):
            variables.append({
                "name": nm or UNKNOWN,
                "collection": n.get("variableSetID", UNKNOWN),
                "type": n.get("variableResolvedType") or n.get("variableDataType") or UNKNOWN,
                "description": n.get("description", UNKNOWN),
                "modes": n.get("variableDataValues", UNKNOWN),
                "alias": n.get("variableAlias", UNKNOWN),
                "initialValue": n.get("initialValue", UNKNOWN),
                "isDeleted": n.get("isDeleted", UNKNOWN),
                "scope": n.get("variableScope", UNKNOWN),
                "raw": {k: n[k] for k in FIELD_GROUPS["J_variable"] if k in n} or UNKNOWN,
            })

        # K — 공유 스타일
        if n.get("styleType") or n.get("styleID"):
            styles.append({
                "name": nm or UNKNOWN,
                "type": n.get("styleType", UNKNOWN),
                "styleID": n.get("styleID", UNKNOWN),
                "description": n.get("styleDescription", UNKNOWN),
                "isFillStyle": n.get("isFillStyle", UNKNOWN),
                "isStrokeStyle": n.get("isStrokeStyle", UNKNOWN),
                "inherit": {k: n[k] for k in FIELD_GROUPS["K_style"]
                            if k.startswith("inherit") and k in n} or UNKNOWN,
            })

        # L — 컴포넌트·인스턴스
        if ntype in ("SYMBOL", "INSTANCE") or n.get("componentKey"):
            components.append({
                "name": nm or UNKNOWN,
                "nodeType": ntype,
                "componentKey": n.get("componentKey", UNKNOWN),
                "originComponentKey": n.get("originComponentKey", UNKNOWN),
                "description": n.get("symbolDescription", UNKNOWN),
                "propDefs": n.get("componentPropDefs", UNKNOWN),
                "propRefs": n.get("componentPropRefs", UNKNOWN),
                "propAssignments": n.get("componentPropAssignments", UNKNOWN),
                "isStateGroup": n.get("isStateGroup", UNKNOWN),
                "variantOrders": n.get("stateGroupPropertyValueOrders", UNKNOWN),
                "publish": {k: n[k] for k in ("publishFile", "publishID", "publishedVersion")
                            if k in n} or UNKNOWN,
            })

        # M — 내보내기·모션
        for es in (n.get("exportSettings") or []):
            exports.append({"node": nm or UNKNOWN, "setting": es})
        for f in ("transitionType", "transitionDuration", "easingType", "easingFunction",
                  "navigationType", "interactionType", "overlayPositionType",
                  "connectionType", "transitionShouldSmartAnimate", "transitionTimeout"):
            if n.get(f) is not None:
                unit = "ms" if f in ("transitionDuration", "transitionTimeout") else "-"
                motion.add(f"{f}:{json.dumps(n[f], sort_keys=True, ensure_ascii=False)}",
                           {"field": f, "value": n[f], "unit": unit}, src_kind, nm)
        if n.get("prototypeInteractions"):
            motion.add(f"prototypeInteractions:{nm}",
                       {"field": "prototypeInteractions",
                        "value": n["prototypeInteractions"], "unit": "-"}, src_kind, nm)

        # N — 이름·접근성
        a11y = {k: n[k] for k in FIELD_GROUPS["N_name"] if k in n and k != "name"}
        if nm or a11y:
            names.append({"name": nm or UNKNOWN, "type": ntype,
                          "slashPath": "/" in nm, **({"a11y": a11y} if a11y else {})})

    # 간격 기준 단위 — 4·8 배수 체계가 보이면 함께 보고한다.
    base_unit = UNKNOWN
    ints = [int(v) for v in spacing_values if isinstance(v, (int, float)) and float(v) == int(v) and v > 0]
    if ints:
        if all(v % 8 == 0 for v in ints):
            base_unit = 8
        elif all(v % 4 == 0 for v in ints):
            base_unit = 4
        else:
            g = 0
            for v in ints:
                g = math.gcd(g, v)
            base_unit = g or UNKNOWN

    # notFound — 항목표에 적힌 필드 중 이 파일의 노드에 한 번도 안 나온 것.
    not_found = sorted(DECLARED - seen_fields)
    # unclassifiedFields — 스키마에는 있는데 항목표에 없는 필드(= 새로 늘어난 필드).
    # type은 stats.byType으로 이미 다루므로 제외한다.
    unclassified = sorted(set(node_fields) - DECLARED - {"type"}) if node_fields else []
    # 스키마 전체를 그대로 나열하면 쓸 수 없다. 실제 파일(v106)에서 미분류가 437개
    # 나왔지만 그중 노드에 실제로 나타난 것은 18개뿐이었다. 나머지는 이 파일이 쓰지
    # 않는 필드다. 확인해야 할 것과 참고용을 나눈다.
    unclassified_present = [f for f in unclassified if f in seen_fields]
    unclassified_schema_only = [f for f in unclassified if f not in seen_fields]

    needs = []
    for label, bag in (("color", color), ("typography", typo), ("radius", radius),
                       ("stroke", stroke), ("effect", effect), ("spacing", spacing),
                       ("grid", grid), ("layout", layout), ("motion", motion)):
        for r in bag.list():
            if r["source"] == "infer":
                needs.append({
                    "token": r.get("token") or r.get("field") or label,
                    "category": label,
                    "value": r.get("hex8") or r.get("value") or r.get("family") or UNKNOWN,
                    "why": "빈도 추정 — 변수·스타일·이름표 근거 없음",
                })

    out = {
        "source": {
            "file": meta.get("file_name", UNKNOWN),
            "input": str(src),
            "format": header.get("prelude", UNKNOWN),
            "version": header.get("version", UNKNOWN),
            "decodedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "stats": {
            "nodeCount": len(nodes),
            "byType": dict(by_type.most_common()),
            "imageCount": len(images),
            "imageBytes": sum(int(i.get("bytes") or 0) for i in images),
            "uniqueFieldsSeen": len(seen_fields),
        },
        "document": {
            "pages": pages or UNKNOWN,
            "frames": top_frames or UNKNOWN,
            "topLevelFrames": [f for f in top_frames if f.get("isTopLevel")] or UNKNOWN,
            "images": images or UNKNOWN,
        },
        "schemaFields": schema_fields or UNKNOWN,
        "enumValues": enum_values or UNKNOWN,
        "variables": variables,
        "styles": styles,
        "color": color.list(),
        "typography": typo.list(),
        "radius": radius.list(),
        "stroke": stroke.list(),
        "effect": effect.list(),
        "spacing": {"values": spacing.list(), "baseUnit": base_unit, "unit": "px"},
        "grid": grid.list(),
        "layout": layout.list(),
        "component": components,
        "export": exports,
        "motion": motion.list(),
        "unclassifiedFields": {
            "present": unclassified_present,        # 이 파일 노드에 실제로 나타난 미분류 필드
            "schemaOnly": unclassified_schema_only,  # 스키마에만 있고 이 파일은 안 쓴 필드
            "basis": unclassified_basis,
        },
        "needsConfirmation": needs,
        "notFound": not_found,
    }
    pathlib.Path(args.output).write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # 요약만 콘솔에. JSON 전문은 찍지 않는다.
    print(f"파일        : {out['source']['file']} ({out['source']['format']} v{out['source']['version']})")
    print(f"노드        : {len(nodes)}개 / 이미지 {len(images)}개")
    print(f"노드 타입   : {' '.join(f'{k}={v}' for k, v in by_type.most_common())}")
    print()
    print("=== 뽑힌 항목 ===")
    print(f"  변수         {len(variables)}개" + ("" if variables else "   ← 이 파일에 Figma 변수가 없다"))
    print(f"  공유 스타일  {len(styles)}개" + ("" if styles else "   ← 이 파일에 공유 스타일이 없다"))
    print(f"  색           {len(out['color'])}개")
    print(f"  텍스트 스타일 {len(out['typography'])}개")
    print(f"  라운드       {len(out['radius'])}개")
    print(f"  선·테두리    {len(out['stroke'])}개")
    print(f"  효과         {len(out['effect'])}개")
    print(f"  간격         {len(out['spacing']['values'])}개 (기준 단위 {base_unit})")
    print(f"  그리드       {len(out['grid'])}개")
    print(f"  레이아웃     {len(out['layout'])}개")
    print(f"  컴포넌트     {len(components)}개")
    print(f"  내보내기     {len(exports)}개")
    print(f"  모션         {len(out['motion'])}개")
    print()
    if not variables and not styles:
        print("※ 변수도 공유 스타일도 없다. 이 파일은 디자인 시스템 파일이 아니다.")
        print("  값이 전부 빈도 추정으로 잡히므로 사용자 확인이 반드시 필요하다.")
        print()
    print(f"확인 필요    : {len(needs)}개 (추정으로 잡힌 값)")
    print(f"미분류 필드  : 실제 등장 {len(unclassified_present)}개"
          + (f" → {', '.join(unclassified_present[:12])}" if unclassified_present else "")
          + f" / 스키마에만 {len(unclassified_schema_only)}개")
    print(f"없던 항목    : {len(not_found)}개" + (f" → {', '.join(not_found[:12])}…" if not_found else ""))
    if not schema_fields:
        print("\n※ --schema 를 주지 않아 미분류 필드를 판정하지 못했다(전량 경로에서는 붙일 것).")
    print(f"\n저장        : {args.output}")


if __name__ == "__main__":
    main()
