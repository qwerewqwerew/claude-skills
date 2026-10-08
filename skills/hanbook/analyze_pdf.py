# pip install --break-system-packages pymupdf
"""영문 원서 PDF를 번역하기 전에 구조·권리 표시·글꼴 정보를 요약한다.

기본 출력은 요약 JSON(장 경계, 쪽 번호 차이, 판권 면 후보, 글꼴 집계)이다.
글자 조각 단위의 전체 덤프가 필요할 때만 --full 경로를 함께 준다.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import pymupdf

CHAPTER_RE = re.compile(r"^(chapter|chap\.)\s*\d+", re.IGNORECASE)
PART_RE = re.compile(r"^part\s+(\d+|[ivxlc]+)\b", re.IGNORECASE)
BACK_MATTER_RE = re.compile(
    r"\b(index|other books|you may enjoy|unlock|exclusive benefits|"
    r"leave a review|about packt|newsletter|subscribe)\b",
    re.IGNORECASE,
)
RIGHTS_RE = re.compile(
    r"(©|copyright\s*\(c\)|copyright\s+\d{4}|all rights reserved|creative commons|"
    r"\bcc[ -]by\b|public domain|licensed under)",
    re.IGNORECASE,
)
MONO_HINTS = ("mono", "consolas", "courier", "code", "menlo", "inconsolata")
EMOJI_HINTS = ("emoji",)
PAGE_NUM_RE = re.compile(r"^\d{1,4}$")
INDEX_ENTRY_RE = re.compile(r"\s\d{1,4}(\s*[-–,]\s*\d{1,4})*\s*$")


def font_stats(doc: pymupdf.Document) -> dict:
    chars = Counter()
    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    chars[span.get("font", "")] += len(span.get("text", ""))
    total = sum(chars.values()) or 1
    fonts = [
        {"font": name, "chars": count, "share": round(count / total, 4)}
        for name, count in chars.most_common()
        if name
    ]
    return {
        "fonts": fonts,
        "body_font": fonts[0]["font"] if fonts else None,
        "monospace_fonts": [f["font"] for f in fonts if any(h in f["font"].lower() for h in MONO_HINTS)],
        "emoji_fonts": [f["font"] for f in fonts if any(h in f["font"].lower() for h in EMOJI_HINTS)],
    }


def label_number(page: pymupdf.Page) -> int | None:
    """PDF에 들어 있는 쪽 라벨(인쇄 쪽 번호 정보)이 숫자면 그 값을 쓴다."""
    label = page.get_label().strip()
    return int(label) if PAGE_NUM_RE.match(label) else None


def edge_number(page: pymupdf.Page) -> int | None:
    """쪽 위·아래 12% 띠의 블록에서 첫 줄 또는 마지막 줄이 숫자뿐이면 쪽 번호로 본다.

    머리글과 쪽 번호가 한 블록에 묶인 경우("장 제목\\n9")도 잡기 위해 줄 단위로 본다.
    """
    height = page.rect.height
    for block in page.get_text("blocks"):
        y0, y1, text = block[1], block[3], block[4]
        if not (y1 < height * 0.12 or y0 > height * 0.88):
            continue
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        for candidate in (lines[:1] + lines[-1:]) if lines else []:
            if PAGE_NUM_RE.match(candidate):
                return int(candidate)
    return None


def collect_offsets(doc: pymupdf.Document, reader) -> Counter:
    offsets = Counter()
    for index, page in enumerate(doc, 1):
        number = reader(page)
        if number is not None:
            offsets[index - number] += 1
    return offsets


def page_offset(doc: pymupdf.Document) -> dict:
    """PDF 쪽 번호 - 인쇄 쪽 번호의 최빈값을 구한다. 쪽 라벨을 먼저 보고, 없으면 쪽 가장자리 숫자를 본다."""
    for method, reader in (("page_label", label_number), ("edge_text", edge_number)):
        offsets = collect_offsets(doc, reader)
        if offsets:
            offset, count = offsets.most_common(1)[0]
            return {
                "offset": offset,
                "method": method,
                "evidence_pages": count,
                "other_offsets": {str(k): v for k, v in offsets.most_common(5) if k != offset},
                "note": "PDF 쪽 = 인쇄 쪽 + offset. other_offsets가 많으면 앞부분 로마 숫자 등 별도 번호 체계가 섞인 것이다",
            }
    return {"offset": None, "method": None, "evidence_pages": 0, "note": "인쇄 쪽 번호를 찾지 못했다"}


def rights_candidates(doc: pymupdf.Document) -> list[dict]:
    """앞 12쪽과 뒤 6쪽에서 권리 표시 문구가 있는 쪽을 찾는다. 문구는 한 줄만 남긴다."""
    indexes = list(range(min(12, len(doc)))) + list(range(max(0, len(doc) - 6), len(doc)))
    found = []
    for index in sorted(set(indexes)):
        for line in doc[index].get_text().splitlines():
            if RIGHTS_RE.search(line) and not INDEX_ENTRY_RE.search(line):
                found.append({"page": index + 1, "line": line.strip()[:120]})
                break
    return found


def structure(doc: pymupdf.Document) -> dict:
    toc = doc.get_toc()
    levels = Counter(level for level, _, _ in toc)
    top_level = min(levels) if levels else None
    entries = [(title, page) for level, title, page in toc if level == top_level]
    last_chapter = max(
        (i for i, (title, _) in enumerate(entries) if CHAPTER_RE.match(title)),
        default=-1,
    )
    units = []
    for i, (title, start) in enumerate(entries):
        end = entries[i + 1][1] - 1 if i + 1 < len(entries) else len(doc)
        if CHAPTER_RE.match(title):
            kind = "chapter"
        elif PART_RE.match(title):
            kind = "part"
        elif i < (last_chapter if last_chapter >= 0 else 0):
            kind = "front"
        else:
            kind = "back"
        exclude = kind in ("back", "chapter") and bool(BACK_MATTER_RE.search(title)) and i >= last_chapter
        images = sum(len(doc[p].get_images(full=True)) for p in range(start - 1, end))
        units.append(
            {
                "kind": kind,
                "title": title.strip()[:80],
                "pdf_start": start,
                "pdf_end": end,
                "pages": end - start + 1,
                "images": images,
                "exclude_candidate": exclude,
            }
        )
    return {
        "toc_entries": len(toc),
        "toc_levels": {str(k): v for k, v in sorted(levels.items())},
        "units": units,
        "chapter_count": sum(u["kind"] == "chapter" and not u["exclude_candidate"] for u in units),
        "part_count": sum(u["kind"] == "part" for u in units),
        "note": "책갈피가 없으면 units가 비어 있다. 목차 쪽과 큰 제목 줄로 장 경계를 다시 잡는다",
    }


def scan_check(doc: pymupdf.Document) -> dict:
    low_text = [i + 1 for i, page in enumerate(doc) if len(page.get_text().strip()) < 20 and page.get_images()]
    return {
        "image_only_pages": len(low_text),
        "likely_scanned": len(low_text) > len(doc) * 0.5,
        "sample_pages": low_text[:10],
    }


def full_dump(doc: pymupdf.Document) -> list[dict]:
    pages = []
    for number, page in enumerate(doc, 1):
        blocks = []
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            lines = [
                {
                    "bbox": line.get("bbox"),
                    "spans": [
                        {k: span.get(k) for k in ("text", "bbox", "font", "size", "color", "flags")}
                        for span in line.get("spans", [])
                    ],
                }
                for line in block.get("lines", [])
            ]
            blocks.append({"bbox": block.get("bbox"), "lines": lines})
        pages.append({"page": number, "text_blocks": blocks})
    return pages


def analyze(path: Path) -> dict:
    doc = pymupdf.open(path)
    sizes = Counter((round(p.rect.width), round(p.rect.height)) for p in doc)
    result = {
        "source": path.name,
        "page_count": len(doc),
        "page_sizes_pt": [{"width": w, "height": h, "pages": n} for (w, h), n in sizes.most_common()],
        "encrypted": doc.is_encrypted,
        "image_total": sum(len(p.get_images(full=True)) for p in doc),
        "rights": rights_candidates(doc),
        "page_numbering": page_offset(doc),
        "scan": scan_check(doc),
        "fonts": font_stats(doc),
        "structure": structure(doc),
    }
    doc.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, help="요약 JSON 경로. 없으면 화면에 출력")
    parser.add_argument("--full", type=Path, help="글자 조각 단위 전체 덤프 JSON 경로(선택)")
    args = parser.parse_args()

    summary = analyze(args.pdf)
    encoded = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded)

    if args.full:
        doc = pymupdf.open(args.pdf)
        args.full.parent.mkdir(parents=True, exist_ok=True)
        args.full.write_text(json.dumps(full_dump(doc), ensure_ascii=False), encoding="utf-8")
        doc.close()


if __name__ == "__main__":
    main()
