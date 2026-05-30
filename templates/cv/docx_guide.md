# DOCX Guide For CV Workflows

This guide describes local-first ways to parse, extract, edit, and write `.docx` CV files.

## Safety Baseline

- Work locally by default.
- Do not upload CV files, extracted text, contact details, or job descriptions to external services without explicit approval.
- Redact personal data from logs and summaries when sharing command output.
- Preserve the original CV. Write generated files to a new output path.

## DOCX Structure

A `.docx` file is a ZIP archive containing XML parts. Important locations include:

- `word/document.xml`: main body text and structure
- `word/styles.xml`: paragraph and character styles
- `word/numbering.xml`: bullet and numbering definitions
- `word/media/`: embedded images
- `docProps/core.xml`: document metadata
- `word/header*.xml` and `word/footer*.xml`: headers and footers

## Preferred Parsing Methods

### 1. Structured Text Extraction With Python

Use `python-docx` for most CV parsing:

```python
from docx import Document

doc = Document("cv.docx")
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

tables = []
for table in doc.tables:
    rows = []
    for row in table.rows:
        rows.append([cell.text.strip() for cell in row.cells])
    tables.append(rows)
```

Best for:

- Normal paragraphs
- Tables
- Section headings
- Simple contact blocks

Limitations:

- Text boxes, shapes, comments, and some headers may need XML-level parsing.
- Visual order can differ from XML order in heavily designed CVs.

### 2. XML-Level Extraction

Unzip the `.docx` when layout or text boxes matter:

```bash
python -m zipfile -e cv.docx unpacked_cv
```

Then inspect:

```text
unpacked_cv/word/document.xml
unpacked_cv/word/header1.xml
unpacked_cv/word/footer1.xml
unpacked_cv/word/styles.xml
```

Best for:

- Text boxes
- Custom shapes
- Header/footer contact details
- Diagnosing broken styles
- Finding hidden or repeated content

### 3. Visual Rendering

When formatting matters, render the document:

```bash
soffice --headless --convert-to pdf --outdir output cv.docx
pdftoppm -png output/cv.pdf output/cv-page
```

Best for:

- Checking alignment
- Detecting overflow
- Verifying margins
- Reviewing page breaks
- Comparing template fidelity

## Writing DOCX Files

### Python `python-docx`

Use this for structured CV generation when high-level document controls are enough:

```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10)

doc.add_heading("Candidate Name", level=0)
doc.add_paragraph("Professional headline | Email | Phone | Location")

doc.add_heading("Professional Summary", level=1)
doc.add_paragraph("Three to five lines focused on the target role.")

doc.save("cv_output.docx")
```

Use for:

- ATS-friendly CVs
- Conservative business formats
- Clean section hierarchy
- Tables and simple layout

### Template-Based Editing

When a `.docx` template exists:

1. Copy the template to a new output file.
2. Extract placeholders or existing sections.
3. Replace content while preserving styles.
4. Render and inspect the output.

Recommended placeholders:

```text
{{NAME}}
{{HEADLINE}}
{{CONTACT}}
{{SUMMARY}}
{{SKILLS}}
{{EXPERIENCE}}
{{EDUCATION}}
{{CERTIFICATIONS}}
```

### Low-Level XML Editing

Use XML editing only when high-level tools cannot preserve the design:

1. Unpack `.docx`.
2. Edit targeted XML nodes.
3. Repack as `.docx`.
4. Validate by opening or rendering.

Avoid broad XML rewrites. They are fragile.

## Extraction Schema

Normalize extracted CV content into this structure before writing any format:

```yaml
profile:
  name:
  headline:
  location:
  email:
  phone:
  links:
summary:
skills:
  technical:
  tools:
  domain:
  languages:
experience:
  - title:
    company:
    location:
    start:
    end:
    bullets:
education:
  - institution:
    degree:
    field:
    start:
    end:
certifications:
projects:
awards:
```

## Validation Checklist

- Original file remains unchanged.
- Extracted name and contact details are correct.
- No duplicated table cell text.
- Dates are normalized.
- Bullets keep measurable achievements when present.
- Final `.docx` opens without repair prompts.
- Layout is checked visually after generation.
- Exported PDF matches the intended page count.

