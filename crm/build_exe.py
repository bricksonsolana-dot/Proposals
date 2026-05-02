"""
Build a standalone DevoxSales.exe so the sales team doesn't need Python.

Usage (from this directory):
    python build_exe.py

Output:
    dist/DevoxSales.exe       (the single-file binary)
    dist/DevoxSales-Windows.zip (the zip containing the exe + crm_url.txt)

The exe just opens a native window pointing at the cloud CRM URL.
URL is read at runtime from crm_url.txt sitting next to the exe, so
you can rotate the URL without rebuilding.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
ICON = ROOT / "static" / "logo.ico"
SCRIPT = ROOT / "desktop_client.py"
URL_FILE = ROOT / "crm_url.txt"


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: {SCRIPT} not found", file=sys.stderr)
        return 1
    # Clean previous build artefacts (but keep DevoxSales-Setup.zip, etc.)
    for p in (BUILD, DIST / "DevoxSales", DIST / "DevoxSales.exe"):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.is_file():
            p.unlink(missing_ok=True)

    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", "DevoxSales",
        "--distpath", str(DIST),
        "--workpath", str(BUILD),
        "--specpath", str(BUILD),
    ]
    if ICON.exists():
        args.extend(["--icon", str(ICON)])
    args.append(str(SCRIPT))

    print(">>", " ".join(args))
    result = subprocess.run(args, cwd=str(ROOT))
    if result.returncode != 0:
        print("PyInstaller failed", file=sys.stderr)
        return result.returncode

    exe = DIST / "DevoxSales.exe"
    if not exe.exists():
        print(f"ERROR: expected output {exe} not found", file=sys.stderr)
        return 1

    # Bundle exe + crm_url.txt + README into a single zip
    zip_path = DIST / "DevoxSales-Windows.zip"
    if zip_path.exists():
        zip_path.unlink()
    readme_text = (
        "Devox Sales - Desktop App\n"
        "==========================\n\n"
        "1. Unzip this folder anywhere (e.g. Desktop).\n"
        "2. Double-click DevoxSales.exe.\n"
        "3. Login with the credentials your administrator gave you.\n\n"
        "No installation needed. Python is NOT required.\n"
        "If Windows SmartScreen warns you on first run, click\n"
        '"More info" then "Run anyway".\n'
    )
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(exe, "DevoxSales.exe")
        if URL_FILE.exists():
            z.write(URL_FILE, "crm_url.txt")
        z.writestr("README.txt", readme_text)

    print(f"\nDone:")
    print(f"  exe : {exe}  ({exe.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  zip : {zip_path}  ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
