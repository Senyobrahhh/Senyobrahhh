#!/usr/bin/env python3
"""Recolor a real Platane contribution SVG and add reduced-motion support.

Only presentation changes. Contribution cells, dates and animation paths stay intact.
Usage: python3 scripts/prepare_snake.py INPUT.svg OUTPUT.svg [--static]
"""
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

COLORS = {
    "cb": "#263E50", "cs": "#DCECF1", "ce": "#101E2D",
    "c0": "#101E2D", "c1": "#274555", "c2": "#446D80",
    "c3": "#6797A9", "c4": "#8CC8D8",
}
MOTION = "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"


def prepare(source):
    ET.fromstring(source)
    for name, value in COLORS.items():
        source, count = re.subn(rf"(--{name}:)[^;}}]+", lambda m: m[1]+value, source)
        if count != 1:
            raise ValueError(f"Expected one --{name} color variable; found {count}")
    if MOTION not in source:
        if "</style>" not in source:
            raise ValueError("Snake SVG has no style element")
        source = source.replace("</style>", MOTION+"</style>", 1)
    ET.fromstring(source)
    return source


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4) or (len(sys.argv) == 4 and sys.argv[3] != "--static"):
        raise SystemExit("Usage: prepare_snake.py INPUT.svg OUTPUT.svg [--static]")
    source, target = map(Path, sys.argv[1:3])
    target.parent.mkdir(parents=True, exist_ok=True)
    result = prepare(source.read_text(encoding="utf-8"))
    if len(sys.argv) == 4:
        result = result.replace("</style>", "*{animation:none!important}</style>", 1)
    target.write_text(result, encoding="utf-8")
