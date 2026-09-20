# Professional LaTeX Formatting Guide

Use this guide to make reports and documentation polished, readable, and maintainable.

## Page Layout

- A4 is a good default for Europe and international business documents; Letter is appropriate when requested.
- Use margins around 25 mm for formal reports.
- Use 10.5 pt or 11 pt body type for dense technical documents; 12 pt for review-heavy documents.
- Keep line spacing modest. `\onehalfspacing` is useful for review drafts, but final reports often read better with normal or slightly increased spacing.
- Avoid large manual vertical spaces. Prefer package or class configuration.

## Title Pages

Include the fields the audience needs:

- Document title and optional subtitle.
- Organization, team, or author.
- Date and version.
- Status such as Draft, Review, Approved, or Final.
- Classification such as Public, Internal, Confidential, or Restricted when applicable.
- Optional approval table for controlled documentation.

## Headers And Footers

Good running headers answer "where am I?" without shouting.

- Left header: document title or chapter name.
- Right header: section name, version, or status.
- Footer center or outer edge: page number.
- Footer left/right: classification or owner when required.
- Suppress busy headers on title pages and chapter opening pages.

## Headings

- Make headings descriptive and parallel.
- Keep heading hierarchy shallow when possible.
- Use numbered headings for specifications, policies, and audit documents.
- Use unnumbered headings sparingly for front matter such as acknowledgments or executive summaries.

## Tables

- Use `booktabs` rules instead of vertical gridlines.
- Align numbers on decimal points if precision matters.
- Use `tabularx` for width-constrained text tables.
- Use `longtable` for tables that cross pages.
- Put units in headers, not every cell.
- Add source notes for externally sourced data.

Example:

```latex
\begin{table}[htbp]
  \centering
  \caption{Requirement Priority Summary}
  \label{tab:priority-summary}
  \begin{tabularx}{\textwidth}{lrrX}
    \toprule
    Priority & Count & Percent & Notes \\
    \midrule
    Critical & 8 & 16\% & Must be complete before release. \\
    High & 21 & 42\% & Required for the first production milestone. \\
    Medium & 17 & 34\% & Planned for staged delivery. \\
    Low & 4 & 8\% & Optional or deferred. \\
    \bottomrule
  \end{tabularx}
\end{table}
```

## Figures

- Store images under `figures/`.
- Use vector formats such as PDF for diagrams when practical.
- Use PNG for screenshots and raster exports.
- Every figure needs a caption and label.
- Avoid cropping images so tightly that labels are unreadable.

## Code Listings

Use `listings` for local-safe code blocks:

```latex
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  columns=fullflexible
}
```

Use `minted` only when the user explicitly approves shell escape.

## References And Links

- Load `hyperref` late in the preamble and `cleveref` after it.
- Use subdued link colors.
- Do not paste raw long URLs in prose; put them in footnotes or bibliography entries.
- Use `\url{}` for literal links and `\href{}` for readable link text.

## Index And Glossary

Add an index for long manuals, reference guides, and technical documentation where readers need lookup behavior.

```latex
\usepackage{imakeidx}
\makeindex
...
term\index{term}
...
\printindex
```

Add a glossary when terms need definitions:

```latex
\usepackage[acronym,toc]{glossaries}
\makeglossaries
\newacronym{api}{API}{Application Programming Interface}
...
\gls{api}
...
\printglossaries
```

## Final Polish Checklist

- No unresolved references or citations.
- No missing files.
- No accidental TODO markers in final output.
- No overfull boxes in visible body text.
- Tables and figures fit within page margins.
- TOC, bibliography, glossary, and index are generated.
- PDF metadata title and author are set when appropriate.
- Hyperlinks are clickable and readable.

