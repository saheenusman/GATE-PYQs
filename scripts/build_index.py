#!/usr/bin/env python3
"""Generate navigation pages from question-file frontmatter.

Run from the repo root:  python scripts/build_index.py

Generated (git-ignored, never edit by hand):
  docs/index.md                       home page, from scripts/home_template.md
  docs/<subject>/index.md             subject page with topic counts
  docs/<subject>/<topic>/index.md     topic page listing its questions
  docs/by-year/                       year pages and the "needs attention" list
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BY_YEAR = DOCS / "by-year"
TEMPLATE = ROOT / "scripts" / "home_template.md"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)

SUBJECT_NAMES = {
    "programming-and-data-structures": "Programming & Data Structures",
    "algorithms": "Algorithms",
    "theory-of-computation": "Theory of Computation",
    "compiler-design": "Compiler Design",
    "operating-system": "Operating System",
    "databases": "Databases",
    "computer-networks": "Computer Networks",
    "computer-organization": "Computer Organization",
    "digital-logic": "Digital Logic",
    "discrete-mathematics": "Discrete Mathematics",
    "linear-algebra": "Linear Algebra",
    "calculus": "Calculus",
    "probability-and-statistics": "Probability & Statistics",
    "general-aptitude": "General Aptitude",
}
SUBJECT_ORDER = list(SUBJECT_NAMES)  # syllabus order on the home page
TOPIC_ORDER = [
    # programming-and-data-structures
    "c-basics-and-pointers", "recursion", "arrays", "stacks-and-queues",
    "linked-lists", "trees", "binary-search-trees", "heaps", "graphs",
    # algorithms
    "asymptotic-analysis", "divide-and-conquer", "sorting-and-searching", "hashing",
    "greedy", "dynamic-programming", "graph-algorithms", "np-completeness",
    # theory-of-computation
    "finite-automata-and-regular-languages", "context-free-languages-and-pda",
    "decidability-and-turing-machines",
    # compiler-design
    "lexical-analysis", "parsing", "syntax-directed-translation", "intermediate-code-and-optimization",
    # operating-system
    "processes-and-threads", "cpu-scheduling", "synchronization", "deadlocks",
    "memory-management", "file-systems-and-io",
    # databases
    "er-and-relational-model", "relational-algebra-and-sql",
    "functional-dependencies-and-normalization", "transactions-and-concurrency",
    "indexing-and-file-organization",
    # computer-networks
    "layering-and-physical-layer", "data-link-layer", "ip-and-routing",
    "transport-layer", "application-layer",
    # computer-organization
    "machine-instructions-and-addressing", "number-representation-and-alu",
    "pipelining", "cache-and-memory", "io-and-storage",
    # digital-logic
    "boolean-algebra-and-minimization", "combinational-circuits", "sequential-circuits",
    # discrete-mathematics
    "logic", "sets-relations-and-functions", "combinatorics", "graph-theory", "algebraic-structures",
    # linear-algebra, calculus, probability-and-statistics
    "matrices-and-determinants", "systems-and-eigenvalues",
    "limits-and-continuity", "differentiation-and-optimization", "integration",
    "probability-basics", "random-variables-and-distributions",
    # general-aptitude
    "verbal", "quantitative", "analytical-and-spatial",
]


def subject_sort_key(slug: str) -> tuple[int, str]:
    return (SUBJECT_ORDER.index(slug), slug) if slug in SUBJECT_ORDER else (len(SUBJECT_ORDER), slug)


def subject_name(slug: str) -> str:
    return SUBJECT_NAMES.get(slug, slug.replace("-", " ").title())


def topic_name(slug: str) -> str:
    return slug.replace("-", " ").capitalize()


def topic_sort_key(slug: str) -> tuple[int, str]:
    return (TOPIC_ORDER.index(slug), slug) if slug in TOPIC_ORDER else (len(TOPIC_ORDER), slug)


def question_sort_key(q: dict) -> tuple[int, int, int]:
    return (-int(q["year"]), int(q.get("set", 1)), int(q["q_no"]))


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
        meta["_file"] = rel.name
        questions.append(meta)
    return questions


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_topic_pages(grouped: dict[str, dict[str, list[dict]]]) -> None:
    for subject, topics in grouped.items():
        for topic, qs in topics.items():
            lines = [
                f"# {topic_name(topic)}",
                "",
                f"{plural(len(qs), 'question')} in {subject_name(subject)}.",
                "",
                "| Question | Year | Marks | Type | Status |",
                "|---|---|---|---|---|",
            ]
            for q in sorted(qs, key=question_sort_key):
                title = q.get("title") or f"{q['year']} {q.get('paper', '')} Q{q['q_no']}"
                lines.append(
                    f"| [{title}]({q['_file']}) | {q['year']} | {q.get('marks', '')} "
                    f"| {q.get('type', '')} | {q.get('status', '')} |"
                )
            write(DOCS / subject / topic / "index.md", "\n".join(lines) + "\n")


def build_subject_pages(grouped: dict[str, dict[str, list[dict]]]) -> None:
    for subject, topics in grouped.items():
        total = sum(len(v) for v in topics.values())
        lines = [
            f"# {subject_name(subject)}",
            "",
            f"{plural(total, 'question')} across {plural(len(topics), 'topic')}.",
            "",
            "| Topic | Questions |",
            "|---|---|",
        ]
        for topic in sorted(topics, key=topic_sort_key):
            lines.append(f"| [{topic_name(topic)}]({topic}/index.md) | {len(topics[topic])} |")
        write(DOCS / subject / "index.md", "\n".join(lines) + "\n")


def build_home(questions: list[dict], grouped: dict[str, dict[str, list[dict]]]) -> None:
    years = sorted({int(q["year"]) for q in questions}, reverse=True)
    if questions:
        summary = (
            f"**{len(questions)}** solved questions from GATE "
            + ", ".join(str(y) for y in years) + "."
        )
    else:
        summary = "No questions yet."
    blocks = []
    for subject, topics in grouped.items():
        blocks += [
            f"### [{subject_name(subject)}]({subject}/index.md)",
            "",
            "| Topic | Questions |",
            "|---|---|",
        ]
        for topic in sorted(topics, key=topic_sort_key):
            blocks.append(f"| [{topic_name(topic)}]({subject}/{topic}/index.md) | {len(topics[topic])} |")
        blocks.append("")
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("{{SUMMARY}}", summary).replace("{{TOPICS}}", "\n".join(blocks).strip())
    write(DOCS / "index.md", text)


def build_by_year(questions: list[dict]) -> None:
    by_year: dict[int, list[dict]] = defaultdict(list)
    for q in questions:
        by_year[int(q["year"])].append(q)

    def link(q: dict) -> str:
        return "../" + q["_path"]

    header = "| Question | Subject | Topic | Type | Marks | Status |\n|---|---|---|---|---|---|"
    for year, qs in by_year.items():
        lines = [f"# GATE {year}", ""]
        by_set: dict[int, list[dict]] = defaultdict(list)
        for q in qs:
            by_set[int(q.get("set", 1))].append(q)
        for s in sorted(by_set):
            paper = by_set[s][0].get("paper", f"Set {s}")
            lines += [f"## {paper}", "", header]
            for q in sorted(by_set[s], key=lambda x: int(x["q_no"])):
                lines.append(
                    f"| [Q{q['q_no']}]({link(q)}) | {subject_name(q.get('subject', ''))} "
                    f"| {topic_name(q.get('topic', ''))} | {q.get('type', '')} "
                    f"| {q.get('marks', '')} | {q.get('status', '')} |"
                )
            lines.append("")
        write(BY_YEAR / f"{year}.md", "\n".join(lines))

    idx = ["# By year", ""]
    if by_year:
        for year in sorted(by_year, reverse=True):
            idx.append(f"- [GATE {year}]({year}.md): {plural(len(by_year[year]), 'question')}")
    else:
        idx.append("No questions yet.")
    flagged = [q for q in questions if q.get("status") != "verified"]
    if flagged:
        idx += ["", "## Needs attention", "", "| Question | Year | Status |", "|---|---|---|"]
        for q in sorted(flagged, key=question_sort_key):
            idx.append(
                f"| [{q['year']} {q.get('paper', '')} Q{q['q_no']}]({link(q)}) "
                f"| {q['year']} | {q.get('status', '')} |"
            )
    write(BY_YEAR / "index.md", "\n".join(idx) + "\n")


def build_nav(grouped: dict[str, dict[str, list[dict]]], questions: list[dict]) -> None:
    """Write .nav.yml files (mkdocs-awesome-nav) so the sidebar follows our order, not the alphabet:
    Home, By year, then subjects in syllabus order, topics in TOPIC_ORDER, questions by year/set/number."""
    def q(text: str) -> str:
        return '"' + text.replace('"', '\\"') + '"'

    top = ["nav:", "  - index.md", "  - " + q("By year") + ": by-year"]
    for subject in grouped:
        top.append(f"  - {q(subject_name(subject))}: {subject}")
    write(DOCS / ".nav.yml", "\n".join(top) + "\n")

    for subject, topics in grouped.items():
        lines = ["nav:", "  - index.md"]
        for topic in sorted(topics, key=topic_sort_key):
            lines.append(f"  - {q(topic_name(topic))}: {topic}")
        write(DOCS / subject / ".nav.yml", "\n".join(lines) + "\n")
        for topic, qs in topics.items():
            lines = ["nav:", "  - index.md"]
            lines += [f"  - {q_['_file']}" for q_ in sorted(qs, key=question_sort_key)]
            write(DOCS / subject / topic / ".nav.yml", "\n".join(lines) + "\n")

    years = sorted({int(x["year"]) for x in questions}, reverse=True)
    lines = ["nav:", "  - index.md"] + [f"  - {y}.md" for y in years]
    write(BY_YEAR / ".nav.yml", "\n".join(lines) + "\n")


def main() -> int:
    questions = load_questions()
    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for q in questions:
        grouped[q.get("subject", "other")][q.get("topic", "other")].append(q)

    grouped = {k: grouped[k] for k in sorted(grouped, key=subject_sort_key)}
    build_topic_pages(grouped)
    build_subject_pages(grouped)
    build_home(questions, grouped)
    build_by_year(questions)
    build_nav(grouped, questions)
    topics = sum(len(t) for t in grouped.values())
    print(f"Indexed {len(questions)} questions, {topics} topic page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
