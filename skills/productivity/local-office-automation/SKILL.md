---
name: "local-office-automation"
description: "Use this skill when the user wants to automate local Microsoft Office files or installed Office desktop applications on Windows. Covers Word, Excel, and PowerPoint documents; file-level inspection and modification of .docx, .xlsx/.xlsm, and .pptx files; optional COM automation against installed Office apps for rendering, recalculation, macro-aware workflows, print/export, live document state, selection, comments, tracked changes, charts, pivots, and presentation delivery checks. Do not use for Microsoft 365 tenant administration, cloud Graph API work, SharePoint/OneDrive sync automation, or Google Workspace."
category: productivity
---

## Internal Safety Override

- Status: active for local Windows file and application automation only.
- Work local-first. Do not upload Office files, extracted text, document metadata, screenshots, diagnostics, or logs to external services unless the user explicitly approves that exact transfer.
- Do not connect Microsoft accounts, call Graph APIs, inspect OneDrive/SharePoint cloud state, or enable background sync unless the user explicitly asks for that networked action.
- Do not read secrets, credential stores, browser profiles, auth caches, `.env` files, private keys, or unrelated documents by default.
- Before using COM automation, confirm the target file paths, create backups for destructive edits, and avoid saving over originals unless the user requested in-place modification.
- Do not run macros, embedded OLE objects, external data refreshes, add-ins, links, or workbook connections unless explicitly approved for the current file.
- Prefer read-only analysis first. When modifying, write to a new output file unless in-place edits are specifically requested.
- Audit categories: command, secrets, privacy, local application state.

# Local Office Automation

## Overview

Use this skill to inspect, create, modify, validate, and automate Microsoft Office documents locally. Prefer file-level libraries for deterministic document edits, and use COM automation only when installed Office behavior is required.

Primary targets:
- Word: `.docx`, `.docm`, legacy `.doc` after conversion.
- Excel: `.xlsx`, `.xlsm`, `.xlsb`, `.csv` where Excel rendering/recalculation matters.
- PowerPoint: `.pptx`, `.pptm`, legacy `.ppt` after conversion.

Core principle: keep documents editable and preserve existing structure. Analyze the existing file first, make the smallest targeted change, validate with an independent check, and report residual risk.

---

## Tool Selection

| Need | Prefer | Notes |
|------|--------|-------|
| Fast text/table extraction | Python libraries or unpacked XML | No Office install required; safest for read-only analysis. |
| Structured Word edits | `python-docx` or Open XML package edits | Good for paragraphs, styles, tables, headers, footers, and images. |
| Structured Excel edits | `openpyxl`, `pandas`, `xlsxwriter` | Use formulas in workbooks instead of hardcoded calculated outputs. |
| Structured PowerPoint edits | `python-pptx`, Open XML package edits, PptxGenJS | Best for editable slide content and template-preserving changes. |
| Formula recalculation | Excel COM automation or LibreOffice if available | `openpyxl` writes formulas but does not calculate cached values. |
| Rendering/export to PDF/images | Office COM automation or local LibreOffice | Use COM when Office fidelity is required. |
| Live app state | Office COM automation | Required for active selection, open documents, windows, comments panes, slide show state, or unsaved content. |
| Macros/add-ins/data refresh | Office COM automation with explicit approval | High-risk; default is disabled. |

---

## Standard Workflow

1. Identify file type, desired output, whether edits are in-place or copied, and whether Office app state is involved.
2. Inventory the file locally: file size, extension, read-only flag, macro presence, external links, embedded objects, workbook connections, comments, tracked changes, hidden sheets/slides, and protection.
3. Create a backup or write to a new output path before making destructive edits.
4. Choose the least powerful tool that preserves the requested fidelity.
5. Modify in a focused way. Preserve existing styles, layouts, formulas, metadata, and template conventions unless asked to normalize them.
6. Validate using file-open checks, content checks, and when relevant, rendering or app-level checks.
7. Report changed files, validation commands, any skipped checks, and risks such as macros not executed or formulas not refreshed.

---

## Windows And Office Detection

Use local checks only. Prefer non-invasive detection before launching Office apps.

```powershell
# Check whether Office applications are registered for COM automation.
$apps = "Word.Application", "Excel.Application", "PowerPoint.Application"
foreach ($app in $apps) {
    try {
        $type = [type]::GetTypeFromProgID($app)
        [pscustomobject]@{ ProgId = $app; Available = [bool]$type }
    } catch {
        [pscustomobject]@{ ProgId = $app; Available = $false }
    }
}
```

Prefer Python package checks before installing anything. Do not install packages from the network without explicit approval.

```powershell
@'
import importlib.util
for name in ["docx", "openpyxl", "pptx", "win32com.client", "pandas"]:
    print(f"{name}: {bool(importlib.util.find_spec(name))}")
'@ | python -
```

---

## File-Level Automation

### Word Files

Use file-level operations when the task is content extraction, template filling, style-preserving edits, table edits, image replacement, comments/tracked-change inventory, or raw package inspection.

Recommended local approaches:
- `python-docx` for normal `.docx` paragraph, run, table, section, header, footer, image, and style work.
- Open XML ZIP inspection for comments, tracked changes, custom XML, content controls, relationships, external links, and metadata.
- Local rendering with Office or LibreOffice when page layout fidelity matters.

Example inventory:

```python
from pathlib import Path
from zipfile import ZipFile
from docx import Document

path = Path("input.docx")
doc = Document(path)
print("paragraphs", len(doc.paragraphs))
print("tables", len(doc.tables))
print("sections", len(doc.sections))

with ZipFile(path) as z:
    names = set(z.namelist())
    print("comments", "word/comments.xml" in names)
    print("tracked changes", any("w:ins" in z.read(n).decode("utf-8", "ignore") or
                                 "w:del" in z.read(n).decode("utf-8", "ignore")
                                 for n in names if n.startswith("word/document")))
```

Word validation:
- Reopen the output with `python-docx` to catch corrupt package structure.
- If layout matters, export to PDF locally and visually inspect page images.
- For tracked changes/comments, verify counts before and after the edit.
- For template work, search for leftover placeholders.

### Excel Files

Use file-level operations for tabular cleanup, formulas, styles, worksheet changes, charts where library support is sufficient, named ranges, data validation, and workbook structure checks.

Recommended local approaches:
- `openpyxl` for `.xlsx` and many `.xlsm` edits while preserving VBA with `keep_vba=True`.
- `pandas` for analysis and data cleanup, then write back carefully.
- `xlsxwriter` for new workbooks with charts and formatting.
- COM automation for recalculation, pivot refresh, chart fidelity, password prompts, external links, or `.xlsb`/legacy `.xls` workflows.

Excel rules:
- Use workbook formulas for dynamic calculations, not Python-hardcoded results, unless the user wants static values.
- Preserve formulas, number formats, hidden sheets, freeze panes, filters, validations, defined names, and VBA projects.
- Do not refresh external connections or run macros without explicit approval.
- Write `.xlsm` outputs with macro preservation enabled when macros exist.

Example workbook inventory:

```python
from openpyxl import load_workbook

path = "input.xlsx"
wb = load_workbook(path, data_only=False, read_only=False, keep_vba=path.endswith(".xlsm"))
print("sheets", wb.sheetnames)
print("defined_names", len(wb.defined_names))

for ws in wb.worksheets:
    formulas = sum(
        1 for row in ws.iter_rows()
        for cell in row
        if isinstance(cell.value, str) and cell.value.startswith("=")
    )
    print(ws.title, "rows", ws.max_row, "cols", ws.max_column, "formulas", formulas)
```

Excel validation:
- Reopen with formulas and with cached values when available.
- Use Excel COM recalculation when formulas, pivots, or charts are part of the deliverable.
- Check for formula errors: `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NUM!`, and `#NULL!`.
- Confirm sheet visibility, formulas, number formats, named ranges, and protected ranges were preserved.

### PowerPoint Files

Use file-level operations for slide text, images, notes, layouts, theme-aware shape edits, speaker notes extraction, combining decks, and template-based generation.

Recommended local approaches:
- `python-pptx` for common slide, shape, text, image, and table edits.
- PptxGenJS for creating editable decks from scratch when the repo workflow prefers JavaScript.
- Open XML ZIP inspection for comments, notes, relationships, embedded media, slide masters, and unsupported features.
- COM automation for high-fidelity rendering, slide export, SmartArt, animation timing, notes pages, or active slideshow state.

PowerPoint validation:
- Extract text and confirm content order.
- Render slides to images or PDF locally and inspect for overlap, clipped text, low contrast, placeholder text, and missing media.
- Verify slide count, hidden slides, notes, comments, theme/layout references, and embedded media relationships.

---

## Optional COM Automation

Use COM only on Windows when installed Office behavior is necessary. COM automation can touch live app state and may trigger prompts, add-ins, macros, links, external refreshes, protected-view behavior, or file locks. Keep apps invisible by default unless the user asks to interact with the UI.

COM safety defaults:
- Open files read-only for analysis.
- Disable alerts for automated batch operations, but restore settings afterward.
- Set automation security to disable macros unless macro execution is explicitly approved.
- Do not save over the original file unless requested.
- Always close documents/workbooks/presentations and quit app instances you created.
- Release COM objects and run cleanup to prevent orphaned Office processes.

Python COM pattern:

```python
from pathlib import Path
import pythoncom
import win32com.client as win32

src = Path("input.xlsx").resolve()
out = Path("output.xlsx").resolve()

pythoncom.CoInitialize()
excel = None
wb = None
try:
    excel = win32.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    excel.AutomationSecurity = 3  # msoAutomationSecurityForceDisable
    wb = excel.Workbooks.Open(str(src), UpdateLinks=0, ReadOnly=True)
    wb.ForceFullCalculation = True
    excel.CalculateFullRebuild()
    wb.SaveAs(str(out), FileFormat=51)  # xlsx
finally:
    if wb is not None:
        wb.Close(SaveChanges=False)
    if excel is not None:
        excel.DisplayAlerts = True
        excel.Quit()
    pythoncom.CoUninitialize()
```

PowerShell COM pattern:

```powershell
$word = New-Object -ComObject Word.Application
$doc = $null
try {
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open((Resolve-Path ".\input.docx").Path, $false, $true)
    $doc.ComputeStatistics(2) # wdStatisticWords
} finally {
    if ($doc) { $doc.Close($false) }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
```

---

## Advanced Analysis

### Office Package Inspection

Modern Office files are ZIP packages. Inspect package relationships before edits that may affect media, charts, comments, macros, links, or embedded files.

Check for:
- `[Content_Types].xml` package content types.
- `_rels/.rels` and `*/_rels/*.rels` relationships.
- `vbaProject.bin` macro projects.
- `externalLink`, `oleObject`, `activeX`, `embeddings`, and remote hyperlink relationships.
- Custom XML parts, content controls, comments, notes, tracked changes, and hidden slides/sheets.
- Document properties in `docProps/core.xml`, `docProps/app.xml`, and `docProps/custom.xml`.

Example package scan:

```python
from pathlib import Path
from zipfile import ZipFile

risky_terms = ("vbaProject.bin", "externalLink", "oleObject", "activeX", "embeddings/")
with ZipFile(Path("input.docx")) as z:
    for name in z.namelist():
        if any(term in name for term in risky_terms):
            print(name)
```

### App State Analysis

Use COM app-state inspection only when the user asks about currently open Office windows, active selection, unsaved changes, visible UI state, slide show mode, active workbook filters, selected ranges, or currently open documents.

Examples of useful app-state checks:
- Word: active document path, `Saved` flag, selection text, revisions count, comments count, protection type, active window view.
- Excel: active workbook path, `Saved` flag, selected range, calculation mode, filters, protected sheets, workbook connections, pivot caches, circular references.
- PowerPoint: active presentation path, `Saved` flag, selected slide/shape, slide show windows, hidden slides, comments, notes page text.

Never assume open Office app state is safe to modify. Prefer a read-only report first, then ask before saving, closing, running macros, refreshing data, or changing user selection.

### Protected And Macro-Enabled Files

- If a file is password-protected, stop and ask the user for the password or an unprotected copy. Do not attempt bypass.
- If macros are present, preserve them when editing unless removal is requested.
- If macro execution is requested, explain the risk, run only the named macro, keep the file local, and validate outputs without exposing macro code or generated data externally.
- For `.xlsm` with `openpyxl`, use `keep_vba=True` and save as `.xlsm`.
- For `.docm` and `.pptm`, prefer package-preserving edits or COM automation to avoid stripping macros.

---

## Modification Patterns

### Safe In-Place Edit Pattern

Use this only when the user requested in-place edits.

1. Confirm the absolute target path is inside the active workspace or explicitly named by the user.
2. Create a sibling backup such as `filename.before-local-office-automation.ext`.
3. Modify a temporary output file.
4. Validate the temporary output.
5. Replace the original only after validation succeeds.
6. Keep the backup unless the user asks to remove it.

### Batch Processing Pattern

For multiple files:
- Build an explicit manifest of target files.
- Skip temporary Office lock files beginning with `~$`.
- Process one file at a time when using COM to avoid cross-file app state confusion.
- Write per-file status notes locally: `processed`, `skipped`, `failed`, validation result, and output path.
- Never recursively process broad directories without user approval.

### Redaction Pattern

For sensitive documents:
- Work on a copy.
- Search body text, headers/footers, comments, speaker notes, hidden sheets/slides, document properties, custom XML, alt text, and embedded objects.
- Validate redaction by extracting text from the final file and searching for target terms.
- If exporting to PDF, validate the exported PDF text as well.

---

## Validation Checklist

Run validation proportional to the change:
- File opens locally with the chosen library or Office app.
- Output file extension and format match user expectations.
- Original file is preserved unless in-place edit was requested.
- No unexpected macros, external links, embedded objects, workbook connections, hidden sheets/slides, comments, or tracked changes were introduced.
- Placeholder text and temporary markers are removed.
- Word: paragraphs, tables, headers, footers, comments, tracked changes, page count, and rendered layout are checked when relevant.
- Excel: formulas recalculate, no formula errors remain, formats and formulas are preserved, pivots/charts refresh only if approved, and visible values match expectations.
- PowerPoint: slide count, notes, hidden slides, media, theme/layout references, and rendered slide images are checked when relevant.
- COM-created app instances are closed and no orphaned Office processes remain from the automation session.

For final reporting, include:
- Files read and files changed, using absolute local paths where helpful.
- Tools used: file-level library, package inspection, COM app, local renderer, or manual XML edit.
- Validation performed and validation not performed.
- Safety exceptions: macros not run, links not updated, external refresh skipped, protected content not bypassed.

---

## When To Stop And Ask

Stop before:
- Using network, cloud storage, Graph APIs, account connectors, or external conversion services.
- Running macros, add-ins, OLE objects, or external data refresh.
- Saving over an original Office file without a backup.
- Closing user-open Office windows or discarding unsaved changes.
- Attempting to bypass passwords, IRM, protected view, sensitivity labels, or restricted permissions.
- Processing broad folders, personal document libraries, synced OneDrive folders, or paths outside the active workspace without explicit approval.
- Installing new packages from the network.
