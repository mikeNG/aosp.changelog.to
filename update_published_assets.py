#!/usr/bin/env python3
"""Update asset references in already-published HTML pages.

New pages pick up their asset references from ``html_templates/header.html``
and ``html_templates/index_header.html``. Pages that were generated against the
old CDN URLs still reference the outdated libraries, so this script brings them
in line with the current templates.

Usage:
    ./update_published_assets.py [publish_dir]

``publish_dir`` defaults to the sibling ``gh-pages`` directory.
"""

import pathlib
import sys

PRECONNECT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
)
FONT_CSS = (
    '<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:'
    'opsz,wdth,wght@6..144,25..151,1..1000&display=swap" rel="stylesheet">'
)

BOOTSTRAP_CSS = (
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" '
    'rel="stylesheet" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" '
    'crossorigin="anonymous">'
)
JQUERY_JS = (
    '<script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js" '
    'integrity="sha384-1H217gwSVyLSIfaLxHbE7dRb3v4mYCKbpQvzx0cegeju1MVsGrX5xXxAvs/HgeFs" '
    'crossorigin="anonymous"></script>'
)
BOOTSTRAP_JS = (
    '<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js" '
    'integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" '
    'crossorigin="anonymous"></script>'
)

MARKER = "cdn.jsdelivr.net/npm/bootstrap@3.4.1"


def rewrite(text):
    """Return (new_text, was_changed)."""
    if MARKER in text:
        return text, False

    out = []
    changed = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]
        ending = "\n" if line.endswith("\n") else ""

        # Font Awesome is unused; drop the reference entirely.
        if "maxcdn.bootstrapcdn.com/font-awesome/" in stripped:
            changed = True
            continue

        if "bootstrapcdn.com/bootstrap/" in stripped and "bootstrap.min.css" in stripped:
            for link in PRECONNECT:
                out.append(indent + link + ending)
            out.append(indent + FONT_CSS + ending)
            out.append(indent + BOOTSTRAP_CSS + ending)
            changed = True
            continue

        if "ajax.googleapis.com/ajax/libs/jquery/" in stripped:
            out.append(indent + JQUERY_JS + ending)
            changed = True
            continue

        if "bootstrapcdn.com/bootstrap/" in stripped and "bootstrap.min.js" in stripped:
            out.append(indent + BOOTSTRAP_JS + ending)
            changed = True
            continue

        out.append(line)

    return "".join(out), changed


def main():
    if len(sys.argv) > 1:
        publish_dir = pathlib.Path(sys.argv[1])
    else:
        publish_dir = pathlib.Path(__file__).resolve().parent.parent / "gh-pages"

    if not publish_dir.is_dir():
        sys.exit(f"Publish directory not found: {publish_dir}")

    updated = 0
    for path in sorted(publish_dir.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new_text, changed = rewrite(text)
        if changed:
            path.write_text(new_text, encoding="utf-8")
            updated += 1

    print(f"Updated {updated} page(s) in {publish_dir}")


if __name__ == "__main__":
    main()
