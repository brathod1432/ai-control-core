# DOCX Style Patterns From CV PDF References

Use this reference when converting polished PDF CV layouts into editable DOCX templates. For job applications, create an ATS-safe master first and treat these layouts as human-review variants.

## Core Principle

Recreate the visual language, not the PDF mechanics. DOCX is strongest when the layout is built from styles, simple paragraphs, section breaks, paragraph borders, and restrained shading. Avoid screenshot-based CVs because they are hard to edit and poor for ATS extraction.

For ATS-compliant versions, translate each visual pattern into one-column text:

- Keep the palette and typography hierarchy.
- Replace sidebars with normal sections.
- Replace timelines with standard reverse-chronological entries.
- Replace skill bars with grouped plain-text skills.
- Replace icons with text labels.
- Keep contact details in the document body.

## Pattern 1: Minimal Editorial

Visual traits:

- Centered name.
- Narrow left label column.
- Wide right content column.
- Thin horizontal rules.
- Muted teal accent.

DOCX construction:

- One full-width title block.
- Repeated two-column tables for sections.
- Left cells contain section labels in small bold text.
- Right cells contain headings, bullets, and body content.
- Use bottom borders on section tables.

Best for:

- ATS-friendly applications.
- Recruiter-reviewed CVs.
- Conservative technical or business roles.

## Pattern 2: Ochre Timeline

Visual traits:

- Display name with distinctive personality.
- Contact row under the name.
- Date/location column on the left.
- Vertical timeline divider.
- Small section markers.
- Warm ochre headings and skill bars.

DOCX construction:

- Use a three-column table: dates, timeline marker, content.
- The marker column can be a narrow cell with a left or right border.
- Use shaded square markers with letters such as `P`, `W`, `E`, and `S` instead of fragile icon fonts.
- Skill bars can be nested 6-cell tables where filled cells use the accent color.

Best for:

- Human-reviewed CVs.
- Early/mid career profiles.
- Roles where personality is welcome but readability still matters.

## Pattern 3: Teal Serif Timeline

Visual traits:

- Strong serif name.
- Compact contact row.
- Left date/location column.
- Vertical divider.
- Teal section headings.
- Dense content with clear typographic contrast.

DOCX construction:

- Use a serif heading font such as Georgia or Cambria.
- Use a sans-serif body font such as Aptos, Calibri, or Arial.
- Use two-column tables with a left date column and right content column.
- Put a border on the content column's left edge to create the timeline.

Best for:

- Engineering, QA, data, and academic-adjacent CVs.
- Profiles with many skills and dense experience.

## Pattern 4: Blue Section Cards

Visual traits:

- Blue name.
- Wide gray section bands.
- Left section label blocks.
- Blue icon-like markers.
- Clean content cards.

DOCX construction:

- Use repeated two-column tables with gray cell shading.
- Left cell contains a small accent block and section label.
- Right cell contains role, dates, bullets, and skill grids.
- Use generous spacing between cards.

Best for:

- Modern one-page or two-page human-facing CVs.
- Executive summaries and polished profile documents.

## Skill Bars In DOCX

Use skill bars only in human-review variants. For ATS variants, write skills as plain text.

For designed variants, nested tables can create stable editable bars:

```text
[filled][filled][filled][empty][empty]
```

Implementation notes:

- Use fixed-width cells.
- Remove visible borders or use white borders.
- Fill completed cells with the accent color.
- Fill remaining cells with light gray.
- Keep labels outside the bar for readability.

## Page-Level Sample Strategy

When a user asks for style samples, generate one DOCX with multiple pages:

- Page 1: Minimal Editorial.
- Page 2: Ochre Timeline.
- Page 3: Teal Serif Timeline.
- Page 4: Blue Section Cards.

Use the same sample profile on every page so visual comparison is easy.

## Validation

After generating DOCX:

1. Open or convert with LibreOffice.
2. Export to PDF.
3. Render PDF pages to PNG.
4. Inspect each page for overflow, clipping, unreadable text, and broken tables.
5. Adjust table widths and font sizes if content spills.
