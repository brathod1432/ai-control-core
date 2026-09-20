# CV Format Workflows

This reference explains how to produce CV outputs in DOCX, PPTX, ODT, Markdown, and PDF.

## Markdown First

Use Markdown as the intermediate planning format:

1. Extract source CV content.
2. Normalize into `profile_summary.md`.
3. Analyze completeness in `cv_analysis.md`.
4. Tailor content to the job description.
5. Generate final format.

Markdown is easy to diff, review, and reuse across output formats.

## DOCX Workflow

Use DOCX for ATS and recruiter workflows.

Preferred local tools:

- `python-docx`
- LibreOffice for conversion/rendering
- XML/ZIP parsing for advanced template editing

Steps:

1. Parse source `.docx`.
2. Normalize extracted profile.
3. Choose ATS Classic or Modern Sidebar layout.
4. Generate a new `.docx`.
5. Render or open to verify.
6. Export PDF if needed.

Validation:

- File opens without repair.
- All links work.
- Page count is expected.
- No clipped tables or sidebars.
- Text remains selectable.

## PPTX Workflow

Use PPTX for a visual career profile or executive introduction.

Preferred local tools:

- PptxGenJS
- python-pptx
- Existing `.pptx` templates

Steps:

1. Reduce CV content into a concise career narrative.
2. Select 4-6 slides.
3. Use one palette and one motif.
4. Include timeline, achievements, skills, and selected projects.
5. Keep each slide highly scannable.
6. Render or thumbnail-check slides.

Do not cram a full CV into slides. PPTX is for story and differentiation.

## ODT Workflow

Use ODT for LibreOffice/OpenDocument compatibility.

Preferred local tools:

- LibreOffice conversion from DOCX
- odfpy for structured ODT generation
- Template ODT files when available

Steps:

1. Generate clean Markdown or DOCX source.
2. Convert to ODT with LibreOffice when available.
3. Open or render the ODT to verify page layout.
4. Export PDF if requested.

ODT is a good fallback when Microsoft Word libraries are unavailable.

## PDF Workflow

Use PDF only as a final, non-editable delivery format.

Preferred local tools:

- LibreOffice export from DOCX or ODT
- PowerPoint export from PPTX
- PDF rendering for visual QA

Always keep an editable source file.

## Failure Recovery

If one format fails:

1. Keep Markdown source.
2. Switch to another editable format.
3. Report which dependency failed.
4. Preserve generated intermediate files for later regeneration.

Examples:

- `python-docx` unavailable: use LibreOffice conversion from Markdown or ODT.
- LibreOffice unavailable: generate DOCX directly with `python-docx`.
- PPTX library unavailable: create Markdown storyboard and DOCX one-pager.
- ODT library unavailable: generate DOCX and provide conversion instructions.

