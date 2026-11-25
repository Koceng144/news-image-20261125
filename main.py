#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty.

Copies the pre-composed entry image (entry.png, in this repository's
root) to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only. No network, no randomness, no time dependence:
both runs write the same bytes. Exits 0 on every path.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("cannot create output dir %s: %s" % (out_dir, exc),
              file=sys.stderr)
        return 0
    dst = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(SRC, dst)
    except OSError as exc:
        print("cannot copy %s to %s: %s" % (SRC, dst, exc), file=sys.stderr)
        return 0
    print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
