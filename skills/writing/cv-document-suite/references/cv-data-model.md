# CV Data Model

Use this model as the neutral intermediate representation before generating DOCX, PPTX, ODT, PDF, or Markdown outputs.

## Normalized Schema

```yaml
profile:
  name:
  headline:
  location:
  email:
  phone:
  links:
    linkedin:
    github:
    portfolio:
    website:
summary:
  short:
  long:
skills:
  technical:
  tools:
  platforms:
  domain:
  languages:
  leadership:
experience:
  - title:
    company:
    location:
    start:
    end:
    current:
    context:
    bullets:
      - text:
        evidence:
        keywords:
education:
  - institution:
    degree:
    field:
    start:
    end:
    notes:
certifications:
  - name:
    issuer:
    date:
    expiry:
projects:
  - name:
    role:
    technologies:
    outcome:
awards:
publications:
volunteering:
interests:
metadata:
  target_role:
  target_market:
  source_file:
  extraction_notes:
```

## Extraction Checklist

- Check body paragraphs.
- Check tables and repeated table cells.
- Check headers and footers for contact details.
- Check text boxes and drawing XML for sidebar content.
- Preserve original wording for facts, dates, job titles, certifications, and employer names.
- Normalize only formatting, ordering, and labels unless the user asks for rewriting.
- Mark unknowns as `pending` or `not found`; do not invent.

## Job Description Alignment

When a job description is provided:

1. Extract hard requirements.
2. Extract soft requirements.
3. Extract domain keywords.
4. Map each requirement to existing CV evidence.
5. Mark gaps as:
   - `missing`
   - `present but weak`
   - `present and strong`
   - `not relevant`
6. Recommend edits that remain truthful.

## Bullet Quality Rules

Strong bullets usually contain:

- Action verb
- Scope
- Method or tool
- Result
- Metric when available

Pattern:

```text
Led [scope] using [method/tool], resulting in [measurable outcome].
```

Avoid:

- Vague responsibility lists
- Claims without evidence
- Repeating the same verb
- Overloaded bullets longer than 2 lines

