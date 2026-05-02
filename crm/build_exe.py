"""
Build a standalone DevoxSales installer so the sales team doesn't
need Python and doesn't need to extract anything.

Usage (from this directory):
    python build_exe.py

Output:
    dist/DevoxSales.exe        (the single-file portable binary)
    dist/DevoxSales-Setup.exe  (the proper Windows installer — what we ship)

The installer prompts the user with Next/Install, drops the exe in
Program Files, creates Start Menu + Desktop shortcuts, registers an
uninstaller, and offers to launch the app at the end.

Requirements:
    - PyInstaller (pip install pyinstaller pywebview)
    - Inno Setup 6 (https://jrsoftware.org/isinfo.php) — installed
      to its default location, or ISCC.exe on PATH.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
ICON = ROOT / "static" / "logo.ico"
SCRIPT = ROOT / "desktop_client.py"
URL_FILE = ROOT / "crm_url.txt"
ISS_FILE = ROOT / "installer" / "DevoxSales.iss"


def _find_iscc() -> str | None:
    """Locate the Inno Setup compiler (ISCC.exe)."""
    on_path = shutil.which("ISCC") or shutil.which("ISCC.exe")
    if on_path:
        return on_path
    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
            / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
            / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs"
            / "Inno Setup 6" / "ISCC.exe",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


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

    print(f"\nPyInstaller done: {exe} ({exe.stat().st_size / 1024 / 1024:.1f} MB)")

    # Build the proper Windows installer with Inno Setup
    iscc = _find_iscc()
    if not iscc:
        print(
            "\nWARNING: Inno Setup not found — installer NOT built.\n"
            "         Install from https://jrsoftware.org/isinfo.php "
            "(or run: winget install JRSoftware.InnoSetup)\n"
            "         Standalone exe is still available at dist/DevoxSales.exe",
            file=sys.stderr)
        return 0

    if not ISS_FILE.exists():
        print(f"ERROR: {ISS_FILE} not found", file=sys.stderr)
        return 1

    print(f"\nRunning Inno Setup: {iscc}")
    iscc_args = [iscc, str(ISS_FILE)]
    print(">>", " ".join(iscc_args))
    iscc_result = subprocess.run(iscc_args, cwd=str(ROOT))
    if iscc_result.returncode != 0:
        print("Inno Setup failed", file=sys.stderr)
        return iscc_result.returncode

    setup = DIST / "DevoxSales-Setup.exe"
    if not setup.exists():
        print(f"ERROR: expected installer {setup} not found", file=sys.stderr)
        return 1

    # Remove the legacy zip — we now ship the installer instead
    legacy_zip = DIST / "DevoxSales-Windows.zip"
    if legacy_zip.exists():
        legacy_zip.unlink()

    print(f"\nDone:")
    print(f"  installer : {setup}  ({setup.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  portable  : {exe}  ({exe.stat().st_size / 1024 / 1024:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
