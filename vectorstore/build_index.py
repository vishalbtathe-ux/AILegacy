"""Minimal index builder: reads text files from datasets/raw and copies them to datasets/processed
This file is a placeholder for chunking + embedding pipeline.
"""
import os
from pathlib import Path

RAW = Path("datasets/raw")
PROC = Path("datasets/processed")


def build_index():
    PROC.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in RAW.glob("**/*.txt"):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        # basic cleanup
        txt = txt.replace('\r\n', '\n')
        out = PROC / p.name
        out.write_text(txt, encoding="utf-8")
        count += 1
    print(f"Processed {count} files from {RAW} to {PROC}")


if __name__ == "__main__":
    build_index()