#!/usr/bin/env python3
"""Update asset references and markup in already-published HTML pages.

New pages are generated from ``html_templates/header.html`` and
``html_templates/index_header.html``. Pages published before the front-end
dependencies were migrated still use Bootstrap 3 markup and the old CDN URLs,
so this script brings them in line with the current templates:

* swap the Bootstrap 3 CSS/JS (and the now unnecessary jQuery) for the
  Bootstrap 5 bundle,
* drop the unused Font Awesome reference,
* rewrite the Bootstrap 3 navbar to the Bootstrap 5 markup,
* rename the classes that were removed in Bootstrap 5.

Usage:
    ./update_published_assets.py [publish_dir]

``publish_dir`` defaults to the sibling ``gh-pages`` directory.
"""

import pathlib
import sys

BOOTSTRAP_CSS = (
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" '
    'rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" '
    'crossorigin="anonymous">'
)
BOOTSTRAP_JS = (
    '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" '
    'integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" '
    'crossorigin="anonymous"></script>'
)

OLD_NAVBAR = "navbar navbar-default navbar-fixed-top"
NEW_NAVBAR = """<nav class="navbar navbar-expand-lg bg-body-tertiary fixed-top">
  <div class="container">
    <a class="navbar-brand" href="./index.html">AOSP Changelogs</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar" aria-controls="mainNavbar" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNavbar">
      <ul class="navbar-nav me-auto"></ul>
    </div>
  </div>
</nav>
"""

CLASS_RENAMES = (
    ('class="container card"', 'class="container"'),
    ('class="text-muted"', 'class="text-body-secondary"'),
)

MARKER = "cdn.jsdelivr.net/npm/bootstrap@5.3.8"


def rewrite_head(text):
    """Swap the Bootstrap 3 head references for Bootstrap 5."""
    out = []
    changed = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]
        ending = "\n" if line.endswith("\n") else ""
        is_bootstrap = (
            "bootstrapcdn.com/bootstrap/" in stripped
            or "cdn.jsdelivr.net/npm/bootstrap@3" in stripped
        )

        if "font-awesome/" in stripped:
            changed = True
            continue

        if is_bootstrap and "bootstrap.min.css" in stripped:
            out.append(indent + BOOTSTRAP_CSS + ending)
            changed = True
            continue

        if stripped.startswith("<script") and "jquery" in stripped:
            changed = True
            continue

        if is_bootstrap and "bootstrap.min.js" in stripped:
            out.append(indent + BOOTSTRAP_JS + ending)
            changed = True
            continue

        out.append(line)

    return "".join(out), changed


def rewrite_navbar(text):
    """Replace the Bootstrap 3 navbar block with Bootstrap 5 markup."""
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    changed = False

    while i < len(lines):
        if OLD_NAVBAR in lines[i]:
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count("<div")
                depth -= lines[j].count("</div>")
                if depth <= 0 and "</div>" in lines[j]:
                    break
                j += 1
            out.append(NEW_NAVBAR)
            i = j + 1
            changed = True
            continue

        out.append(lines[i])
        i += 1

    return "".join(out), changed


def rewrite(text):
    if MARKER in text:
        return text, False

    changed = False
    text, did = rewrite_head(text)
    changed = changed or did
    text, did = rewrite_navbar(text)
    changed = changed or did

    for old, new in CLASS_RENAMES:
        if old in text:
            text = text.replace(old, new)
            changed = True

    return text, changed


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
