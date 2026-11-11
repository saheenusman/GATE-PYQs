# GATE CS PYQ Solutions

Personal study repo: previous-year GATE CS questions, solved by topic.
Published as a mobile-friendly site (MkDocs Material + GitHub Pages).
Scope: the entire GATE CS syllabus, done one subject at a time (Programming & Data Structures first;
see the subject list below). Not just PDS.

## Layout
- `raw/<year>/` : source question paper + official answer key PDFs. Git-ignored. NEVER edit, never commit.
- `docs/<subject>/<topic>/<year>-set<n>-q<no>.md` : one file per question.
- `docs/assets/<year>/` : cropped figures and diagrams (committed).
- `scripts/build_index.py` : builds navigation pages from question frontmatter. These are GENERATED and
  git-ignored, never edit them by hand: `docs/index.md`, `docs/<subject>/index.md`,
  `docs/<subject>/<topic>/index.md`, `docs/by-year/`.
- `docs/out-of-syllabus.md` : hand-written note page (NOT generated) for old questions on topics the current
  syllabus no longer has (e.g. software engineering). Not in any subject or topic folder.
- `scripts/home_template.md` : the text of the home page. Edit this (not `docs/index.md`) to change it.

## Naming
- Subject folders and topic folders are kebab-case, taken from the subject list below.
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
Body, in this order. The format must render on BOTH GitHub and the MkDocs site, so use plain
Markdown plus HTML `<details>`, never MkDocs-only syntax such as `??? success` admonitions.
1. `# <title>` : same text as the frontmatter `title`.
2. `## Question` : the text, then the figure if any, then the options. Always visible.
3. Answer block: only the final answer.
   ```html
   <details class="success" markdown="1">
   <summary>Answer</summary>

   **B**

   </details>
   ```
4. Solution block, same shape with `class="info"` and `<summary>Solution</summary>`: step-by-step
   working, with a trace table or diagram where it helps, ending with a bold `**Key idea:**` line
   (one or two lines naming the concept tested).

Details-block rules:
- Keep a blank line after `</summary>` and before `</details>`, or GitHub will not render the Markdown inside.
- Do NOT indent the content. Code fences, tables and ` ```mermaid ` blocks sit at column 0.
- Keep `markdown="1"` (the site needs it) and the `class` (the site styles it; GitHub ignores it).
- Use bold labels, not headings, inside the blocks.
- Math: `$...$` and `$$...$$` (both GitHub and the site render these). Write set braces as
  `\lbrace` and `\rbrace`, never `\{` and `\}`: GitHub strips that backslash and the braces vanish.

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

## Subjects and topics
Subject folder, then its topic folders. Topic slugs are unique across the whole repo.
Each question goes in exactly one subject; if it spans topics use the main one and add `also: [..]`.

- `programming-and-data-structures` (PDS): c-basics-and-pointers, recursion, arrays,
  stacks-and-queues, linked-lists, trees, binary-search-trees, heaps, graphs
- `algorithms`: asymptotic-analysis, divide-and-conquer, sorting-and-searching, hashing,
  greedy, dynamic-programming, graph-algorithms, np-completeness
- `theory-of-computation`: finite-automata-and-regular-languages, context-free-languages-and-pda,
  decidability-and-turing-machines
- `compiler-design`: lexical-analysis, parsing, syntax-directed-translation,
  intermediate-code-and-optimization
- `operating-system`: processes-and-threads, cpu-scheduling, synchronization, deadlocks,
  memory-management, file-systems-and-io
- `databases`: er-and-relational-model, relational-algebra-and-sql, functional-dependencies-and-normalization,
  transactions-and-concurrency, indexing-and-file-organization
- `computer-networks`: layering-and-physical-layer, data-link-layer, ip-and-routing,
  transport-layer, application-layer
- `computer-organization`: machine-instructions-and-addressing, number-representation-and-alu,
  pipelining, cache-and-memory, io-and-storage
- `digital-logic`: boolean-algebra-and-minimization, combinational-circuits, sequential-circuits
- `discrete-mathematics`: logic, sets-relations-and-functions, combinatorics, graph-theory, algebraic-structures
- `linear-algebra`: matrices-and-determinants, systems-and-eigenvalues
- `calculus`: limits-and-continuity, differentiation-and-optimization, integration
- `probability-and-statistics`: probability-basics, random-variables-and-distributions
- `general-aptitude`: verbal, quantitative, analytical-and-spatial

Boundaries: graph representation questions stay in PDS `graphs`; graph algorithms (BFS/DFS, MST,
shortest paths), sorting, searching and hashing go to `algorithms`. Pure graph-theory facts (matchings,
colouring, vertex cover as a property) go to `discrete-mathematics/graph-theory`; an algorithmic
question about them goes to `algorithms`. Digital Logic, Computer Organization and Computer Networks
syllabi changed for GATE 2027; their topic lists may be adjusted, but ask first.

## Workflow per paper
1. Read the paper(s), list the questions of ONE subject with proposed topics, and wait for my OK.
2. Write the question files, run the code, compare with the key.
3. Rebuild indexes (`python scripts/build_index.py`), run `mkdocs build --strict`.
4. Commit on a branch named `pyq/<year>-<subject>`. One commit per topic. Don't merge.
5. Final message: counts, plus a list of disputed or unverified questions.

## Don't
- Don't modify `raw/`, and don't commit it.
- Don't change the template or topic list without asking.
- Don't push to `main` directly.
