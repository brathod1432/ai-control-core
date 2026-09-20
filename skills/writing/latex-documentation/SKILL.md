---
name: latex-documentation
description: Prepare, edit, format, and validate professional LaTeX reports, technical documentation, academic-style papers, manuals, and formal PDFs. Use when the user asks for LaTeX, TeX, .tex, report templates, title pages, tables of contents, indexes, headings, references, citations, bibliographies, headers, footers, page layout, appendices, figures, tables, equations, cross-references, or PDF build troubleshooting.
license: MIT
metadata:
  version: 1.0.0
  category: writing
  domain: latex-documentation
  updated: 2026-05-01
  frameworks: latexmk, xelatex, biblatex, hyperref, cleveref, fancyhdr, glossaries, imakeidx
---

## Internal Safety Override

- Status: local-only unless explicitly opted into external access.
- Before using network tools, package managers, account connectors, browser automation, or remote APIs, state the destination, data scope, and reason, then wait for explicit user approval.
- Do not upload source files, PDFs, logs, bibliography data, document text, project metadata, secrets, or private assets to external services by default.
- Do not install TeX packages, enable `--shell-escape`, run arbitrary Makefiles, or execute generated scripts unless the user explicitly approves that specific action.
- Do not edit files outside the active workspace unless the user explicitly approves the target path.
- Preserve user changes. Make focused edits and do not perform destructive cleanup, broad rewrites, git resets, or forced checkouts.
- Audit categories: filesystem, command-execution, network, package-install, secrets, document-content.

# LaTeX Documentation

This skill creates and improves professional LaTeX deliverables: reports, technical documentation, formal specifications, manuals, white papers, research notes, and polished PDFs with strong structure, references, typography, and navigation.

## Use This Skill For

- Creating a complete LaTeX report or documentation project.
- Converting outlines, Markdown, notes, or plain text into LaTeX.
- Designing title pages, document metadata, headers, footers, page numbering, margins, and section hierarchy.
- Adding tables of contents, lists of figures/tables, indexes, glossaries, appendices, and acronyms.
- Managing citations, bibliographies, footnotes, cross-references, labels, and hyperlinks.
- Formatting professional tables, figures, code listings, equations, diagrams, callouts, and appendices.
- Troubleshooting LaTeX build errors, warnings, overfull boxes, missing references, missing citations, and layout issues.

## Do Not Use This Skill For

- Word `.docx` editing unless the user specifically wants LaTeX output.
- PowerPoint or slide deck generation unless the user wants Beamer or LaTeX source.
- Remote collaborative editors such as Overleaf unless the user explicitly approves external access.
- Installing or updating TeX distributions without explicit approval.

## Default Workflow

1. **Scope the document**
   - Identify document type: report, manual, specification, paper, thesis chapter, proposal, policy, or appendix pack.
   - Confirm audience, required sections, branding constraints, citation style, page size, language, and output target.
   - If details are missing and the task is safe, choose conservative defaults: A4 paper, 11 pt, `scrreprt`, `xelatex`, `biblatex`, numbered headings, `hyperref`, `cleveref`, `fancyhdr`, and a table of contents.

2. **Inspect existing files**
   - Read current `.tex`, `.bib`, image, and build files before changing anything.
   - Check whether the project already uses `latexmk`, `pdflatex`, `xelatex`, `lualatex`, `bibtex`, `biber`, `biblatex`, or `natbib`.
   - Follow the existing class, package, naming, folder, and build conventions when they are reasonable.

3. **Plan the document architecture**
   - For new projects, start from `templates/professional-report-template.tex`.
   - Use stable structure: title matter, abstract or executive summary, table of contents, body sections, conclusion, bibliography, appendices, glossary/index if needed.
   - Split large reports into included chapter files only when it improves maintainability.
   - Use `\label{}` and `\cref{}` consistently for sections, figures, tables, equations, and appendices.

4. **Implement formatting**
   - Use semantic LaTeX: `\chapter`, `\section`, `\subsection`, `table`, `figure`, `description`, `enumerate`, `itemize`, `quote`, `lstlisting`, and custom macros when repetition is meaningful.
   - Keep visual design professional: readable margins, restrained color, clear heading hierarchy, useful running headers/footers, and accessible link colors.
   - Use manual spacing commands sparingly. Prefer class options, package configuration, and reusable macros.

5. **Handle references and citations**
   - Use `biblatex` with `biber` for new documents unless the existing project uses another system.
   - Never invent sources. If a citation is needed but not supplied, insert a clear compile-safe placeholder such as `\textbf{[Source needed: ...]}` or ask for sources.
   - Ensure every `\cite{}` key exists in the `.bib` file and every important figure/table/section has a label.

6. **Build and verify locally**
   - Prefer local commands only. Use `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` when `latexmk` and Perl are available; on MiKTeX without Perl, use `texify` or explicit `xelatex`/`biber` passes.
   - Do not use `--shell-escape` unless explicitly approved.
   - Review `.log`, `.blg`, and `.bbl` files for errors, unresolved references, missing citations, missing files, overfull boxes, and font issues.
   - If local TeX tools are unavailable, run static checks and report that PDF compilation was skipped.

7. **Report results**
   - Summarize files changed, document structure, build command used, warnings that remain, and any manual follow-up.
   - Separate facts, assumptions, and open questions when content or source material is incomplete.

## Quality Checklist

Use this checklist before delivering a LaTeX document:

- Title page contains title, subtitle if useful, author/organization, version/date, classification if applicable, and contact or owner if requested.
- Page layout has appropriate paper size, margins, line spacing, paragraph spacing, header/footer, and page numbering.
- Heading levels are consistent and no level is skipped for visual effect.
- Table of contents is generated and shows the right depth.
- Lists of figures, tables, glossary, acronyms, or index are included only when useful.
- Cross-references use labels rather than hardcoded numbers.
- Citations are present for factual claims that require support, and bibliography entries are complete enough for the requested style.
- Figures and tables have captions, labels, source notes when required, and fit within margins.
- Long tables use `longtable` or `tabularx` instead of spilling off the page.
- Code blocks use a configured listing style and do not overflow.
- Appendices are clearly separated and referenced from the body.
- Hyperlinks are active, legible, and not visually noisy.
- Build completes locally or static validation findings are documented.

## File Organization

Recommended project structure:

```text
latex-report/
|-- main.tex
|-- references.bib
|-- chapters/
|   |-- 01-introduction.tex
|   |-- 02-methodology.tex
|   |-- 03-findings.tex
|   `-- 04-conclusion.tex
|-- figures/
|-- tables/
|-- appendices/
|   `-- appendix-a.tex
|-- build/
`-- README.md
```

For small reports, a single `main.tex` plus `references.bib` is acceptable.

## Local Resources

- `templates/professional-report-template.tex`: complete editable LaTeX report template with title page, headers/footers, contents, citations, figures, tables, glossary, index, and appendices.
- `templates/references.bib`: starter bibliography file.
- `references/latex-document-architecture.md`: structure, package choices, and build guidance.
- `references/professional-formatting.md`: typography, layout, headings, tables, figures, and finishing checklist.
- `scripts/check_latex_project.py`: static local checker for common LaTeX report issues.

## Static Validation Script

Run from the skill directory or pass a target `.tex` file:

```bash
python scripts/check_latex_project.py path/to/main.tex
```

The script checks for missing structure, duplicate labels, unresolved citation keys against a local `.bib`, risky `shell-escape` mentions, missing bibliography setup, and common draft placeholders. It does not compile the PDF and does not contact the network.

## Build Commands

Recommended new-document build when `latexmk` and Perl are available:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
biber main
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

If the project uses `biblatex`, `latexmk` usually invokes `biber` automatically when configured. If it uses `natbib`, follow the existing BibTeX workflow.

MiKTeX fallback when `latexmk` is unavailable:

```bash
texify --pdf --engine=xetex --synctex=1 main.tex
```

Manual fallback for `biblatex` documents:

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
biber main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## Troubleshooting

- **Undefined references**: run LaTeX enough times, then inspect labels and `\cref{}` keys.
- **Undefined citations**: verify `.bib` file name, citation keys, `biber` or `bibtex` backend, and generated `.bcf` or `.aux`.
- **Overfull hboxes**: find the line in `.log`, then fix long URLs, table widths, code listings, or unbreakable inline text.
- **Missing fonts**: switch to installed fonts, use TeX Gyre fonts, or ask before installing fonts.
- **Package missing**: ask before installing packages; offer a fallback using packages already present.
- **Index or glossary missing**: ensure `makeindex`/`makeglossaries` step is configured and the document has entries.
