from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "posts_html"
ROUTES = (
    "aboutme",
    "Dynexit",
    "HAAC_ADA_2022_annyal_symposium",
    "FE-CTF2022",
    "TowardsFastPI",
    "PPIMCE",
    "HAAC_ISCA_demo_slide",
    "HAAC_DISCC",
    "Privit",
    "mixedGC",
    "MATLAB-halftone-dither",
    "MATLAB-image-rotation-interpolation",
    "Remote-SSH-to-WSL",
)


def main() -> None:
    documents = [OUTPUT_ROOT / route / "index.html" for route in ROUTES]
    missing_pages = [path.relative_to(ROOT) for path in documents if not path.is_file()]
    if missing_pages:
        raise RuntimeError(f"Missing generated pages: {missing_pages}")

    bad_tokens: list[tuple[Path, str]] = []
    missing_references: list[tuple[Path, str]] = []
    local_reference_count = 0

    for path in documents:
        source = path.read_text(encoding="utf-8")
        for token in ("{%", "{{", "layout:", "permalink:"):
            if token in source:
                bad_tokens.append((path.relative_to(ROOT), token))

        required_markup = (
            "<!DOCTYPE html>",
            '<article class="post-content">',
            'href="/stylesheet.css"',
            "<title>",
        )
        for markup in required_markup:
            if markup not in source:
                bad_tokens.append((path.relative_to(ROOT), markup))

        for reference in re.findall(r'(?:href|src)="([^"#?]*)', source):
            if not reference or reference.startswith(
                ("http://", "https://", "//", "#", "mailto:", "data:", "javascript:")
            ):
                continue
            local_reference_count += 1
            if reference.startswith("/"):
                target = ROOT / reference.lstrip("/")
            else:
                target = path.parent / reference
            if not target.exists() and not (target / "index.html").exists():
                missing_references.append((path.relative_to(ROOT), reference))

    if bad_tokens:
        raise RuntimeError(f"Unexpected page content: {bad_tokens}")
    if missing_references:
        raise RuntimeError(f"Missing local references: {missing_references}")

    remote_ssh = documents[-1].read_text(encoding="utf-8")
    if "办公室安装了" not in remote_ssh:
        raise RuntimeError("Chinese text did not survive UTF-8 conversion")

    print(f"Validated {len(documents)} generated pages and {local_reference_count} local references.")


if __name__ == "__main__":
    main()
