# R-Copy-Files-on-Close

Small Windows automation to open **RStudio** and, when it closes, ask whether your local project folders should be copied to **Google Drive**.

## Improvements included

- external configuration via `config.json`
- backup log saved to `backup.log`
- clearer error handling
- copy only new/changed files
- optional exclude patterns for temp/cache files
- safer launch scripts for `RStudio` and the hidden VBS wrapper

## How to use

1. Edit `config.json` and set the folders you want to back up.
2. Confirm that `RStudio` is installed in one of these locations:
   - `C:\Program Files\RStudio\rstudio.exe`
   - `C:\Program Files\RStudio\bin\rstudio.exe`
3. Create or update your shortcut so it points to `hideBat_openR.vbs`.
4. Open RStudio using that shortcut.
5. When RStudio closes, the script will ask whether you want to sync the configured folders.

## Example `config.json`

```json
{
  "ask_confirmation": true,
  "show_success_message": true,
  "exclude_patterns": [
    "*.tmp",
    ".Rproj.user/*",
    "__pycache__/*"
  ],
  "copies": [
    {
      "from": "C:/Users/YOUR_USER/Documents/LocalProject",
      "to": "G:/MyDrive/Backups/LocalProject"
    }
  ]
}
```

## Requirements

- Windows
- Python 3
- Tk support enabled in Python

> `tkinter` and `shutil` are part of Python's standard library in a normal Windows installation.