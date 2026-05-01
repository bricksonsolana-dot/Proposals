"""
Desktop launcher for the Lead Finder.
Starts the Flask dashboard in a background thread and shows it in a native window.
On close, prompts for confirmation if a scrape or enrichment is running.

Usage:
    python desktop_app.py
or double-click LeadFinder.bat (Windows).
"""
import logging
import os
import socket
import sys
import threading
import time
from pathlib import Path

import webview

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def _set_windows_app_id():
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Devox.LeadFinder.1")
    except Exception:
        pass


def find_free_port(preferred: int = 5000) -> int:
    for port in [preferred, preferred + 1, preferred + 2, 0]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return s.getsockname()[1]
        except OSError:
            continue
    return preferred


def is_already_running(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect(("127.0.0.1", port))
            return True
    except OSError:
        return False


def start_flask(port: int):
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    import dashboard
    dashboard.app.run(host="127.0.0.1", port=port,
                       debug=False, threaded=True, use_reloader=False)


def wait_until_ready(port: int, timeout: float = 15.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                s.connect(("127.0.0.1", port))
                return True
        except OSError:
            time.sleep(0.15)
    return False


def is_busy() -> bool:
    """True if a scrape or enrichment is currently running."""
    try:
        import dashboard
        scraping = bool(dashboard.state.get("running"))
        enriching = bool(dashboard.enrich_state.get("running"))
        syncing = bool(dashboard.sync_state.get("running"))
        return scraping or enriching or syncing
    except Exception:
        return False


def busy_label() -> str:
    try:
        import dashboard
        labels = []
        if dashboard.state.get("running"):
            labels.append("scraping")
        if dashboard.enrich_state.get("running"):
            labels.append("domain enrichment")
        if dashboard.sync_state.get("running"):
            labels.append("CRM sync")
        return " + ".join(labels) if labels else "background task"
    except Exception:
        return "background task"


def on_closing():
    """Called when user clicks the X. Return False to cancel close."""
    if not is_busy():
        return True
    label = busy_label()
    try:
        win = webview.active_window() or webview.windows[0]
        msg = (f"A {label} is currently running. "
                "Closing now will stop it. Are you sure you want to close?")
        ok = win.evaluate_js(f"confirm({_js_str(msg)})")
        return bool(ok)
    except Exception:
        return True


def _js_str(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


def main():
    _set_windows_app_id()

    port = 5000
    if is_already_running(port):
        url = f"http://127.0.0.1:{port}"
    else:
        port = find_free_port(5000)
        threading.Thread(target=start_flask, args=(port,),
                            daemon=True).start()
        if not wait_until_ready(port):
            print("ERROR: Flask did not start in time")
            sys.exit(1)
        url = f"http://127.0.0.1:{port}"

    icon_path = ROOT.parent / "crm" / "static" / "logo.ico"

    window = webview.create_window(
        title="Devox Lead Finder",
        url=url,
        width=1400,
        height=900,
        min_size=(1000, 700),
        resizable=True,
    )
    window.events.closing += on_closing

    if icon_path.exists():
        webview.start(icon=str(icon_path))
    else:
        webview.start()


if __name__ == "__main__":
    main()
