# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""One-time setup: extract the revision zip and flatten it into the repo root.

Idempotent and safe:
  * Extracts dnb-radiodiagnosis-revision.zip into a temp staging dir.
  * Moves the inner README.md and paper-* folders up into the repo root.
  * Removes the now-empty extracted wrapper folder.
  * Refuses to overwrite an existing target unless --force is given.

Run from the repo root:
    uv run scripts/setup_extract.py
    uv run scripts/setup_extract.py --force   # overwrite existing targets
"""
from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ZIP = REPO / "dnb-radiodiagnosis-revision.zip"
WRAPPER = "dnb-radiodiagnosis-revision"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="Overwrite existing targets in repo root")
    args = ap.parse_args()

    if not ZIP.exists():
        raise SystemExit(f"Zip not found: {ZIP}")

    with tempfile.TemporaryDirectory(dir=str(REPO)) as tmp:
        tmpdir = Path(tmp)
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(tmpdir)

        inner = tmpdir / WRAPPER
        if not inner.is_dir():
            # zip may not have a wrapper folder; treat tmpdir as the content root
            inner = tmpdir

        moved, skipped = [], []
        for item in sorted(inner.iterdir()):
            dest = REPO / item.name
            if dest.exists():
                if args.force:
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                else:
                    skipped.append(item.name)
                    continue
            shutil.move(str(item), str(dest))
            moved.append(item.name)

    # Remove any leftover empty wrapper at repo root (from a previous run)
    leftover = REPO / WRAPPER
    if leftover.is_dir() and not any(leftover.iterdir()):
        leftover.rmdir()

    print("Moved into repo root:", ", ".join(moved) or "(none)")
    if skipped:
        print("Skipped (already exist; use --force to overwrite):", ", ".join(skipped))


if __name__ == "__main__":
    main()
