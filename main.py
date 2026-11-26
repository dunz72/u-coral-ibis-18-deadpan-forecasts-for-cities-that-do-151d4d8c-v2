#!/usr/bin/env python3
"""Copy the deadpan forecast from entry.txt to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only: the grader image has no third-party libraries, so this
program imports nothing beyond the standard library.

The copy is verified byte-identical (SHA-256) before exiting, and the
text is checked against the competition gate: UTF-8, 1 to 160
characters, not only whitespace.
"""

import hashlib
import os
import sys


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_entry(src_path: str) -> tuple[str, bytes]:
    with open(src_path, "rb") as f:
        data = f.read()
    return data.decode("utf-8"), data


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.txt")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst_path = os.path.join(out_dir, "entry.txt")

    text, data = load_entry(src_path)
    if not text.strip():
        print("error: entry.txt is empty or whitespace only", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 160:
        print(f"error: entry text is {len(text)} characters, must be 1-160",
              file=sys.stderr)
        return 1
    if text != text.rstrip("\n") or "\n" in text.rstrip("\n"):
        print("error: entry.txt must be a single line with no trailing newline",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dst_path, "wb") as f:
        f.write(data)

    with open(dst_path, "rb") as f:
        copied = f.read()
    if copied != data:
        print("error: copied entry.txt does not match the source",
              file=sys.stderr)
        return 1

    print(f"copied entry.txt ({len(data)} bytes, "
          f"sha256 {sha256_hex(data)}) to {dst_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
