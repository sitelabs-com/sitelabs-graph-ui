#!/usr/bin/env python3
# Copyright 2026 Sitelabs.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The documents' menus and the documentation site's sidebar:

    python tools/docs.py            # write the menu at the top of every docs/*.md, and mkdocs.yml's nav
    python tools/docs.py --check    # change nothing; fail if a file is out of date (CI runs this)

Every document starts with the same menu: the sections (docs/sitedocs.py), then the pages of its own
section, from GROUPS. mkdocs.yml's nav is the same sections and pages, so the site's sidebar matches
the menus. A document in no section is an error, so a new one gets a place. The standard library only.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("sitedocs", ROOT / "docs" / "sitedocs.py")
sitedocs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sitedocs)

GROUPS = {
    "Features": [("features.md", "Features")],
    "Using the page": [("using.md", "Overview"), ("graph-views.md", "Graph views")],
    "Serving it": [("serving.md", "Overview"), ("server-contract.md", "Server contract"),
                   ("installing.md", "Installing into a project")],
    "Development": [("development.md", "Overview"), ("testing.md", "Tests"), ("graph-size.md", "How big a graph")],
    "Security": [("security.md", "Overview")],
    "References": [("index.md", "All documents")],
}


def build(root: str | Path = ROOT) -> dict[Path, str]:
    """Every file this tool writes, with what it should hold."""
    root = Path(root)
    docs = root / "docs"
    known = set(sitedocs.pages(GROUPS))
    missing = sorted(n for n in (p.relative_to(docs).as_posix() for p in docs.rglob("*.md")) if n not in known)
    if missing:
        raise SystemExit(f"in no section (tools/docs.py GROUPS): {', '.join(missing)}")
    out = {docs / name: sitedocs.with_menu((docs / name).read_text(), GROUPS, name, "../" * name.count("/"))
           for name in sorted(known)}
    out[root / "mkdocs.yml"] = sitedocs.with_nav((root / "mkdocs.yml").read_text(), GROUPS)   # the site's sidebar
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="change nothing; fail if a file is out of date")
    args = ap.parse_args()
    stale = []
    for path, text in build().items():
        if path.read_text() != text:
            stale.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(text)
    if args.check and stale:
        raise SystemExit("out of date (run python tools/docs.py): " + ", ".join(stale))
    print(("up to date" if not stale else ("would change: " if args.check else "wrote: ") + ", ".join(stale)))


if __name__ == "__main__":
    main()
