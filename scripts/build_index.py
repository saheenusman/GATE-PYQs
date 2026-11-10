#!/usr/bin/env python3
"""Build docs/by-year/ from question-file frontmatter.

Run from the repo root:  python scripts/build_index.py
The by-year folder is generated and git-ignored.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "by-year"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def load_questions() -> list[dict]:
    questions = []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        if rel.parts[0] == "by-year" or rel.name == "index.md" or len(rel.parts) < 3:
            continue
        m = FM.match(path.read_text(encoding="utf-8"))
        if not m:
            continue
        meta = yaml.safe_load(m.group(1)) or {}
        if "year" not in meta or "q_no" not in meta:
            continue
        meta["_path"] = rel.as_posix()
        questions.append(meta)
    return questions


def link(meta: dict) -> str:
    return "../" + meta["_path"]


def row(meta: dict) -> str:
    title = f"Q{meta['q_no']}"
    return (
        f"| [{title}]({link(meta)}) | {meta.get('subject', '')} | {meta.get('topic', '')} "
        f"| {meta.get('type', '')} | {meta.get('marks', '')} | {meta.get('status', '')} |"
    )


def main() -> int:
    questions = load_questions()
    OUT.mkdir(parents=True, exist_ok=True)
    by_year: dict[int, list[dict]] = defaultdict(list)
    for q in questions:
        by_year[int(q["year"])].append(q)

    header = "| Question | Subject | Topic | Type | Marks | Status |\n|---|---|---|---|---|---|"
    for year, qs in by_year.items():
        lines = [f"# GATE {year}", ""]
        by_set: dict[int, list[dict]] = defaultdict(list)
        for q in qs:
            by_set[int(q.get("set", 1))].append(q)
        for s in sorted(by_set):
            paper = by_set[s][0].get("paper", f"Set {s}")
            lines += [f"## {paper}", "", header]
            lines += [row(q) for q in sorted(by_set[s], key=lambda x: int(x["q_no"]))]
            lines.append("")
        (OUT / f"{year}.md").write_text("\n".join(lines), encoding="utf-8")

    idx = ["# By year", ""]
    if by_year:
        for year in sorted(by_year, reverse=True):
            idx.append(f"- [GATE {year}]({year}.md): {len(by_year[year])} questions")
    else:
        idx.append("No questions yet.")
    flagged = [q for q in questions if q.get("status") != "verified"]
    if flagged:
        idx += ["", "## Needs attention", "", "| Question | Year | Status |", "|---|---|---|"]
        for q in sorted(flagged, key=lambda x: (int(x["year"]), int(x.get("set", 1)), int(x["q_no"]))):
            idx.append(f"| [{q['year']} {q.get('paper', '')} Q{q['q_no']}]({link(q)}) | {q['year']} | {q.get('status', '')} |")
    (OUT / "index.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"Indexed {len(questions)} questions across {len(by_year)} year(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
