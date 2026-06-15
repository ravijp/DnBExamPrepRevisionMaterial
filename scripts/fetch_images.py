# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Download images for a topic and (re)build its images.md manifest.

Reads a per-topic source list (JSON) describing each image to fetch, downloads
the files into <topic>/images/, and writes <topic>/images/images.md with
source URL, license, intended finding, and a verified? flag (always NO on
download — Claude cannot visually confirm a downloaded file's content; the
owner must spot-check and flip these to YES).

Source-list format (a JSON array), e.g. scripts/sources/02-bone-tumours.json:
[
  {
    "filename": "lodwick-grades.jpg",
    "url": "https://.../Fig1.jpg",
    "finding": "Lodwick decision tree IA-III",
    "license": "CC BY 4.0",
    "source_page": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8854272/"
  }
]

Usage (from repo root):
    uv run scripts/fetch_images.py paper-1-musculoskeletal/02-bone-tumours-approach \\
        scripts/sources/02-bone-tumours.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (DNB-revision-image-fetch; educational use)"


def fetch(url: str, dest: Path) -> tuple[bool, str]:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        dest.write_bytes(r.content)
        return True, f"{len(r.content):,} bytes"
    except Exception as e:  # noqa: BLE001 — report any failure, keep going
        return False, str(e)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topic_dir", help="Topic folder (relative to repo root or absolute)")
    ap.add_argument("sources", help="JSON source-list file")
    args = ap.parse_args()

    topic = (REPO / args.topic_dir) if not Path(args.topic_dir).is_absolute() else Path(args.topic_dir)
    images_dir = topic / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    sources = json.loads(Path(args.sources).read_text(encoding="utf-8"))

    rows = []
    for item in sources:
        dest = images_dir / item["filename"]
        ok, note = fetch(item["url"], dest)
        status = "downloaded" if ok else f"FAILED ({note})"
        print(f"[{status}] {item['filename']}  <- {item['url']}")
        rows.append({**item, "ok": ok})

    # Build images.md manifest
    lines = [
        f"# Image manifest — {topic.name}",
        "",
        "> Downloaded for revision. **`verified?` = NO until a human confirms the image",
        "> actually shows the stated finding** — these were fetched programmatically and not",
        "> visually checked. Copyright/licence clearance before any redistribution is the",
        "> repository owner's responsibility.",
        "",
        "| File | Finding it should show | Source | Licence | verified? |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        fname = r["filename"] if r["ok"] else f"~~{r['filename']}~~ (download failed)"
        src = f"[link]({r.get('source_page', r['url'])})"
        lines.append(
            f"| {fname} | {r['finding']} | {src} | {r.get('license', '?')} | NO |"
        )
    lines.append("")
    (images_dir / "images.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {images_dir / 'images.md'}")
    n_ok = sum(1 for r in rows if r["ok"])
    print(f"{n_ok}/{len(rows)} downloaded.")
    if n_ok < len(rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
