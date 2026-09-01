from __future__ import annotations

import html
import re
import sys
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "posts_html"
sys.path.insert(0, str(ROOT / ".tmp" / "markdown-lib"))

import markdown  # noqa: E402
import yaml  # noqa: E402


SPECIAL_ROUTES = {
    "2020-08-09-about.md": "aboutme",
    "_2021-05-29-Remote SSH to WSL.md": "Remote-SSH-to-WSL",
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def split_front_matter(source: str) -> tuple[dict, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", source, re.DOTALL)
    if not match:
        return {}, source
    return yaml.safe_load(match.group(1)) or {}, source[match.end() :]


def route_for(path: Path, metadata: dict) -> str:
    permalink = str(metadata.get("permalink", "")).strip(" /")
    if permalink:
        return permalink
    if path.name in SPECIAL_ROUTES:
        return SPECIAL_ROUTES[path.name]
    if "halftone" in path.name.lower():
        return "MATLAB-halftone-dither"
    if "MSE" in path.name:
        return "MATLAB-image-rotation-interpolation"
    stem = path.stem.lstrip("_")
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


def title_for(path: Path, metadata: dict) -> str:
    if metadata.get("title"):
        return str(metadata["title"])
    if path.name == "_2021-05-29-Remote SSH to WSL.md":
        return "Remote SSH to WSL"
    return route_for(path, metadata).replace("-", " ").replace("_", " ")


def date_for(path: Path, metadata: dict) -> tuple[str, str]:
    value = metadata.get("date")
    if isinstance(value, (date, datetime)):
        parsed = value
    else:
        raw = str(value or "")[:10]
        if not raw:
            match = re.search(r"\d{4}-\d{2}-\d{2}", path.name)
            raw = match.group(0) if match else ""
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            return "", ""
    return parsed.strftime("%Y-%m-%d"), parsed.strftime("%B %d, %Y").replace(" 0", " ")


def preprocess(body: str) -> str:
    replacements = {
        "{{ site.footer-links.github }}": "jianqiaomo",
        "{{ site.footer-links.linkedin }}": "jianqiao-cambridge-mo",
        "{{ site.footer-links.googlescholar }}": "rydgKnMAAAAJ",
        "jqmo@nyu,edu": "jqmo@nyu.edu",
    }
    body = re.sub(r"^\{%\s*include\s+aboutme\.md\s*%\}\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^@\s*\[TOC\]\([^)]+\)\s*$", "", body, flags=re.MULTILINE)
    for old, new in replacements.items():
        body = body.replace(old, new)
    return re.sub(r"(?<![A-Za-z0-9/])==([^=\n]+)==(?!/)", r"<mark>\1</mark>", body)


def description_from(rendered: str, title: str) -> str:
    parser = TextExtractor()
    parser.feed(rendered)
    text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
    return (text or title)[:180]


def render_page(path: Path) -> tuple[str, Path]:
    source = path.read_text(encoding="utf-8-sig")
    metadata, body = split_front_matter(source)
    route = route_for(path, metadata)
    title = title_for(path, metadata)
    iso_date, display_date = date_for(path, metadata)
    body = preprocess(body)
    rendered = markdown.markdown(
        body,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    description = description_from(rendered, title)
    language = "zh-CN" if re.search(r"[\u3400-\u9fff]", title + body) else "en"
    canonical = f"https://jqmo.top/posts_html/{route}/"
    date_markup = (
        f'<time datetime="{html.escape(iso_date)}">{html.escape(display_date)}</time>'
        if iso_date
        else ""
    )
    document = f'''<!DOCTYPE html>
<html lang="{language}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | Jianqiao Mo</title>
  <meta name="author" content="Jianqiao Mo">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
  <link rel="stylesheet" href="/stylesheet.css">
  <link rel="icon" type="image/png" href="/images/favicon.png">
</head>
<body>
  <!-- Generated from {html.escape(path.relative_to(ROOT).as_posix())} by scripts/build_posts.py. -->
  <main class="post-page">
    <nav class="post-nav" aria-label="Post navigation">
      <a href="/">Jianqiao Mo</a>
      <span aria-hidden="true">/</span>
      <a href="/#activities">Activities</a>
    </nav>
    <header class="post-header">
      <h1>{html.escape(title)}</h1>
      <p class="post-meta">{date_markup}</p>
    </header>
    <article class="post-content">
{rendered}
    </article>
    <footer class="post-footer">
      <a href="/">Back to Home</a>
    </footer>
  </main>
</body>
</html>
'''
    destination = OUTPUT_ROOT / route / "index.html"
    return document, destination


def main() -> None:
    sources = sorted((ROOT / "_posts").glob("*.md"), key=lambda item: item.name)
    if len(sources) != 13:
        raise RuntimeError(f"Expected 13 Markdown posts, found {len(sources)}")
    generated: list[Path] = []
    for source in sources:
        document, destination = render_page(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(document, encoding="utf-8", newline="\n")
        generated.append(destination.relative_to(ROOT))
    print("\n".join(path.as_posix() for path in generated))


if __name__ == "__main__":
    main()
