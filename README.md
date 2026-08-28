# Resume and Cover Letter PDF Formatter

`ResumeTextFormatterv4.py` is a desktop Tkinter application for editing resume and cover letter content, previewing the result as a PDF, and exporting PDF files.

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux with Tkinter installed
- Python packages:

```powershell
python -m pip install pypdf pillow pymupdf reportlab
```

On Windows, use the same Python executable that you use to run the application. For example:

```powershell
C:\Python313\python.exe -m pip install pypdf pillow pymupdf reportlab
```

## Start the application

Run the script without arguments:

```powershell
python ResumeTextFormatterv4.py
```

The application opens with these sample files loaded when they are present beside the script:

- `sample_cv.json`
- `sample_cover_letter.json`
- `sample_cv.md`
- `sample_cover_letter.md`

The main window contains:

- **Full CV**: edit the complete CV markdown.
- **Full Letter**: edit the complete cover letter markdown.
- **Main**: edit structured CV JSON fields.
- **Cover Letter**: edit structured cover letter fields.
- **JSON**: view or apply structured CV data.
- **Live PDF Preview**: review the current document before exporting.

Use **Apply Full CV** or **Apply Full Letter** after editing raw markdown so the preview and export use the latest text. The **Load Markdown** and **Save as Markdown** buttons can be used to work with other markdown files.

## Export PDF without opening the UI

Use the `--Output` option to run in headless mode. This mode does not open a Tkinter window.

### Export the default sample

If no input path is provided, the application uses `sample_cover_letter.md`:

```powershell
python ResumeTextFormatterv4.py --Output
```

This creates:

```text
sample_cover_letter.pdf
```

### Export a markdown file

```powershell
python ResumeTextFormatterv4.py --Output path\to\document.md
```

The PDF is written beside the input file with the same base name:

```text
path\to\document.pdf
```

Both CV and cover letter markdown files are supported. CV markdown is identified by headings such as `## PROFESSIONAL SUMMARY` or `## PROFESSIONAL EXPERIENCE`; other markdown is treated as a cover letter.

### Export a JSON file

```powershell
python ResumeTextFormatterv4.py --Output path\to\document.json
```

The application identifies the JSON type automatically:

- CV JSON contains fields such as `summary` or `experience`.
- Cover letter JSON contains fields such as `recipient` or `body`.

The PDF is written beside the JSON file with the same base name.

## Input formats

Supported input extensions are:

- `.md`
- `.markdown`
- `.txt`
- `.json`

JSON files must contain a top-level object. Markdown and text files are treated as complete document content.

## UI export

Inside the application:

1. Select the document tab you want to export.
2. Edit the content or load a file.
3. Click **Apply Full CV** or **Apply Full Letter** when using the full markdown tabs.
4. Click **Export PDF**.
5. Choose the output filename and folder.

The UI also saves related JSON and markdown/text files depending on the selected document type.

## Troubleshooting

### The script reports a missing module

Install the required packages again using the active Python interpreter:

```powershell
python -m pip install pypdf pillow pymupdf reportlab
```

### The default sample is not loaded

Make sure the sample files are in the same folder as `ResumeTextFormatterv4.py` and use the expected names:

- `sample_cv.md`
- `sample_cv.json`
- `sample_cover_letter.md`
- `sample_cover_letter.json`

### The PDF is empty or uses the wrong document type

For markdown input, use CV section headings for a CV. For JSON input, include the expected CV or cover letter fields so the formatter can identify the document type.
