#!/usr/bin/env python3
"""Validate profile assets and local README references without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class ReadmeImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "iframe"}:
            raise ValueError(f"Unsupported README element: {tag}")
        if tag == "img":
            if not attrs.get("alt"):
                raise ValueError("README image is missing alt text")
            self.references.append(attrs["src"])
        elif tag == "source":
            self.references.append(attrs["srcset"])


def validate():
    svgs = list((ROOT / "assets").rglob("*.svg"))
    for asset in svgs:
        source = asset.read_text(encoding="utf-8")
        element = ET.fromstring(source)
        if element.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError(f"Invalid SVG root: {asset}")
        for child in element.iter():
            if child.tag.split("}")[-1] == "script":
                raise ValueError(f"Script in SVG: {asset}")
            for name in child.attrib:
                if name.lower().startswith("on"):
                    raise ValueError(f"Event handler in SVG: {asset}")
        if "@keyframes" in source and "prefers-reduced-motion" not in source:
            raise ValueError(f"Animated asset lacks reduced-motion support: {asset}")
    parser = ReadmeImages()
    parser.feed((ROOT / "README.md").read_text(encoding="utf-8"))
    local = 0
    for reference in parser.references:
        if urlparse(reference).scheme:
            continue
        resolved = (ROOT / reference).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.is_file():
            raise ValueError(f"Broken or escaping local reference: {reference}")
        local += 1
    print(f"Validated {len(svgs)} SVGs and {local} local README image references.")


if __name__ == "__main__":
    validate()
