# Maximo Import Error Highlighter

Marks error rows in an import CSV based on a Maximo import preview.

## Symptom

A Maximo import preview reports `BMXAA5598E` errors with messages like:

> CTGCC1046I - The CIRelation has not been saved, because the CI must exist before you can save the CIRelation.  
> BMXAA4129E - The record for Source=[CI], Target=[CI], Relation=[REL] already exists.

Scrolling between the preview and the CSV to find which rows failed is tedious and error-prone.

## Resolution

Paste the preview into this tool, select the CSV, and it marks every affected row with the exact error message in a new `Import_Error` column. A `.bak` backup is created automatically.

## Usage

```bash
python src/import_highlighter.py
```

1. Paste the Maximo import preview text into the text area
2. Click **Browse for CSV...** and select the CSV you tried to import
3. Click **Mark Import Errors**

The tool parses `BMXAA5598E` lines, extracts the affected CSV line ranges and error messages, and adds an `Import_Error` column to the CSV. A `.bak` backup of the original is created automatically.

## Build (standalone .exe)

Double-click **`build.bat`** (or right-click `build.ps1` → Run with PowerShell).

The script installs PyInstaller if needed and outputs `dist\ImportHighlighter.exe`.

## Keywords

Maximo, import preview, BMXAA5598E, CTGCC1046I, BMXAA4129E, CSV error highlighting, CI relationship import, bulk import troubleshooting, Maximo CIRelation, duplicate record detection
