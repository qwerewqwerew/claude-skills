#!/usr/bin/env python3
"""Extract layout facts needed before translating a PDF."""

import argparse
import json
from pathlib import Path

import fitz


def analyze(path: Path) -> dict:
    document = fitz.open(path)
    pages = []
    fonts = set()
    for number, page in enumerate(document, 1):
        blocks = []
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            lines = []
            for line in block.get("lines", []):
                spans = []
                for span in line.get("spans", []):
                    fonts.add(span.get("font", ""))
                    spans.append(
                        {
                            "text": span.get("text", ""),
                            "bbox": span.get("bbox"),
                            "font": span.get("font"),
                            "size": span.get("size"),
                            "color": span.get("color"),
                            "flags": span.get("flags"),
                        }
                    )
                if spans:
                    lines.append({"bbox": line.get("bbox"), "spans": spans})
            if lines:
                blocks.append({"bbox": block.get("bbox"), "lines": lines})
        pages.append(
            {
                "page": number,
                "width": page.rect.width,
                "height": page.rect.height,
                "rotation": page.rotation,
                "image_count": len(page.get_images(full=True)),
                "text_blocks": blocks,
            }
        )
    metadata = document.metadata
    document.close()
    return {
        "source": str(path.resolve()),
        "page_count": len(pages),
        "fonts": sorted(font for font in fonts if font),
        "metadata": metadata,
        "pages": pages,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.pdf)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
