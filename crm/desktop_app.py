"""
Desktop launcher for the Devox CRM.
Starts the Flask app in a background thread and shows it in a native window.

Usage:
    python desktop_app.py
or double-click DevoxSales.bat (Windows).
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


def find_free_port(preferred: int = 5001) -> int:
    """Use the preferred port if available, else any free port."""
    for port in [preferred, preferred + 1, preferred + 2, 0]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return s.getsockname()[1]
        except OSError:
            continue
    return preferred


def is_already_running(port: int) -> bool:
    """Check if our Flask app is already serving on this port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect(("127.0.0.1", port))
            return True
    except OSError:
        return False


def start_flask(port: int):
    """Run Flask in current thread (called from background thread)."""
    # Silence Flask dev server logs (we have our own UI)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    import app as crm_app
    crm_app.app.run(host="127.0.0.1", port=port,
                     debug=False, threaded=True, use_reloader=False)


def wait_until_ready(port: int, timeout: float = 10.0) -> bool:
    """Poll until Flask is accepting connections."""
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


def main():
    port = 5001
    if is_already_running(port):
        # Reuse existing instance — common when developer also has app.py running
        url = f"http://127.0.0.1:{port}"
    else:
        port = find_free_port(5001)
        threading.Thread(target=start_flask, args=(port,),
                            daemon=True).start()
        if not wait_until_ready(port):
            print("ERROR: Flask did not start in time")
            sys.exit(1)
        url = f"http://127.0.0.1:{port}"

    icon_path = ROOT / "static" / "logo.ico"
    window_kwargs = {
        "title": "Devox Sales",
        "url": url,
        "width": 1400,
        "height": 900,
        "min_size": (1000, 700),
        "resizable": True,
    }
    webview.create_window(**window_kwargs)
    # Only pass icon if a .ico file exists (PNG not accepted on Windows)
    if icon_path.exists():
        webview.start(icon=str(icon_path))
    else:
        webview.start()


if __name__ == "__main__":
    main()
