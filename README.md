# Maximo Import Error Highlighter

Marks error rows in an import CSV based on a Maximo import preview.

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
