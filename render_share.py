#!/usr/bin/env python3
"""Turn share.html (written by build.py) into assets/img/share.jpg, the link-preview image.

Run it after build.py:  python3 build.py && python3 render_share.py
Needs Playwright:        pip install playwright && python3 -m playwright install chromium
The GitHub Action in .github/workflows/build.yml does both on every relevant push.
Set CHROME=/path/to/chrome to use an installed Chrome instead of Playwright's Chromium.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "share.html"
TARGET = ROOT / "assets" / "img" / "share.jpg"


def main():
    if not SOURCE.exists():
        sys.exit("share.html is missing: run python3 build.py first.")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is missing: pip install playwright && python3 -m playwright install chromium")

    with sync_playwright() as p:
        options = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
        browser = p.chromium.launch(**options)
        page = browser.new_page(viewport={"width": 1200, "height": 627}, device_scale_factor=1)
        page.goto(SOURCE.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(TARGET), type="jpeg", quality=88,
                        clip={"x": 0, "y": 0, "width": 1200, "height": 627})
        browser.close()
    print(f"Rendered {TARGET.relative_to(ROOT)} from share.html")


if __name__ == "__main__":
    main()
