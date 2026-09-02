#!/usr/bin/env python3
"""Generate a sitemap for the static HTML files in this repository."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree


SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def page_url(base_url: str, relative_path: Path) -> str:
    if relative_path.name == "index.html":
        parent = relative_path.parent.as_posix()
        url_path = "/" if parent == "." else f"/{quote(parent, safe='/')}/"
    else:
        url_path = f"/{quote(relative_path.as_posix(), safe='/')}"
    return f"{base_url.rstrip('/')}{url_path}"


def git_last_modified(source_root: Path, relative_path: Path) -> str | None:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(source_root),
            "log",
            "-1",
            "--format=%cs",
            "--",
            relative_path.as_posix(),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    date = result.stdout.strip()
    return date or None


def generate_sitemap(
    site_root: Path,
    source_root: Path,
    output: Path,
    base_url: str,
) -> int:
    pages = sorted(
        path
        for path in site_root.rglob("*.html")
        if path.is_file() and path.name.lower() != "404.html"
    )

    ElementTree.register_namespace("", SITEMAP_NAMESPACE)
    urlset = ElementTree.Element(f"{{{SITEMAP_NAMESPACE}}}urlset")

    for page in pages:
        relative_path = page.relative_to(site_root)
        url = ElementTree.SubElement(urlset, f"{{{SITEMAP_NAMESPACE}}}url")
        ElementTree.SubElement(url, f"{{{SITEMAP_NAMESPACE}}}loc").text = page_url(
            base_url, relative_path
        )
        last_modified = git_last_modified(source_root, relative_path)
        if last_modified:
            ElementTree.SubElement(
                url, f"{{{SITEMAP_NAMESPACE}}}lastmod"
            ).text = last_modified

    ElementTree.indent(urlset, space="  ")
    output.parent.mkdir(parents=True, exist_ok=True)
    ElementTree.ElementTree(urlset).write(
        output, encoding="utf-8", xml_declaration=True
    )
    return len(pages)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    site_root = args.site_root.resolve()
    source_root = args.source_root.resolve()
    output = args.output.resolve() if args.output else site_root / "sitemap.xml"
    page_count = generate_sitemap(site_root, source_root, output, args.base_url)
    print(f"Generated {output} with {page_count} URLs")


if __name__ == "__main__":
    main()
