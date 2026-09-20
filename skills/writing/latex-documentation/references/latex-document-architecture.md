# LaTeX Document Architecture

Use this reference when creating or reorganizing professional LaTeX reports and documentation.

## Recommended Defaults

- Engine: `xelatex` for modern fonts and Unicode.
- Class: `scrreprt` for reports and formal documentation; `scrartcl` for short documents; `book` or `memoir` only when the project already uses them or the report is book-length.
- Bibliography: `biblatex` with `biber` for new documents.
- References: `hyperref` plus `cleveref`.
- Headers and footers: `fancyhdr` or KOMA-Script page styles.
- Tables: `booktabs`, `tabularx`, `longtable`, `array`.
- Figures: `graphicx`, `caption`, `subcaption`.
- Code: `listings` for portable local builds; `minted` only with explicit approval because it requires shell escape.
- Index: `imakeidx`.
- Glossary/acronyms: `glossaries` when the document needs controlled terms.

## Standard Report Order

1. Title page.
2. Document control block if needed: version, owner, approver, status, confidentiality.
3. Abstract or executive summary.
4. Table of contents.
5. List of figures and list of tables for figure-heavy documents.
6. Acronyms or glossary for terminology-heavy documents.
7. Main chapters or sections.
8. Conclusion and recommendations.
9. Bibliography.
10. Appendices.
11. Index for manuals, reference guides, or long reports.

## Sectioning Rules

- Use one top-level style consistently: chapters for long reports, sections for short documents.
- Do not skip heading levels to create a visual effect.
- Keep heading names short, specific, and parallel.
- Set table of contents depth deliberately:

```latex
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{3}
```

## Labels And Cross-References

Use predictable prefixes:

```latex
\label{chap:introduction}
\label{sec:scope}
\label{fig:architecture}
\label{tab:requirements}
\label{eq:risk-score}
\label{app:source-data}
```

Prefer `\cref{tab:requirements}` over "Table 3" so numbering remains correct after edits.

## Bibliography Decisions

For new documents:

```latex
\usepackage[
  backend=biber,
  style=authoryear,
  sorting=nyt
]{biblatex}
\addbibresource{references.bib}
```

Choose citation style by document type:

- `authoryear`: business, policy, research reports.
- `numeric`: engineering, technical specifications, compact reports.
- `ieee`: engineering papers when requested.
- `apa`: academic or social-science style when requested.

Do not invent citations. Use placeholders or ask for sources.

## Build Strategy

Use `latexmk` when available:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

For bibliography issues:

```bash
biber main
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Never enable shell escape by default. If a document uses `minted`, external diagrams, or generated content requiring shell escape, explain the risk and ask for approval.

