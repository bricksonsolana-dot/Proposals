"""
Desktop client for the Devox CRM (cloud version).
Opens the cloud-hosted CRM in a native window — no local server.

The CRM URL is read from (in priority order):
  1. CRM_URL environment variable
  2. crm_url.txt file next to this script
  3. fallback default
"""
import os
import sys
from pathlib import Path

import webview


def _set_windows_app_id():
    """Tell Windows this is a distinct app (not generic Python).
    Without this, all pywebview/Python apps share the same taskbar group.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Devox.Sales.CRM.1")
    except Exception:
        pass

ROOT = Path(__file__).parent
URL_FILE = ROOT / "crm_url.txt"
DEFAULT_URL = "http://127.0.0.1:5001"


def get_crm_url() -> str:
    env = os.environ.get("CRM_URL")
    if env:
        return env.strip()
    if URL_FILE.exists():
        try:
            url = URL_FILE.read_text(encoding="utf-8").strip()
            if url:
                return url
        except Exception:
            pass
    return DEFAULT_URL


def main():
    _set_windows_app_id()
    url = get_crm_url()
    icon_path = ROOT / "static" / "logo.ico"

    webview.create_window(
        title="Devox Sales",
        url=url,
        width=1400,
        height=900,
        min_size=(1000, 700),
        resizable=True,
    )
    if icon_path.exists():
        webview.start(icon=str(icon_path))
    else:
        webview.start()


if __name__ == "__main__":
    main()
