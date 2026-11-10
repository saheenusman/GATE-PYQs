# GATE CS PYQ Solutions

Personal study repo: previous-year GATE CS questions, solved by topic.
Published as a mobile-friendly site (MkDocs Material + GitHub Pages).
Current scope: Programming & Data Structures (PDS). Other subjects come later.

## Layout
- `raw/<year>/` : source question paper + official answer key PDFs. Git-ignored. NEVER edit, never commit.
- `docs/<subject>/<topic>/<year>-set<n>-q<no>.md` : one file per question.
- `docs/assets/<year>/` : cropped figures and diagrams (committed).
- `scripts/build_index.py` : builds `docs/by-year/` from frontmatter. That folder is GENERATED and git-ignored. Never edit it by hand.

## Naming
- Subject folder: `programming-and-data-structures`. Topic folders are kebab-case (see topic list).
- File: `<year>-set<n>-q<no>.md`, for example `2026-set1-q41.md`.
- Frontmatter `paper` records the official paper name (for 2026: `CS1` = set1, FN, session 3; `CS2` = set2, AN, session 4).
- Figures: `docs/assets/<year>/set<n>-q<no>[-a|-b].png`.

## Question file template
Frontmatter:
```yaml
---
title: "2026 CS1 Q41"
year: 2026
set: 1
paper: CS1
q_no: 41
subject: programming-and-data-structures
topic: trees
also: []            # extra topics if the question spans more than one
marks: 2
type: MCQ           # MCQ | MSQ | NAT
official_answer: "B"
status: verified    # verified | disputed | unverified
---
```
Body, in this order:
1. `## Question` : the text, then the figure if any, then the options. Always visible.
2. `??? success "Answer"` : collapsible block with only the final answer.
3. `??? info "Solution"` : separate collapsible block: step-by-step working, with a trace table or
   diagram where it helps, ending with a bold `**Key idea:**` line (one or two lines naming the concept tested).
   Content inside a collapsible block is indented 4 spaces (including code and mermaid fences).
   Use bold labels, not headings, inside collapsibles.

## Rules
1. **Official key is the reference.** Compare every answer with the official key.
   If my solution disagrees, set `status: disputed`, explain both, and do NOT silently pick one.
2. **Run the code.** For every C snippet or NAT question, compile and run it
   (`gcc -Wall`) and confirm the output. Note any undefined or
   implementation-defined behavior explicitly.
3. **No guessing.** If a question or figure is unreadable in the PDF, flag it, don't invent it.
4. **Classify carefully.** Pick the topic from the list below. If a question
   spans topics, use the main one and add `also: [..]`.
5. **Diagrams:** crop figures from the PDF at 2x into `docs/assets/`. For trees, graphs
   and heaps, also redraw as Mermaid or SVG when it makes the solution clearer.
   Always add alt text.
6. **Mobile-first writing:** short lines, small tables, no wide code blocks, no
   huge files. Math in LaTeX (`$...$`).
7. **Solutions teach.** For MCQ/MSQ, say why each wrong option is wrong. Keep it concise, no filler.
8. **Status honesty.** Mark `verified` only if the code ran (where applicable) and the answer matches the official key.

## PDS topics
c-basics-and-pointers, recursion, arrays, stacks-and-queues, linked-lists,
trees, binary-search-trees, heaps, graphs

Boundaries: graph algorithms (BFS/DFS, MST, shortest paths), sorting, searching
and hashing belong to Algorithms (later). Use `graphs` here only for graph
representation questions.

## Workflow per paper
1. Read the paper, list the PDS questions with proposed topics, and wait for my OK.
2. Write the question files, run the code, compare with the key.
3. Rebuild indexes (`python scripts/build_index.py`), run `mkdocs build --strict`.
4. Commit on a branch named `pyq/<year>`. One commit per topic. Don't merge.
5. Final message: counts, plus a list of disputed or unverified questions.

## Don't
- Don't modify `raw/`, and don't commit it.
- Don't change the template or topic list without asking.
- Don't push to `main` directly.
