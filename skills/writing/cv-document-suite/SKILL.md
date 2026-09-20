---
name: cv-document-suite
description: Prepare, analyze, tailor, and generate professional CVs and resumes across DOCX, PPTX, and ODT formats. Use when the user asks to parse a CV, extract profile details, create profile_summary.md, generate cv_analysis.md, tailor a CV to a job description, build editable Word/PowerPoint/OpenDocument CVs, choose a professional color palette, or fall back between document formats when one toolchain is unavailable.
license: MIT
metadata:
  version: 1.0.0
  category: writing
  domain: cv-resume-documents
  updated: 2026-05-14
  formats: docx, pptx, odt, md, pdf
---

## Internal Safety Override

- Status: local-only unless explicitly opted into external access.
- CVs contain personal data. Do not upload CV files, extracted text, profile summaries, job descriptions, generated documents, or rendered pages to external services unless the user explicitly approves that exact action.
- Do not expose phone numbers, emails, addresses, account IDs, or private employer/client details in logs or public summaries.
- Do not edit the original CV directly. Write derived files to a new output path.
- Before installing packages, running converters, enabling macros, opening account connectors, or using network services, state the destination, data scope, and reason, then wait for explicit approval.
- Prefer local libraries and installed tools: `python-docx`, LibreOffice, PptxGenJS, python-pptx, odfpy, Pandoc, and local XML/ZIP parsing.
- Audit categories: personal-data, filesystem, command-execution, document-content, network, package-install.

# CV Document Suite

This skill prepares professional CV and resume outputs in DOCX, PPTX, and ODT, with Markdown analysis artifacts as the stable intermediate layer. Default to ATS-compliant CVs for applications; designed or graphical variants are secondary human-review copies.

## Use This Skill For

- Parsing a `.docx` CV and extracting profile details.
- Creating `profile_summary.md`, `docx_guide.md`, and `cv_analysis.md`.
- Tailoring a CV to a job description.
- Creating a professional editable CV in DOCX, PPTX, or ODT.
- Choosing a visual direction, layout, color palette, and typography for a CV.
- Falling back between DOCX, PPTX, ODT, Markdown, and PDF when a toolchain is unavailable.
- Building ATS-compliant application CVs first, plus presentation-style variants when useful.

## Default Workflow

1. **Collect inputs**
   - CV source path.
   - Target job description, if available.
   - Desired output format: DOCX, PPTX, ODT, PDF, or Markdown.
   - Target market: EU, US, UK, academic, executive, technical, consulting, creative, or regulated.
   - Preferred tone and design: conservative, modern, executive, technical, portfolio, or minimal.

2. **Preserve originals**
   - Never modify the source CV.
   - Copy templates before filling them.
   - Keep generated files in a clear output folder.

3. **Extract profile data**
   - Parse structured text from DOCX/ODT/PPTX.
   - Inspect tables, headers, footers, and text boxes when contact details or sidebars are likely.
   - Normalize content into the schema in `references/cv-data-model.md`.
   - Do not invent missing details.

4. **Create Markdown working files**
   - `profile_summary.md`: extracted profile details and normalized data.
   - `docx_guide.md`: document workflow notes and local parsing/writing guide.
   - `cv_analysis.md`: completeness review, improvement areas, and job alignment rubric.

5. **Select output strategy**
   - DOCX: best for ATS, recruiters, editable business CVs, and formal applications. Default to an ATS-safe DOCX master.
   - PPTX: best for portfolio profiles, executive one-pagers, consulting bios, and visual career narratives.
   - ODT: best for LibreOffice/OpenDocument workflows and open standards.
   - If the requested format fails, fall back to Markdown plus another editable format and report the limitation.

6. **Apply ATS-first rules**
   - Read `references/cv-ats-compliance.md` before generating application CVs.
   - Use one-column searchable text, standard headings, normal paragraph flow, and no essential content in images, text boxes, headers, footers, sidebars, charts, or skill bars.
   - If the user wants a designed CV, produce it as a second human-review variant derived from the ATS master.

7. **Apply design system**
   - Pick one palette from `references/cv-design-palettes.md`.
   - If the user provides PDF references, read `references/cv-docx-style-patterns.md` and translate the visual language into editable DOCX tables, borders, shading, and styles.
   - Keep contrast high, section hierarchy clear, and text extractable.
   - Use color as hierarchy, not decoration.
   - Avoid putting critical ATS content only inside images.

8. **Generate and validate**
   - Reopen or render the output where possible.
   - Extract text from generated DOCX files and verify ATS reading order for the application version.
   - Check page count, clipping, alignment, spacing, headers, links, and section order.
   - For job-targeted CVs, compare against the job description and report gaps.

## Format Fallback Matrix

| Requested | Preferred Tooling | Fallback 1 | Fallback 2 |
|---|---|---|---|
| DOCX | `python-docx` or template XML editing | LibreOffice conversion from ODT | Markdown source plus manual DOCX steps |
| PPTX | PptxGenJS or python-pptx | Convert selected CV content into slides from Markdown | Export visual summary as PDF |
| ODT | LibreOffice or odfpy | Generate DOCX then convert to ODT | Markdown plus ODT structure guide |
| PDF | LibreOffice export | Render from DOCX/ODT/PPTX | Provide editable source only |

## Output Standards

- CV content should be truthful, specific, and evidence-driven.
- Use measurable achievements where possible.
- Keep ATS variants simple, one-column, and text-based.
- Keep graphical variants readable and professional, but never make them the only application copy.
- Use consistent dates, section naming, capitalization, and punctuation.
- Use active verbs and outcome-focused bullets.
- Use portfolio/visual elements only when they help the target role.

## Local References

- `references/cv-data-model.md`: normalized CV schema and extraction checklist.
- `references/cv-ats-compliance.md`: ATS-safe structure, layout, typography, and validation rules.
- `references/cv-design-palettes.md`: professional palettes, typography, and visual systems.
- `references/cv-docx-style-patterns.md`: how to recreate polished PDF CV layouts in editable DOCX.
- `references/cv-format-workflows.md`: DOCX, PPTX, ODT, Markdown, and PDF workflows.

## PDF Reference To DOCX Workflow

When the user adds PDF references:

1. Render the PDF pages locally.
2. Extract text only as supporting context; use rendered pages for layout fidelity.
3. Identify reusable patterns: section labels, timeline columns, accent colors, skill bars, cards, title block, contact row, margins, and typography.
4. Create editable DOCX equivalents with:
   - tables for columns and cards,
   - paragraph borders for rules,
   - table shading for bands,
   - nested tables for skill bars,
   - Word styles for headings and body text.
5. Avoid placing PDF page screenshots in the DOCX except as optional reference thumbnails.
6. Render or export the DOCX for visual QA before delivery.
