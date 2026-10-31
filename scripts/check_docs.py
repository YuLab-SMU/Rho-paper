#!/usr/bin/env python3
"""Check the project's local links, anchors, tables and containment, then render.

Local references are resolved against the file that contains them, so a reference
that only works from some other working directory fails here. External links are
listed but never fetched: their content belongs to other owners and changes without
notice, so a live result would not stay true.

Writes work/render/ (gitignored) and exits nonzero when anything fails.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import markdown
    from bs4 import BeautifulSoup
except ImportError as error:  # pragma: no cover - reported to the caller
    print(f"missing dependency: {error}. install markdown and beautifulsoup4", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "render"
CSS = """body{margin:0;background:#fff;color:#202124;font:18px/1.72 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;}
main{max-width:1120px;margin:0 auto;padding:40px 48px 70px;}h1{font-size:30px;line-height:1.4}
h2{font-size:25px;margin-top:1.6em}h3{font-size:21px;margin-top:1.4em}
a{color:#14559d;text-decoration:none;overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%;font-size:15.5px;line-height:1.6;margin:20px 0;}
th,td{border:1px solid #cbd3db;text-align:left;vertical-align:top;padding:10px 12px;overflow-wrap:normal}
th{background:#eef2f6}blockquote{border-left:4px solid #71869d;margin:24px 0;padding:8px 20px;background:#f5f7fa}
code{font-size:.92em;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#f5f7fa;padding:16px}"""


def documents() -> list[Path]:
    found = [ROOT / "README.md", ROOT / "AGENTS.md", *sorted((ROOT / "docs").glob("*.md"))]
    return [path for path in found if path.is_file()]


def render(path: Path) -> BeautifulSoup:
    html = markdown.markdown(path.read_text(encoding="utf-8"), extensions=["tables", "fenced_code", "toc"])
    return BeautifulSoup(html, "html.parser")


def anchors(path: Path) -> set[str]:
    """Identifiers GitHub produces for a page: heading slugs plus explicit ids."""

    ids: set[str] = set()
    used: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not heading:
            continue
        text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading.group(1)).lower()
        slug = re.sub(r"[^\w\- ]", "", text).replace(" ", "-")
        seen = used.get(slug, 0)
        ids.add(f"{slug}-{seen}" if seen else slug)
        used[slug] = seen + 1
    ids.update(node["id"] for node in render(path).find_all(id=True))
    return ids


def check(path: Path, cache: dict[Path, set[str]]) -> dict:
    errors: list[str] = []
    soup = render(path)
    relative: list[dict] = []
    external: set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            external.add(href)
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        entry = {"href": href, "ok": True}
        if not target.is_relative_to(ROOT):
            entry["ok"] = False
            errors.append(f"{path.name}: {href} leaves the project")
        elif not target.exists():
            entry["ok"] = False
            errors.append(f"{path.name}: {href} does not exist")
        elif parts.fragment and target.suffix == ".md":
            known = cache.setdefault(target, anchors(target))
            if unquote(parts.fragment) not in known:
                entry["ok"] = False
                errors.append(f"{path.name}: {href} has no anchor {unquote(parts.fragment)}")
        relative.append(entry)

    tables = []
    for index, table in enumerate(soup.find_all("table"), 1):
        widths = {len(row.find_all(["th", "td"], recursive=False)) for row in table.find_all("tr")}
        tables.append({"table": index, "columns": sorted(widths)})
        if len(widths) != 1:
            errors.append(f"{path.name}: table {index} has uneven rows {sorted(widths)}")

    OUT.mkdir(parents=True, exist_ok=True)
    target_html = OUT / f"{path.stem}.html"
    target_html.write_text(
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        f"<title>{path.stem}</title><style>{CSS}</style><main>{soup}</main></html>",
        encoding="utf-8",
    )

    source = path.read_text(encoding="utf-8")
    return {
        "file": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(source.encode()).hexdigest(),
        "lines": len(source.splitlines()),
        "rendered": str(target_html.relative_to(ROOT)),
        "local_links": relative,
        "external_links": sorted(external),
        "tables": tables,
        "errors": errors,
    }


def main() -> int:
    cache: dict[Path, set[str]] = {}
    reports = [check(path, cache) for path in documents()]
    errors = [error for report in reports for error in report["errors"]]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "link-report.json").write_text(
        json.dumps({"documents": reports, "errors": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    summary = [
        {
            "file": report["file"],
            "lines": report["lines"],
            "local_links": len(report["local_links"]),
            "external_links": len(report["external_links"]),
            "tables": len(report["tables"]),
            "errors": len(report["errors"]),
        }
        for report in reports
    ]
    print(json.dumps({"documents": summary, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
