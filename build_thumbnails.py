#!/usr/bin/env python3
"""Capture the top fold of every manifest page with local Playwright/Chrome.

By default pages are loaded from local file URLs. Use --base-url when serving
the folder (for example http://127.0.0.1:8000) so relative assets behave as
they would in a browser.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def page_names() -> list[str]:
    manifest = json.loads((ROOT / "design-manifest.json").read_text(encoding="utf-8"))
    return [design["file"] for design in manifest["designs"]]


def chrome_path() -> str | None:
    candidates = [
        os.environ.get("CHROME_PATH", ""),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    return next((path for path in candidates if path and Path(path).is_file()), None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", help="Optional URL prefix instead of file URLs")
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--output", type=Path, default=ROOT / "thumbnails")
    parser.add_argument("filenames", nargs="*", help="Optional manifest filenames")
    args = parser.parse_args()
    names = args.filenames or page_names()
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print(f"Playwright is required: {exc}")
        return 2
    executable = chrome_path()
    launch_kwargs = {"headless": True}
    if executable:
        launch_kwargs["executable_path"] = executable
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": args.width, "height": args.height}, device_scale_factor=1)
        for name in names:
            source = f"{args.base_url.rstrip('/')}/{name}" if args.base_url else (ROOT / name).resolve().as_uri()
            output = args.output / f"{Path(name).stem}.png"
            page.goto(source, wait_until="domcontentloaded")
            page.screenshot(path=str(output), full_page=False)
            print(f"captured {name} -> {output}")
        browser.close()
    print(f"created {len(names)} thumbnail(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
