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


REFRESH_JS = r"""
(function() {
  // F5, Ctrl+R, Cmd+R → reload
  document.addEventListener('keydown', function(e) {
    if (e.key === 'F5' ||
        ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'r')) {
      e.preventDefault();
      window.location.reload();
    }
  }, true);

  // Floating reload button (top-right, only inside the desktop wrapper).
  // We mark the body so the in-app CSS/JS knows it's running in the
  // desktop client and can adapt later if needed.
  document.documentElement.setAttribute('data-devox-desktop', '1');
  function addBtn() {
    if (document.getElementById('__devox_reload')) return;
    var b = document.createElement('button');
    b.id = '__devox_reload';
    b.title = 'Reload (F5 / Ctrl+R)';
    b.textContent = '↻';
    b.style.cssText = (
      'position:fixed;top:10px;right:10px;z-index:99999;' +
      'width:34px;height:34px;border-radius:50%;border:0;' +
      'background:rgba(37,99,235,0.85);color:#fff;font-size:20px;' +
      'cursor:pointer;line-height:1;display:flex;align-items:center;' +
      'justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.4);' +
      'opacity:0.4;transition:opacity 0.2s;'
    );
    b.onmouseenter = function(){ b.style.opacity = '1'; };
    b.onmouseleave = function(){ b.style.opacity = '0.4'; };
    b.onclick = function(){ window.location.reload(); };
    document.body.appendChild(b);
  }
  if (document.body) addBtn();
  else document.addEventListener('DOMContentLoaded', addBtn);
})();
"""


def _on_loaded(window):
    """Called by pywebview after the page finishes loading.
    Re-injects the refresh button + keybinds on every navigation.
    """
    try:
        window.evaluate_js(REFRESH_JS)
    except Exception:
        pass


def main():
    _set_windows_app_id()
    url = get_crm_url()
    icon_path = ROOT / "static" / "logo.ico"

    window = webview.create_window(
        title="Devox Sales",
        url=url,
        width=1400,
        height=900,
        min_size=(1000, 700),
        resizable=True,
    )
    # Re-inject our keybinds + floating reload button after every page load
    # (covers login → app navigation, full reloads, etc.)
    window.events.loaded += lambda: _on_loaded(window)

    if icon_path.exists():
        webview.start(icon=str(icon_path))
    else:
        webview.start()


if __name__ == "__main__":
    main()
