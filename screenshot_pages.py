"""
Take screenshots of the public Devox Sales pages (login + download)
in both desktop and mobile viewports, save them to ./screenshots/.

Usage:
    python screenshot_pages.py [URL]

Default URL: https://devox-crm.onrender.com
"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://devox-crm.onrender.com"
OUT = Path("screenshots")
OUT.mkdir(exist_ok=True)


PAGES = [
    ("login", "/login"),
    ("download_desktop", "/download"),
    ("download_mobile", "/download"),
]


async def shoot(playwright, name, path, viewport, device="desktop"):
    is_mobile = device == "mobile"
    browser = await playwright.chromium.launch()
    context = await browser.new_context(
        viewport=viewport,
        device_scale_factor=2,
        is_mobile=is_mobile,
        has_touch=is_mobile,
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
            "Mobile/15E148 Safari/604.1"
        ) if is_mobile else None,
    )
    page = await context.new_page()
    full_url = URL.rstrip("/") + path
    print(f"  fetching {full_url} as {device} {viewport}")
    await page.goto(full_url, wait_until="networkidle", timeout=45000)
    # wait for fonts so screenshots aren't FOUT
    await page.evaluate("document.fonts.ready")
    out_path = OUT / f"{name}.png"
    await page.screenshot(path=str(out_path), full_page=True)
    size = out_path.stat().st_size
    print(f"  saved {out_path} ({size/1024:.0f} KB)")
    await browser.close()


async def main():
    async with async_playwright() as pw:
        await shoot(pw, "login_desktop", "/login",
                    {"width": 1440, "height": 900}, "desktop")
        await shoot(pw, "login_mobile", "/login",
                    {"width": 390, "height": 844}, "mobile")
        await shoot(pw, "download_desktop", "/download",
                    {"width": 1440, "height": 900}, "desktop")
        await shoot(pw, "download_mobile", "/download",
                    {"width": 390, "height": 844}, "mobile")


if __name__ == "__main__":
    asyncio.run(main())
