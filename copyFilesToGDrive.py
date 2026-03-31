from __future__ import annotations

import json
import logging
import shutil
from fnmatch import fnmatch
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
LOG_FILE = BASE_DIR / "backup.log"


def create_hidden_root() -> tk.Tk:
    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    return root


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE.name}. Edit it with your folders before running the backup."
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    copies = config.get("copies", [])
    if not copies:
        raise ValueError("No copy tasks were configured in config.json.")

    return config


def should_skip(relative_path: Path, patterns: list[str]) -> bool:
    normalized = relative_path.as_posix()
    return any(
        fnmatch(normalized, pattern) or fnmatch(relative_path.name, pattern)
        for pattern in patterns
    )


def copy_changed_files(source: Path, destination: Path, exclude_patterns: list[str]) -> int:
    copied_files = 0
    destination.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):
        relative_path = item.relative_to(source)
        if should_skip(relative_path, exclude_patterns):
            continue

        target = destination / relative_path
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        if (not target.exists()) or item.stat().st_mtime > target.stat().st_mtime or item.stat().st_size != target.stat().st_size:
            shutil.copy2(item, target)
            copied_files += 1

    return copied_files


def run_backup_jobs(config: dict) -> tuple[int, list[str]]:
    total_files = 0
    summary_lines: list[str] = []
    global_excludes = config.get("exclude_patterns", [])

    for index, job in enumerate(config["copies"], start=1):
        source = Path(job["from"]).expanduser()
        destination = Path(job["to"]).expanduser()
        excludes = global_excludes + job.get("exclude_patterns", [])

        if not source.exists():
            raise FileNotFoundError(f"Source folder not found:\n{source}")

        if source.resolve() == destination.resolve():
            raise ValueError(f"Source and destination cannot be the same folder:\n{source}")

        updated_files = copy_changed_files(source, destination, excludes)
        total_files += updated_files
        summary_lines.append(
            f"{index}. {source} -> {destination} ({updated_files} file(s) copied/updated)"
        )

    return total_files, summary_lines


def main() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    root = None
    try:
        config = load_config()
        root = create_hidden_root()

        if config.get("ask_confirmation", True):
            answer = messagebox.askokcancel(
                title="Confirmation",
                message="Would you like to copy the files to Google Drive?",
            )
            if not answer:
                logging.info("Backup cancelled by the user.")
                return

        total_files, summary_lines = run_backup_jobs(config)
        summary = "\n".join(summary_lines)
        logging.info("Backup completed successfully. %s", " | ".join(summary_lines))

        if config.get("show_success_message", True):
            messagebox.showinfo(
                title="Success",
                message=(
                    "Backup finished successfully.\n\n"
                    f"{summary}\n\n"
                    f"{total_files} file(s) copied or updated."
                ),
            )
    except Exception as exc:
        logging.exception("Backup failed: %s", exc)
        error_root = root or create_hidden_root()
        messagebox.showerror(
            title="Backup error",
            message=f"Backup failed.\n\n{exc}\n\nCheck backup.log for details.",
        )
        if root is None:
            error_root.destroy()
    finally:
        if root is not None:
            root.destroy()


if __name__ == "__main__":
    main()

        
