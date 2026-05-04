"""HTML/CSS/JS for the CRM workspace UI."""

INDEX_HTML = r"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Devox Sales">
<link rel="manifest" href="/static/manifest.json">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/static/icon-512.png">
<link rel="shortcut icon" href="/static/logo.ico">
<title>Devox Sales</title>
<style>
/* =============================================================
   Devox Sales — Design System
   ============================================================= */

:root {
  /* Surfaces (dark, near-black with slight blue tint) */
  --bg:        #0a0b0f;
  --surface:   #12141b;
  --surface-2: #1a1d26;
  --surface-3: #232733;
  --hover:     #1e222c;

  /* Borders */
  --border:        #232733;
  --border-strong: #2f3445;

  /* Text */
  --text:    #f4f5f7;
  --text-2:  #b6bac6;
  --text-3:  #7c818f;
  --text-4:  #555b6a;

  /* Brand accent (Devox electric blue) */
  --brand:        #4f7cff;
  --brand-hover:  #6c8fff;
  --brand-soft:   rgba(79, 124, 255, 0.12);
  --brand-text:   #a8bdff;

  /* Semantic */
  --success:      #2ecc71;
  --success-soft: rgba(46, 204, 113, 0.12);
  --warning:      #ffb547;
  --warning-soft: rgba(255, 181, 71, 0.12);
  --danger:       #ff5c6f;
  --danger-soft:  rgba(255, 92, 111, 0.12);
  --info:         #5cd0ff;
  --info-soft:    rgba(92, 208, 255, 0.12);

  /* Shadows */
  --shadow-1: 0 1px 2px rgba(0,0,0,0.2);
  --shadow-2: 0 4px 12px rgba(0,0,0,0.25);
  --shadow-3: 0 12px 32px rgba(0,0,0,0.4);

  /* Radii */
  --r-1:  4px;
  --r-2:  6px;
  --r-3:  10px;
  --r-4:  14px;
  --r-pill: 999px;

  /* Spacing scale (4px base) */
  --s-1: 4px;
  --s-2: 8px;
  --s-3: 12px;
  --s-4: 16px;
  --s-5: 24px;
  --s-6: 32px;

  /* Layout */
  --header-h: 52px;
  --sidebar-w: 232px;
  --bottom-tabs-h: 64px;
}

* { box-sizing: border-box; }
*:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

html, body { height: 100%; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text',
               'SF Pro Display', 'Inter', 'Segoe UI',
               'Helvetica Neue', Arial, sans-serif;
  font-feature-settings: 'cv11', 'ss01';
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  background: var(--bg);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;  /* prevent any accidental sideways scroll */
  -webkit-text-size-adjust: 100%;  /* don't auto-grow text */
}

a { color: var(--brand); text-decoration: none; }
a:hover { color: var(--brand-hover); }

/* ---------- Top bar (thin, iOS-inspired) ---------- */
.top {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--s-3);
  height: var(--header-h);
  padding: 0 var(--s-4);
  background: rgba(18, 20, 27, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 0.5px solid var(--border);
  z-index: 50;
}
.top h1 {
  margin: 0; display: flex; align-items: center; gap: var(--s-2);
  font-size: 13px; font-weight: 700; letter-spacing: -0.01em;
  width: calc(var(--sidebar-w) - var(--s-4));
}
.top h1 img {
  height: 18px; width: auto;
  filter: brightness(0) invert(1);
}
.top .top-title {
  font-size: 14px; font-weight: 600;
  color: var(--text);
  letter-spacing: -0.005em;
  flex: 0 0 auto;
}
.top .nav { display: none; }
.top .center-title { display: none; }
.top .spacer { flex: 1; }
.top .user-info {
  display: flex; align-items: center; gap: var(--s-2);
  font-size: 13px; color: var(--text-2);
}
.user-info .badge {
  padding: 4px 10px; background: var(--surface-3); border-radius: var(--r-pill);
  font-size: 12px; font-weight: 500;
}
.user-info .live {
  color: var(--text-3); font-size: 12px;
}
.user-info > a {
  color: var(--text-3); padding: 6px 10px; border-radius: var(--r-2);
  font-size: 12px; font-weight: 500; transition: all 0.12s;
}
.user-info > a:hover { color: var(--text); background: var(--hover); }
.target-badge {
  background: var(--surface-3); color: var(--text-2);
  padding: 4px 10px; border-radius: var(--r-pill);
  font-size: 12px; font-weight: 600;
}
.target-badge.met {
  background: var(--success-soft); color: var(--success);
}

/* ---------- User avatar + menu (desktop) ---------- */
.user-avatar {
  display: inline-flex;
  align-items: center; justify-content: center;
  width: 28px; height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand) 0%, #7c5dff 100%);
  color: white;
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}
.user-avatar.lg {
  width: 44px; height: 44px;
  font-size: 16px;
}
.user-avatar-img {
  position: absolute;
  inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 50%;
  pointer-events: none;
}
.avatar-wrap { position: relative; display: inline-flex; }
.user-menu-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; border: 0;
  color: var(--text-2);
  padding: 4px 6px 4px 4px;
  margin-left: 8px;
  border-radius: var(--r-pill);
  cursor: pointer;
  font-family: inherit; font-size: 13px; font-weight: 500;
  transition: background 0.12s;
}
.user-menu-btn:hover { background: var(--hover); color: var(--text); }
.user-menu-btn .user-name {
  max-width: 140px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.user-menu {
  position: fixed;
  top: calc(var(--header-h) + 6px);
  right: 16px;
  min-width: 240px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  padding: 8px;
  z-index: 60;
  display: none;
  animation: menuSlide 0.16s ease;
}
@keyframes menuSlide {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}
.user-menu.open { display: block; }
.user-menu-header {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px 14px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 6px;
}
.user-menu-name {
  font-size: 14px; font-weight: 600; color: var(--text);
  letter-spacing: -0.01em;
}
.user-menu-role {
  font-size: 12px; color: var(--text-3);
  text-transform: capitalize;
  margin-top: 2px;
}
.user-menu-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px; font-weight: 500;
  color: var(--text-2);
  text-decoration: none;
  cursor: pointer;
  transition: background 0.1s, color 0.1s;
}
.user-menu-item:hover {
  background: var(--hover);
  color: var(--text);
}
.user-menu-item .ic {
  display: inline-flex; align-items: center; justify-content: center;
  color: var(--text-3);
  flex-shrink: 0;
}
.user-menu-item:hover .ic { color: var(--brand); }
.user-menu-item.danger { color: var(--danger); }
.user-menu-item.danger:hover { background: var(--danger-soft); color: var(--danger); }
.user-menu-item.danger .ic { color: var(--danger); }
.user-menu-divider {
  height: 1px; background: var(--border);
  margin: 6px 0;
}

/* ---------- Layout ---------- */
.container {
  display: grid;
  grid-template-columns: var(--sidebar-w) 1fr;
  height: calc(100vh - var(--header-h));
}
.sidebar {
  padding: var(--s-3) 10px;
  border-right: 0.5px solid var(--border);
  overflow-y: auto;
  background: var(--surface);
  display: flex; flex-direction: column;
}

/* iOS-style sidebar navigation list */
.side-nav {
  display: flex; flex-direction: column;
  gap: 1px;
  margin-bottom: 4px;
}
.side-nav-item {
  display: flex; align-items: center; gap: 11px;
  padding: 7px 10px;
  border-radius: 7px;
  color: var(--text-2);
  font-size: 14px; font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  letter-spacing: -0.005em;
  transition: background 0.1s, color 0.1s;
  position: relative;
}
.side-nav-item:hover {
  background: var(--hover);
  color: var(--text);
}
.side-nav-item.active {
  background: var(--brand-soft);
  color: var(--brand-text);
  font-weight: 600;
}
.side-nav-item.active .side-nav-icon { color: var(--brand); }
.side-nav-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px;
  color: var(--text-3);
  flex-shrink: 0;
}
.side-nav-item:hover .side-nav-icon { color: var(--text); }
.side-nav-label { flex: 1; min-width: 0; }
.side-nav-item .nav-badge {
  margin-left: auto;
  margin-right: 2px;
}

.side-divider {
  height: 0.5px;
  background: var(--border);
  margin: 8px 4px;
}

.side-section-title {
  font-size: 10px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--text-4);
  padding: 8px 12px 6px;
  margin-top: 4px;
}
.main {
  padding: var(--s-5) var(--s-6);
  overflow-y: auto;
}
.main h2 {
  font-size: 22px; font-weight: 700;
  color: var(--text);
  margin: 0 0 18px;
  letter-spacing: -0.018em;
  text-transform: none;
}
.main h2:first-child { margin-top: 0; }

/* ---------- Buttons ---------- */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 6px; height: 36px; padding: 0 14px;
  background: var(--brand); color: white;
  border: 0; border-radius: var(--r-2);
  font-family: inherit; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: background 0.12s, transform 0.08s;
  white-space: nowrap;
}
.btn:hover { background: var(--brand-hover); }
.btn:active { transform: scale(0.98); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

.btn.secondary {
  background: var(--surface-3); color: var(--text);
}
.btn.secondary:hover { background: var(--border-strong); }

.btn.ghost {
  background: transparent; color: var(--text-2);
  border: 1px solid var(--border);
}
.btn.ghost:hover { background: var(--hover); color: var(--text); }

.btn.danger {
  background: var(--danger); color: white;
}
.btn.danger:hover { background: #ff7585; }

.btn.success {
  background: var(--success); color: white;
}
.btn.success:hover { background: #4dd884; }

.btn.lg { height: 44px; padding: 0 20px; font-size: 14px; }
.btn.sm { height: 28px; padding: 0 10px; font-size: 12px; }

/* ---------- Inputs ---------- */
select, input[type=text], input[type=number], input[type=date],
input[type=password], textarea {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  height: 36px;
  padding: 0 12px;
  border-radius: var(--r-2);
  font-family: inherit; font-size: 13px;
  width: 100%;
  transition: border-color 0.12s, background 0.12s;
}
input::placeholder, textarea::placeholder { color: var(--text-4); }
select:hover, input[type=text]:hover, input[type=number]:hover,
input[type=date]:hover, input[type=password]:hover, textarea:hover {
  border-color: var(--border-strong);
}
select:focus, input:focus, textarea:focus {
  outline: 0;
  border-color: var(--brand);
  background: var(--bg);
}
textarea {
  height: auto; padding: 10px 12px;
  resize: vertical; min-height: 72px; line-height: 1.5;
}
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%237c818f' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 32px;
}

.filter-group { margin-bottom: var(--s-3); }
.filter-group label {
  display: block; font-size: 11px;
  color: var(--text-3); margin-bottom: 6px;
  font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Toggle row (segmented) */
.toggle-row {
  display: flex; gap: 2px;
  background: var(--surface);
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: var(--r-2);
}
.toggle-row button {
  flex: 1; padding: 7px 10px;
  background: transparent;
  color: var(--text-3);
  border: 0; border-radius: var(--r-1);
  font-family: inherit; font-size: 12px; font-weight: 600;
  cursor: pointer; transition: all 0.12s;
}
.toggle-row button:hover { color: var(--text); }
.toggle-row button.active {
  background: var(--brand);
  color: white;
}

/* ---------- Sidebar status counts ---------- */
.status-counts {
  display: flex; flex-direction: column; gap: 2px;
}
.status-counts .row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; cursor: pointer;
  border-radius: var(--r-2); font-size: 13px;
  background: transparent;
  border-left: 3px solid transparent;
  transition: background 0.12s;
}
.status-counts .row:hover { background: var(--hover); }
.status-counts .row.active {
  background: var(--brand-soft); color: var(--text);
}
.status-counts .row .label { font-weight: 500; }
.status-counts .row .count {
  background: var(--surface-3); color: var(--text-2);
  padding: 1px 8px; border-radius: var(--r-pill);
  font-size: 11px; font-weight: 600; min-width: 24px; text-align: center;
}
.status-counts .row.active .count {
  background: rgba(255,255,255,0.15); color: white;
}
.status-counts .row.dot-new { border-left-color: var(--text-3); }
.status-counts .row.dot-called { border-left-color: var(--info); }
.status-counts .row.dot-reached { border-left-color: var(--info); }
.status-counts .row.dot-interested { border-left-color: var(--success); }
.status-counts .row.dot-not_interested { border-left-color: var(--danger); }
.status-counts .row.dot-follow_up { border-left-color: var(--warning); }
.status-counts .row.dot-closed_won { border-left-color: var(--success); }
.status-counts .row.dot-closed_lost { border-left-color: var(--danger); }
.status-counts .row.dot-disqualified { border-left-color: var(--text-4); }

.clear-filter-btn {
  font-size: 11px; color: var(--brand);
  cursor: pointer; background: transparent; border: 0;
  padding: 6px 0; font-weight: 600;
}
.clear-filter-btn:hover { color: var(--brand-hover); }

/* ---------- Table ---------- */
table {
  width: 100%; border-collapse: collapse; font-size: 13px;
}
th {
  text-align: left;
  padding: 10px 16px;
  background: var(--surface);
  color: var(--text-3);
  font-weight: 600; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.06em;
  position: sticky; top: 0; z-index: 1;
  border-bottom: 1px solid var(--border);
}
td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
tr.lead-row { cursor: pointer; transition: background 0.1s; }
tr.lead-row:hover td { background: var(--hover); }
tr.lead-row.selected td { background: var(--brand-soft); }

/* ---------- Badges ---------- */
.status-badge {
  display: inline-flex; align-items: center;
  padding: 3px 9px; border-radius: var(--r-pill);
  font-size: 11px; font-weight: 600;
  white-space: nowrap;
}
.s-new { background: var(--surface-3); color: var(--text-2); }
.s-called { background: var(--info-soft); color: var(--info); }
.s-reached { background: var(--info-soft); color: var(--info); }
.s-interested { background: var(--success-soft); color: var(--success); }
.s-not_interested { background: var(--danger-soft); color: var(--danger); }
.s-follow_up { background: var(--warning-soft); color: var(--warning); }
.s-closed_won { background: var(--success-soft); color: var(--success); }
.s-closed_lost { background: var(--danger-soft); color: var(--danger); }
.s-disqualified { background: var(--surface-3); color: var(--text-4); }

.op-badge {
  display: inline-flex; align-items: center;
  padding: 2px 8px; border-radius: var(--r-1);
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.04em;
}
.op-none      { background: var(--danger-soft); color: var(--danger); }
.op-facebook  { background: rgba(66,103,178,0.15); color: #6e8fdc; }
.op-instagram { background: rgba(228,64,95,0.15); color: #e4405f; }
.op-booking   { background: rgba(0,53,128,0.2); color: #5b8eef; }
.op-airbnb    { background: rgba(255,90,95,0.15); color: #ff7a82; }
.op-tripadvisor { background: rgba(0,170,108,0.15); color: #4cc99a; }
.op-link-in-bio { background: var(--surface-3); color: var(--text-2); }
.op-whatsapp  { background: rgba(37,211,102,0.15); color: #25d366; }
.op-other, .op-ota-aggregator {
  background: var(--warning-soft); color: var(--warning);
}

.assigned-pill {
  display: inline-flex; align-items: center;
  padding: 2px 9px; border-radius: var(--r-pill);
  background: var(--surface-3); color: var(--text-2);
  font-size: 11px; font-weight: 500;
}
.assigned-pill.unassigned {
  color: var(--text-4); font-style: italic;
}
.assigned-pill.mine {
  background: var(--brand-soft); color: var(--brand-text);
}

.multi-prop-badge {
  display: inline-flex; align-items: center;
  background: var(--warning-soft); color: var(--warning);
  padding: 1px 7px; border-radius: var(--r-pill);
  font-size: 10px; font-weight: 700;
  margin-left: 6px;
}

/* ---------- Property list inside lead detail ---------- */
.props-list {
  background: var(--surface); border-radius: var(--r-3);
  padding: 12px; border: 1px solid var(--border);
  border-left: 3px solid var(--warning);
}
.props-list .prop {
  padding: 10px 0; border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.props-list .prop:last-child { border-bottom: 0; }
.props-list .prop .name {
  font-weight: 600; color: var(--text);
}
.props-list .prop .meta {
  color: var(--text-3); font-size: 11px; margin-top: 2px;
}

.res-card {
  background: var(--surface); padding: 16px;
  border-radius: var(--r-3); cursor: pointer;
  border: 1px solid var(--border);
  transition: all 0.12s;
}
.res-card:hover {
  border-color: var(--brand); background: var(--hover);
}
.res-card.active {
  border-color: var(--brand);
  background: var(--brand-soft);
}
.res-card .title {
  font-weight: 600; font-size: 14px; color: var(--text);
}
.res-card .subtitle {
  font-size: 12px; color: var(--text-3); margin-top: 4px;
}

/* ---------- Markdown rendering ---------- */
.markdown-body {
  color: var(--text-2); line-height: 1.65; font-size: 14px;
}
.markdown-body h1 {
  font-size: 24px; margin: 0 0 16px; color: var(--text);
  font-weight: 700; letter-spacing: -0.01em;
  border-bottom: 1px solid var(--border); padding-bottom: 12px;
}
.markdown-body h2 {
  font-size: 18px; margin: 24px 0 12px; color: var(--text);
  font-weight: 600; text-transform: none; letter-spacing: -0.01em;
}
.markdown-body h3 {
  font-size: 15px; margin: 20px 0 8px; color: var(--text);
  font-weight: 600; text-transform: none; letter-spacing: 0;
}
.markdown-body p { margin: 10px 0; }
.markdown-body ul, .markdown-body ol { margin: 10px 0 10px 24px; }
.markdown-body li { margin: 4px 0; }
.markdown-body code {
  background: var(--surface); padding: 2px 6px;
  border-radius: var(--r-1); font-size: 12px;
  font-family: 'JetBrains Mono', Consolas, monospace;
  color: var(--brand-text);
}
.markdown-body pre {
  background: var(--surface); padding: 14px;
  border-radius: var(--r-3); overflow-x: auto;
  font-size: 12px;
  font-family: 'JetBrains Mono', Consolas, monospace;
  border: 1px solid var(--border);
}
.markdown-body pre code { background: transparent; padding: 0; color: var(--text); }
.markdown-body blockquote {
  border-left: 3px solid var(--brand);
  padding-left: 14px; color: var(--text-3);
  margin: 12px 0;
}
.markdown-body table { border-collapse: collapse; margin: 14px 0; }
.markdown-body th, .markdown-body td {
  border: 1px solid var(--border); padding: 8px 12px;
}
.markdown-body th { background: var(--surface); font-size: 12px; }
.markdown-body a { color: var(--brand); }
.markdown-body strong { color: var(--text); font-weight: 600; }
.markdown-body hr {
  border: 0; border-top: 1px solid var(--border); margin: 24px 0;
}

.empty {
  text-align: center; padding: 60px 20px;
  color: var(--text-4); font-size: 13px;
}

/* ---------- Leads toolbar ---------- */
.leads-toolbar {
  display: grid;
  grid-template-columns: 1fr 200px 200px auto;
  gap: var(--s-3);
  margin-bottom: var(--s-4);
  align-items: center;
}
.leads-toolbar input[type="text"] {
  height: 40px; font-size: 14px;
  padding-left: 36px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%237c818f' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: 12px center;
}

.fav-toggle-label {
  display: flex; align-items: center; gap: 8px;
  background: var(--surface);
  padding: 0 14px; height: 40px;
  border-radius: var(--r-2);
  border: 1px solid var(--border);
  cursor: pointer; user-select: none;
  font-size: 13px; color: var(--text-2);
  white-space: nowrap; transition: all 0.12s;
}
.fav-toggle-label:hover { border-color: var(--warning); color: var(--text); }
.fav-toggle-label input { cursor: pointer; accent-color: var(--warning); }

.leads-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: var(--s-3); gap: var(--s-3); flex-wrap: wrap;
}
.leads-header h2 {
  margin: 0 !important; font-size: 18px;
  text-transform: none; letter-spacing: -0.01em;
  color: var(--text); font-weight: 600;
}

/* Country filter chips (above the leads toolbar) */
.country-chips {
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-bottom: 12px;
}
.country-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px; border-radius: var(--r-1);
  font-size: 13px; font-weight: 600;
  cursor: pointer; user-select: none;
  background: var(--surface); color: var(--text);
  border: 1px solid var(--border);
  transition: all 0.12s;
}
.country-chip:hover {
  border-color: var(--brand); color: var(--text);
}
.country-chip.active {
  background: var(--brand); color: white; border-color: var(--brand);
}
.country-chip .flag { font-size: 15px; }
.country-chip .count {
  background: var(--surface-3); padding: 1px 7px;
  border-radius: var(--r-pill);
  font-size: 11px; color: var(--text-2);
}
.country-chip.active .count {
  background: rgba(255,255,255,0.25); color: white;
}

/* Quick filter pills */
.quick-filters {
  display: flex; gap: 6px; flex-wrap: wrap;
}
.quick-filter-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 11px; border-radius: var(--r-pill);
  font-size: 12px; font-weight: 600;
  cursor: pointer; user-select: none;
  background: var(--surface); color: var(--text-3);
  border: 1px solid var(--border);
  transition: all 0.12s;
}
.quick-filter-pill:hover {
  color: var(--text); border-color: var(--border-strong);
}
.quick-filter-pill .count {
  background: var(--surface-3); padding: 1px 7px;
  border-radius: var(--r-pill);
  font-size: 10px; color: var(--text-2);
}
.quick-filter-pill.active {
  background: var(--brand); color: white; border-color: var(--brand);
}
.quick-filter-pill.active .count {
  background: rgba(255,255,255,0.25); color: white;
}

.action-btn {
  background: var(--brand-soft); color: var(--brand-text);
  padding: 4px 10px; border-radius: var(--r-1);
  font-size: 11px; font-weight: 600;
  text-decoration: none;
}
.action-btn:hover { background: var(--brand); color: white; }

/* ---------- Side panel ---------- */
.panel-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.6);
  display: none; z-index: 100;
  backdrop-filter: blur(2px);
}
.panel-overlay.open { display: block; }
.side-panel {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: 480px; background: var(--surface);
  border-left: 1px solid var(--border);
  z-index: 101;
  transform: translateX(100%);
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  overflow-y: auto;
  box-shadow: var(--shadow-3);
}
.side-panel.open { transform: translateX(0); }
.panel-header {
  padding: 18px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between;
  align-items: flex-start; gap: 12px;
  position: sticky; top: 0;
  background: var(--surface); z-index: 1;
}
.panel-close {
  background: transparent; color: var(--text-3);
  border: 0; cursor: pointer;
  width: 32px; height: 32px; border-radius: var(--r-2);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; transition: all 0.12s;
}
.panel-close:hover { color: var(--text); background: var(--hover); }
.panel-body { padding: 20px; }
.panel-body h3 {
  font-size: 11px; text-transform: uppercase;
  color: var(--text-3); letter-spacing: 0.08em;
  margin: 24px 0 10px;
  font-weight: 600;
}
.panel-body h3:first-child { margin-top: 0; }
.panel-body .name {
  font-size: 20px; font-weight: 700; color: var(--text);
  letter-spacing: -0.01em;
}
.panel-body .meta {
  font-size: 13px; color: var(--text-3); margin-top: 4px;
}

.panel-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin: 16px 0 20px;
}
.panel-actions a {
  background: var(--brand); color: white;
  padding: 12px;
  border-radius: var(--r-2);
  text-align: center;
  font-size: 13px; font-weight: 600;
  text-decoration: none;
  display: flex; align-items: center;
  justify-content: center; gap: 6px;
  transition: all 0.12s;
}
.panel-actions a:hover { background: var(--brand-hover); }
.panel-actions a.wa { background: #25d366; }
.panel-actions a.wa:hover { background: #4be086; }
.panel-actions a.email { background: #8b5cf6; }
.panel-actions a.email:hover { background: #a78bfa; }
.panel-actions a.disabled {
  opacity: 0.3; pointer-events: none;
  background: var(--surface-3); color: var(--text-4);
}

.info-row {
  display: flex; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.info-row:last-of-type { border-bottom: 0; }
.info-row .label { color: var(--text-3); font-weight: 500; }
.info-row .value {
  color: var(--text); font-weight: 500;
  max-width: 60%; text-align: right; word-break: break-word;
}
.copy-btn {
  background: var(--surface-3); border: 0;
  color: var(--text-3);
  padding: 2px 8px; border-radius: var(--r-1);
  font-size: 11px; font-weight: 500;
  cursor: pointer; margin-left: 6px;
  transition: all 0.12s;
}
.copy-btn:hover { color: var(--text); background: var(--border-strong); }

.action-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin: 12px 0;
}
.action-row button {
  padding: 11px 8px;
  font-size: 12px; font-weight: 600;
  background: var(--surface);
  color: var(--text-2);
  border: 1px solid var(--border);
  border-radius: var(--r-2);
  cursor: pointer;
  transition: all 0.12s;
}
.action-row button:hover {
  background: var(--hover); color: var(--text);
  border-color: var(--border-strong);
}
.action-row button.active {
  background: var(--brand-soft); color: var(--brand-text);
  border-color: var(--brand);
}
.action-row button.active.no-answer {
  background: var(--warning-soft); color: var(--warning);
  border-color: var(--warning);
}
.action-row button.active.wrong-number {
  background: var(--danger-soft); color: var(--danger);
  border-color: var(--danger);
}

.save-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 14px;
  border-radius: var(--r-3);
  margin-top: 18px;
  position: sticky;
  bottom: 0;
}
.dirty-indicator {
  color: var(--warning); font-size: 11px; font-weight: 600;
  margin-bottom: 8px; display: none;
}
.dirty-indicator.show { display: block; }

.fav-star {
  background: transparent; border: 0;
  cursor: pointer;
  font-size: 18px; padding: 4px 8px;
  color: var(--text-4);
  transition: color 0.15s, transform 0.15s;
  border-radius: var(--r-1);
}
.fav-star:hover {
  color: var(--warning);
  transform: scale(1.15);
}
.fav-star.active { color: var(--warning); }
.fav-toggle { padding: 4px 8px; }

/* ---------- Activity timeline ---------- */
.timeline { margin-top: 8px; }
.timeline .item {
  padding: 12px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid var(--brand);
  border-radius: var(--r-2);
  margin-bottom: 8px;
  font-size: 13px;
}
.timeline .item .meta-line {
  color: var(--text-3);
  font-size: 11px; font-weight: 500;
  margin-bottom: 4px;
}
.timeline .item.action-status_change { border-left-color: var(--warning); }
.timeline .item.action-called { border-left-color: var(--info); }
.timeline .item.action-reached { border-left-color: var(--success); }
.timeline .item.action-note { border-left-color: #c084fc; }
.timeline .item.action-assigned { border-left-color: var(--warning); }
.timeline .item .actions {
  float: right; display: none; gap: 4px;
}
.timeline .item:hover .actions { display: inline-flex; }
.timeline .item .actions button {
  background: transparent; border: 0;
  color: var(--text-3); cursor: pointer;
  font-size: 11px; padding: 2px 6px;
  border-radius: var(--r-1);
}
.timeline .item .actions button:hover {
  color: var(--danger); background: var(--danger-soft);
}
.timeline .item.editing { background: var(--hover); }
.timeline .item textarea {
  width: 100%; min-height: 60px; margin-top: 6px;
}

/* ---------- Activity feed ---------- */
.feed-item {
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-3);
  margin-bottom: 8px;
  font-size: 13px;
}
.feed-item .meta-line {
  color: var(--text-3);
  font-size: 11px; font-weight: 500;
  margin-bottom: 4px;
}

.hidden { display: none !important; }

.notify {
  position: fixed; top: 70px; right: 20px;
  background: var(--success);
  color: white;
  padding: 12px 18px;
  border-radius: var(--r-3);
  font-size: 13px; font-weight: 600;
  z-index: 200;
  box-shadow: var(--shadow-3);
  animation: slideIn 0.22s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(20px); }
  to   { opacity: 1; transform: translateX(0); }
}
.notify.fade { opacity: 0; transition: opacity 0.5s; }

/* ---------- Daily plan ---------- */
.dp-card {
  background: var(--surface);
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: var(--r-3);
  margin-bottom: 12px;
}
.dp-card h3 {
  font-size: 13px; color: var(--text-3);
  margin: 0 0 8px;
  text-transform: uppercase; letter-spacing: 0.06em;
  font-weight: 600;
}
.dp-card .count {
  font-size: 32px; font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
  line-height: 1;
}
.dp-card .small {
  color: var(--text-3);
  font-size: 12px;
  margin-top: 6px;
}

/* ---------- Chat view ---------- */
.chat-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 0;
  height: calc(100vh - var(--header-h) - 48px);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}
.chat-sidebar {
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  overflow: hidden;
  background: var(--surface);
}
.chat-sidebar-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 18px;
  border-bottom: 1px solid var(--border);
}
.chat-sidebar-header h2 {
  font-size: 16px !important; font-weight: 700;
  text-transform: none; letter-spacing: -0.01em;
  color: var(--text);
}
.chat-list {
  flex: 1;
  overflow-y: auto;
}
.chat-row {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 18px;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: background 0.1s;
  background: transparent;
  border-left: 0; border-right: 0; border-top: 0;
  width: 100%; text-align: left;
  font-family: inherit;
  color: var(--text);
}
.chat-row:hover { background: var(--hover); }
.chat-row.active { background: var(--brand-soft); }
.chat-row .avatar-wrap {
  position: relative; flex-shrink: 0;
}
.chat-row .user-avatar {
  width: 38px; height: 38px; font-size: 13px;
}
.chat-row .chat-row-info { flex: 1; min-width: 0; }
.chat-row .chat-row-name {
  font-size: 14px; font-weight: 600;
  color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  letter-spacing: -0.005em;
}
.chat-row .chat-row-last {
  font-size: 12px; color: var(--text-3);
  margin-top: 2px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.chat-row .chat-row-meta {
  display: flex; flex-direction: column; align-items: flex-end;
  gap: 4px; flex-shrink: 0;
}
.chat-row .chat-row-time {
  font-size: 10px; color: var(--text-4);
  font-weight: 500;
}
.chat-row .chat-unread {
  background: var(--brand);
  color: white;
  font-size: 10px; font-weight: 700;
  min-width: 18px; height: 18px;
  border-radius: var(--r-pill);
  padding: 0 6px;
  display: inline-flex; align-items: center; justify-content: center;
}

.chat-thread {
  display: flex; flex-direction: column;
  height: 100%;
  overflow: hidden;
  background: var(--bg);
}
.chat-thread-empty {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-4);
  font-size: 14px;
  padding: 40px;
  text-align: center;
}
.chat-thread-header {
  padding: 14px 22px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  display: flex; align-items: center; gap: 12px;
}
.chat-thread-header .user-avatar {
  width: 36px; height: 36px; font-size: 13px;
}
.chat-thread-header .name {
  font-size: 15px; font-weight: 600;
  letter-spacing: -0.005em;
  color: var(--text);
}
.chat-thread-header .sub {
  font-size: 12px; color: var(--text-3);
  margin-top: 2px;
}
.chat-back-btn {
  display: none;
  background: transparent; border: 0;
  color: var(--text-2);
  width: 32px; height: 32px;
  border-radius: var(--r-2);
  cursor: pointer;
  align-items: center; justify-content: center;
}
.chat-edit-btn {
  background: transparent; border: 0;
  color: var(--text-3);
  width: 36px; height: 36px;
  border-radius: var(--r-2);
  cursor: pointer; flex-shrink: 0;
  display: inline-flex; align-items: center; justify-content: center;
  transition: background 0.12s, color 0.12s;
}
.chat-edit-btn:hover {
  background: var(--hover);
  color: var(--text);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px 18px 8px;
  display: flex; flex-direction: column;
  gap: 2px;
}

/* iMessage / Instagram-style bubbles
   - their messages: left aligned, gray bubble, avatar on the left
   - my messages: right aligned, blue bubble, no avatar
*/
.chat-msg {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin-top: 10px;
  max-width: 100%;
}
.chat-msg.same-author { margin-top: 2px; }
.chat-msg.mine {
  flex-direction: row-reverse;
}

/* Avatar shown only on the FIRST message of a streak from another
   author. Hidden for our own messages and for follow-up messages. */
.chat-msg-avatar { flex-shrink: 0; align-self: flex-end; }
.chat-msg-avatar .user-avatar {
  width: 28px; height: 28px; font-size: 11px;
}
.chat-msg.mine .chat-msg-avatar { display: none; }
.chat-msg.same-author .chat-msg-avatar { visibility: hidden; }

.chat-msg-body {
  display: flex; flex-direction: column;
  min-width: 0; max-width: 75%;
}
.chat-msg.mine .chat-msg-body { align-items: flex-end; }
.chat-msg:not(.mine) .chat-msg-body { align-items: flex-start; }

/* Author name + time only above the FIRST message of a streak,
   only for OTHER people. We don't bother showing our own name. */
.chat-msg-meta {
  display: flex; align-items: baseline; gap: 8px;
  margin: 0 4px 3px;
  font-size: 11px;
}
.chat-msg.mine .chat-msg-meta { display: none; }
.chat-msg.same-author .chat-msg-meta { display: none; }
.chat-msg-author {
  font-weight: 600;
  color: var(--text-2);
  letter-spacing: -0.005em;
}
.chat-msg-time {
  color: var(--text-4);
}

/* The actual bubble */
.chat-msg-text {
  font-size: 14px;
  line-height: 1.4;
  padding: 9px 13px;
  border-radius: 18px;
  word-wrap: break-word;
  white-space: pre-wrap;
  max-width: 100%;
}
.chat-msg:not(.mine) .chat-msg-text {
  background: var(--surface-2);
  color: var(--text);
  border-bottom-left-radius: 6px;
}
.chat-msg.mine .chat-msg-text {
  background: var(--brand);
  color: white;
  border-bottom-right-radius: 6px;
}
/* Tighter corner on continuation messages so a streak feels like
   a single chunk. */
.chat-msg.same-author:not(.mine) .chat-msg-text {
  border-top-left-radius: 6px;
}
.chat-msg.same-author.mine .chat-msg-text {
  border-top-right-radius: 6px;
}

/* When a message is JUST attachments (no text), strip the bubble */
.chat-msg-text:empty { display: none; }
.chat-day-divider {
  text-align: center;
  font-size: 11px; color: var(--text-4);
  font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.06em;
  margin: 14px 0 6px;
  position: relative;
}
.chat-day-divider::before, .chat-day-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 38%;
  height: 1px;
  background: var(--border);
}
.chat-day-divider::before { left: 0; }
.chat-day-divider::after { right: 0; }

.chat-composer {
  padding: 12px 18px;
  border-top: 1px solid var(--border);
  background: var(--surface);
  display: flex; flex-direction: column; gap: 8px;
}
.chat-composer-row {
  display: flex; align-items: flex-end; gap: 10px;
}
.chat-composer textarea {
  flex: 1;
  min-height: 40px;
  max-height: 120px;
  padding: 10px 14px;
  border-radius: var(--r-3);
  resize: none;
  background: var(--surface-2);
  border: 0;
  font-size: 14px;
  line-height: 1.4;
}
.chat-composer textarea:focus {
  background: var(--bg);
  box-shadow: 0 0 0 2px var(--brand-soft);
}
.chat-composer .icon-btn {
  flex-shrink: 0;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: var(--surface-3);
  color: var(--text-2);
  border: 0;
  display: inline-flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: background 0.12s, transform 0.08s;
}
.chat-composer .icon-btn:hover { background: var(--border-strong); color: var(--text); }
.chat-composer .icon-btn:active { transform: scale(0.95); }
.chat-composer .send-btn {
  flex-shrink: 0;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: var(--brand);
  color: white;
  border: 0;
  display: inline-flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: background 0.12s, transform 0.08s;
}
.chat-composer .send-btn:hover { background: var(--brand-hover); }
.chat-composer .send-btn:active { transform: scale(0.95); }
.chat-composer .send-btn:disabled {
  opacity: 0.4; cursor: not-allowed; transform: none;
}

/* Pending-attachment thumbnails inside the composer */
.composer-attachments {
  display: flex; gap: 8px; flex-wrap: wrap;
}
.composer-attachment {
  position: relative;
  width: 84px; height: 84px;
  border-radius: 10px; overflow: hidden;
  background: var(--surface-2);
  border: 1px solid var(--border);
}
.composer-attachment img {
  width: 100%; height: 100%; object-fit: cover; display: block;
}
.composer-attachment .remove {
  position: absolute; top: 4px; right: 4px;
  width: 22px; height: 22px;
  border-radius: 50%;
  background: rgba(0,0,0,0.7);
  color: white;
  display: inline-flex; align-items: center; justify-content: center;
  cursor: pointer; border: 0;
  font-size: 14px; line-height: 1;
}

/* Inline image attachments inside a chat message */
.chat-msg-attachments {
  display: flex; gap: 4px; flex-wrap: wrap;
  margin-top: 4px;
}
.chat-msg.mine .chat-msg-attachments { justify-content: flex-end; }
.chat-msg-attachment {
  max-width: 220px; max-height: 220px;
  border-radius: 14px; overflow: hidden;
  background: var(--surface-2); cursor: pointer;
  display: inline-block;
  border: 0; padding: 0;
}
.chat-msg-attachment img {
  display: block;
  max-width: 100%; max-height: 220px;
  object-fit: cover;
}

/* Lightbox for full-size image preview */
.image-lightbox {
  position: fixed; inset: 0; z-index: 300;
  background: rgba(0,0,0,0.92);
  display: flex; align-items: center; justify-content: center;
  cursor: zoom-out;
}
.image-lightbox img {
  max-width: 100%; max-height: 100%;
}

/* Online dot on avatars */
.avatar-wrap { position: relative; }
.online-dot {
  position: absolute;
  bottom: -1px; right: -1px;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--success);
  border: 2px solid var(--surface);
  display: none;
}
.avatar-wrap.online .online-dot { display: block; }

/* Top nav badge for Chat tab */
.nav-badge {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--brand);
  color: white;
  font-size: 10px; font-weight: 700;
  min-width: 18px; height: 18px;
  border-radius: var(--r-pill);
  padding: 0 6px;
  margin-left: 4px;
}

/* Bottom tab badge */
.tab-badge {
  position: absolute;
  top: -4px; right: -10px;
  background: var(--brand);
  color: white;
  font-size: 9px; font-weight: 700;
  min-width: 16px; height: 16px;
  border-radius: var(--r-pill);
  padding: 0 4px;
  display: inline-flex; align-items: center; justify-content: center;
  border: 1.5px solid var(--surface);
}

/* New DM picker */
.dm-picker {
  position: fixed; inset: 0; z-index: 200;
  background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
}
.dm-picker-inner {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  width: 420px; max-width: 100%;
  max-height: 70vh; overflow: hidden;
  display: flex; flex-direction: column;
}
.dm-picker-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}
.dm-picker-header h3 { margin: 0; font-size: 16px; font-weight: 600; }
.dm-picker-list {
  overflow-y: auto;
  padding: 8px;
}
.dm-picker-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.1s;
}
.dm-picker-row:hover { background: var(--hover); }
.dm-picker-row .name {
  font-size: 14px; font-weight: 500; color: var(--text);
}
.dm-picker-row .role {
  font-size: 12px; color: var(--text-3);
  margin-top: 2px;
}

/* Mobile chat tweaks */
@media (max-width: 768px) {
  /* Chat takes the entire viewport below the top bar, ignoring the
     main padding so the composer can sit flush at the bottom against
     the tab bar. */
  #view-chat {
    position: fixed;
    top: 48px;
    left: 0; right: 0;
    bottom: var(--bottom-tabs-h);
    padding: 0 !important;
    margin: 0;
    z-index: 5;
    background: var(--bg);
  }
  .chat-layout {
    grid-template-columns: 1fr;
    height: 100%;
    width: 100%;
    border-radius: 0;
    border: 0;
    margin: 0;
  }
  .chat-sidebar { border-right: 0; }
  .chat-sidebar.hidden-on-mobile { display: none; }
  .chat-thread.active-on-mobile { display: flex; }
  .chat-thread:not(.active-on-mobile) { display: none; }
  .chat-thread-header {
    padding: 10px 14px;
    background: rgba(18, 20, 27, 0.92);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 0.5px solid var(--border);
  }
  .chat-back-btn { display: inline-flex; }
  .chat-messages { padding: 14px 16px; }
  .chat-composer {
    padding: 10px 14px;
    border-top: 0.5px solid var(--border);
    background: rgba(18, 20, 27, 0.96);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    flex-shrink: 0;
  }
  .chat-composer textarea { font-size: 16px; }
}

/* ---------- Proposal view ---------- */
.proposal-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 18px;
  align-items: flex-start;
}
.proposal-form {
  display: flex; flex-direction: column;
  gap: 14px;
}
.proposal-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
}
.proposal-section-title {
  font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-3);
  margin-bottom: 14px;
}
.proposal-actions {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.proposal-actions .btn { height: 44px; }
.proposal-preview {
  background: white;
  border-radius: 14px;
  min-height: 600px;
  overflow: auto;
  border: 1px solid var(--border);
}
.proposal-preview-empty {
  color: var(--text-4);
  padding: 60px 20px;
  text-align: center;
  font-size: 14px;
}

/* Mobile proposal */
@media (max-width: 768px) {
  .proposal-layout {
    grid-template-columns: 1fr !important;
    gap: 12px;
  }
  .proposal-section {
    padding: 16px;
    border-radius: 12px;
  }
  .proposal-section input, .proposal-section select {
    height: 44px !important;
  }
  .proposal-actions {
    position: sticky; bottom: calc(var(--bottom-tabs-h) + 8px);
    z-index: 5;
    background: var(--bg);
    padding: 8px 0;
    margin-top: 4px;
  }
  .proposal-actions .btn { height: 48px; font-size: 15px; }
  .proposal-preview { min-height: 320px; }
}

/* ---------- Account view ---------- */
.account-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px;
  margin-bottom: 20px;
  max-width: 720px;
}
.account-head {
  display: flex; align-items: center; gap: 16px;
}
.account-name {
  font-size: 20px; font-weight: 700;
  color: var(--text);
  letter-spacing: -0.01em;
}
.account-meta {
  display: flex; align-items: center; gap: 8px;
  margin-top: 4px;
  font-size: 13px; color: var(--text-3);
}
.account-meta .dot { color: var(--text-4); }
.account-meta .role {
  text-transform: capitalize;
  background: var(--surface-3);
  padding: 2px 8px;
  border-radius: var(--r-pill);
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-2);
}
.account-regions {
  display: flex; align-items: center; gap: 10px;
  margin-top: 18px; padding-top: 18px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-2);
  flex-wrap: wrap;
}
.account-label {
  font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-3);
}

.account-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  margin-bottom: 14px;
  max-width: 720px;
  overflow: hidden;
}
.account-section-title {
  font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-3);
  padding: 14px 18px 6px;
}
.account-row {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 18px;
  cursor: pointer;
  text-decoration: none; color: inherit;
  border: 0; background: transparent;
  width: 100%;
  font-family: inherit;
  text-align: left;
  border-top: 1px solid var(--border);
  transition: background 0.1s;
}
.account-row:first-of-type { border-top: 0; }
.account-row:not(.static):hover { background: var(--hover); }
.account-row.static { cursor: default; }
.account-row .ic {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px;
  border-radius: 8px;
  background: var(--surface-3);
  color: var(--text-2);
  flex-shrink: 0;
}
.account-row.danger .ic {
  background: var(--danger-soft);
  color: var(--danger);
}
.account-row.danger .account-row-title { color: var(--danger); }
.account-row-text { flex: 1; min-width: 0; }
.account-row-title {
  font-size: 14px; font-weight: 500;
  color: var(--text);
  letter-spacing: -0.005em;
}
.account-row-sub {
  font-size: 12px; color: var(--text-3);
  margin-top: 2px;
}
.account-chevron { color: var(--text-4); }
.account-pill {
  font-size: 11px; font-weight: 600;
  padding: 3px 10px;
  border-radius: var(--r-pill);
  background: var(--surface-3); color: var(--text-3);
}
.account-pill.on {
  background: var(--success-soft); color: var(--success);
}

/* ---------- Admin ---------- */
.user-row {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-3);
  margin-bottom: 8px;
}
.user-row .name { flex: 1; font-size: 14px; }
.user-row .role {
  font-size: 11px; padding: 3px 10px;
  border-radius: var(--r-pill);
  background: var(--surface-3); color: var(--text-2);
  font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.05em;
}
.user-row .role.admin {
  background: var(--warning-soft); color: var(--warning);
}

/* ============================================================
   MOBILE  (max-width: 768px) — iOS-density, no overflow
   ============================================================ */
@media (max-width: 768px) {

  html, body { overflow-x: hidden; max-width: 100vw; }
  body { font-size: 15px; }

  /* iOS-style top bar: thinner, single row, no clutter */
  .top {
    height: 48px; padding: 0 12px; gap: 8px;
    flex-wrap: nowrap;
    background: var(--surface);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
  }
  .top .nav { display: none; }
  .top .center-title { display: none; }
  .top h1 { gap: 6px; }
  .top h1 img { height: 18px; }

  .top .user-info { font-size: 12px; gap: 4px; }
  /* Hide all desktop user-menu chrome; mobile uses More tab */
  .user-menu-btn,
  .user-menu,
  .target-badge { display: none !important; }
  #calls-today-badge { display: inline-flex !important;
    font-size: 10px; padding: 2px 8px; }
  #online-now { display: none; }
  #my-regions-badge { display: none !important; }

  /* Bottom tab bar — iOS-style with proper hit area */
  .bottom-tabs {
    display: flex !important;
    position: fixed; bottom: 0; left: 0; right: 0;
    background: rgba(18, 20, 27, 0.92);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-top: 0.5px solid var(--border-strong);
    z-index: 90;
    height: var(--bottom-tabs-h);
    padding-bottom: env(safe-area-inset-bottom, 0);
  }
  .bottom-tabs a {
    flex: 1;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    color: var(--text-4);
    text-decoration: none;
    font-size: 10px; font-weight: 500;
    gap: 2px; padding: 8px 0;
    cursor: pointer;
    transition: color 0.15s;
  }
  .bottom-tabs a .tab-icon {
    font-size: 22px; line-height: 1;
    display: inline-flex; align-items: center; justify-content: center;
    height: 24px;
  }
  .bottom-tabs a .tab-icon svg {
    stroke-width: 1.8;
  }
  .bottom-tabs a.active { color: var(--brand); }
  .bottom-tabs a.active .tab-icon svg { stroke-width: 2.2; }

  /* Layout */
  .container { grid-template-columns: 1fr !important; height: auto; }
  .sidebar { display: none !important; }
  /* Top title and logo behave fine on mobile, but the title gets too tight */
  .top h1 { width: auto; }
  .top .top-title { font-size: 13px; color: var(--text-3); }
  .main {
    padding: 0 16px;
    padding-bottom: calc(var(--bottom-tabs-h) + 16px);
    padding-top: 16px;
    overflow-y: auto;
    height: calc(100vh - 48px);
    width: 100%;
  }

  /* iOS-style large title for main views */
  .leads-header {
    margin: 0 0 14px;
    flex-direction: column; align-items: flex-start;
    gap: 4px;
  }
  .leads-header h2 {
    font-size: 28px !important; font-weight: 700;
    letter-spacing: -0.025em;
    margin: 0;
    color: var(--text);
  }
  .leads-header #lead-count {
    font-size: 13px !important;
    color: var(--text-3);
  }

  /* Search bar — pill-shaped, with icon prefix */
  .leads-toolbar {
    grid-template-columns: 1fr !important;
    gap: 10px;
    padding: 0;
    margin-bottom: 12px;
  }
  .leads-toolbar input[type="text"] {
    height: 40px;
    background: var(--surface-2);
    border: 0;
    border-radius: 10px;
    padding: 0 14px 0 38px;
    font-size: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%237c818f' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: 12px center;
  }
  /* Hide secondary filter inputs on mobile — they live in the drawer */
  .leads-toolbar select { display: none; }
  .leads-toolbar .fav-toggle-label { display: none; }

  /* Status filter pills — clean horizontal scroll, no edge bleed */
  .quick-filters {
    flex-wrap: nowrap !important;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 4px;
    scrollbar-width: none;
    margin-bottom: 14px;
  }
  .quick-filters::-webkit-scrollbar { display: none; }
  .quick-filter-pill {
    white-space: nowrap; flex-shrink: 0;
    height: 32px; padding: 0 12px;
    font-size: 13px; border-radius: var(--r-pill);
    border: 0;
    background: var(--surface-2);
  }
  .quick-filter-pill.active { background: var(--brand); }
  .quick-filter-pill .count {
    background: rgba(255,255,255,0.15);
    font-weight: 600;
  }
  .quick-filter-pill:not(.active) .count {
    background: var(--surface-3);
  }

  /* Hide the desktop table */
  table.leads-table { display: none !important; }
  .leads-cards {
    display: flex !important;
    flex-direction: column;
    gap: 1px;
    background: var(--border);
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--border);
  }

  /* Lead row — iOS contact-list density */
  .lead-card {
    background: var(--surface);
    border: 0;
    border-radius: 0;
    padding: 12px 14px;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    transition: background 0.1s;
  }
  .lead-card:active { background: var(--hover); }
  .lead-card .lc-top {
    display: flex; align-items: center; gap: 12px;
  }
  .lead-card .lc-star {
    font-size: 18px; color: var(--text-4);
    padding: 0; background: transparent; border: 0;
    cursor: pointer; flex-shrink: 0;
    -webkit-tap-highlight-color: transparent;
    line-height: 1; height: 22px; width: 22px;
  }
  .lead-card .lc-star.active { color: var(--warning); }
  .lead-card .lc-info { flex: 1; min-width: 0; }
  .lead-card .lc-name {
    font-weight: 600; font-size: 15px;
    color: var(--text);
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: -0.01em;
    line-height: 1.25;
  }
  .lead-card .lc-region {
    font-size: 12px; color: var(--text-3);
    margin-top: 1px;
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
  }
  /* On the row layout we keep only ONE status badge to the right */
  .lead-card .lc-badges {
    display: flex; gap: 6px;
    margin-top: 0;
    align-items: center;
    flex-shrink: 0;
  }
  /* Hide secondary chips inside the row to avoid clutter — they're
     visible inside the lead detail panel anyway */
  .lead-card .lc-badges .op-badge,
  .lead-card .lc-badges .assigned-pill { display: none; }
  /* The phone CTA row goes below */
  .lead-card .lc-phone {
    display: flex; align-items: center; gap: 8px;
    margin-top: 10px;
  }
  .lead-card .lc-phone a {
    flex: 1; background: var(--brand); color: white;
    text-decoration: none;
    padding: 9px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600; font-size: 14px;
    display: flex; align-items: center; justify-content: center;
    gap: 6px;
  }
  .lead-card .lc-phone a.wa {
    flex: 0 0 44px; background: #25d366;
    padding: 9px 0;
  }

  /* Full-screen lead detail panel */
  .side-panel {
    width: 100% !important;
    top: 0 !important;
    border-left: 0 !important;
    border-radius: 0 !important;
  }
  .panel-header { padding: 14px 16px; }
  .panel-body { padding: 16px; padding-bottom: 100px; }
  .panel-body .name { font-size: 22px; }

  .panel-actions a {
    padding: 12px 6px !important;
    font-size: 13px !important;
  }
  .action-row button {
    padding: 12px 6px !important;
    font-size: 13px !important;
  }
  #sp-note { font-size: 16px; min-height: 80px; }
  .save-bar {
    padding: 12px 16px;
    margin: 16px -16px -16px;
    border-radius: 0;
    border-left: 0; border-right: 0; border-bottom: 0;
    background: rgba(18, 20, 27, 0.96);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
  }
  .save-bar .btn {
    height: 46px !important;
    font-size: 15px !important;
  }

  /* Mobile filter button */
  .mobile-filter-btn {
    display: flex !important;
    align-items: center; gap: 6px;
    background: var(--surface-2);
    border: 0;
    color: var(--text-2);
    padding: 0 14px;
    height: 40px;
    border-radius: 10px;
    font-size: 13px; font-weight: 500;
    cursor: pointer;
    width: 100%;
    -webkit-tap-highlight-color: transparent;
  }

  /* Filter drawer (bottom sheet) */
  .filter-drawer {
    position: fixed; inset: 0; z-index: 150;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    display: none;
  }
  .filter-drawer.open { display: block; }
  .filter-drawer-inner {
    position: absolute; bottom: 0; left: 0; right: 0;
    background: var(--surface);
    border-top-left-radius: 18px;
    border-top-right-radius: 18px;
    padding: 8px 18px 36px;
    max-height: 85vh; overflow-y: auto;
  }
  .filter-drawer-inner::before {
    content: '';
    display: block;
    width: 36px; height: 5px;
    background: var(--border-strong);
    border-radius: 999px;
    margin: 6px auto 18px;
  }
  .filter-drawer-inner h3 {
    font-size: 18px; font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
    text-transform: none;
    margin: 0 0 16px; padding: 0;
    display: flex; justify-content: space-between; align-items: center;
  }
  .filter-drawer-inner .filter-group { margin-bottom: 16px; }
  .filter-drawer-inner select,
  .filter-drawer-inner input[type=text] {
    height: 44px; font-size: 16px;
    background: var(--surface-2); border: 0; border-radius: 10px;
  }
  .filter-drawer-close {
    background: var(--surface-3); border: 0;
    color: var(--text-2);
    width: 30px; height: 30px;
    border-radius: 999px;
    cursor: pointer;
    font-size: 14px;
    display: flex; align-items: center; justify-content: center;
    margin-left: auto;
  }

  /* More menu — iOS settings style */
  .more-header {
    display: flex; align-items: center; gap: 14px;
    padding: 8px 6px 18px;
  }
  .more-header-name {
    font-size: 18px; font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
  }
  .more-header-meta {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: var(--text-3);
    margin-top: 2px;
  }
  .more-header-meta .role {
    text-transform: capitalize;
    background: var(--surface-3);
    padding: 2px 8px;
    border-radius: var(--r-pill);
    font-size: 11px; font-weight: 600;
    color: var(--text-2);
  }
  .more-header-meta .dot { color: var(--text-4); }

  .more-list {
    background: var(--surface-2);
    border-radius: 12px;
    overflow: hidden;
  }
  .more-row {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 16px;
    background: transparent;
    border: 0;
    border-top: 1px solid var(--border);
    width: 100%;
    cursor: pointer;
    font-family: inherit; text-align: left;
    color: var(--text);
    -webkit-tap-highlight-color: transparent;
    transition: background 0.1s;
  }
  .more-row:first-child { border-top: 0; }
  .more-row:active { background: var(--hover); }
  .more-row .ic {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px;
    border-radius: 8px;
    background: var(--surface-3);
    color: var(--text-2);
    flex-shrink: 0;
  }
  .more-row.danger .ic {
    background: var(--danger-soft);
    color: var(--danger);
  }
  .more-row.danger .more-row-title { color: var(--danger); }
  .more-row-text {
    flex: 1; display: flex; flex-direction: column;
    min-width: 0;
  }
  .more-row-title {
    font-size: 15px; font-weight: 500;
    color: var(--text);
    letter-spacing: -0.005em;
  }
  .more-row-sub {
    font-size: 12px; color: var(--text-3);
    margin-top: 2px;
  }
  .more-chevron { color: var(--text-4); flex-shrink: 0; }

  /* Daily plan / proposal layout */
  #view-plan, #view-feed, #view-resources, #view-proposal, #view-admin {
    padding: 0;
  }
  #view-proposal > div { grid-template-columns: 1fr !important; }
  #view-resources > div { grid-template-columns: 1fr !important; }
  #view-plan > div { grid-template-columns: 1fr !important; }
  #prop-preview-area { min-height: 400px !important; }

  /* Notify toast — bottom, above tab bar */
  .notify {
    top: auto !important;
    bottom: calc(var(--bottom-tabs-h) + 16px + env(safe-area-inset-bottom, 0));
    right: 12px; left: 12px;
    text-align: center;
  }

  /* iOS: prevent autozoom */
  input[type=text], input[type=password], input[type=date],
  input[type=number], select, textarea {
    font-size: 16px !important;
  }

  /* Dim other view headings to match */
  #view-plan h2, #view-feed h2, #view-resources h2,
  #view-proposal h2, #view-admin h2 {
    font-size: 28px !important; font-weight: 700;
    letter-spacing: -0.025em;
    margin: 0 0 14px;
    text-transform: none;
    color: var(--text);
  }

  table { font-size: 14px; }
}

/* Hide bottom tabs on desktop */
.bottom-tabs { display: none; }
/* Hide leads-cards on desktop, show table */
.leads-cards { display: none; }
/* Hide mobile-only elements on desktop */
.mobile-filter-btn { display: none; }
.mobile-leads-header { display: none; }
.filter-drawer { display: none; }

/* Mobile leads header — iOS segmented control + filter button */
@media (max-width: 768px) {
  .mobile-leads-header {
    display: flex !important;
    gap: 8px;
    margin-bottom: 12px;
    align-items: stretch;
  }
  .mobile-tab-toggle {
    display: flex;
    flex: 1;
    background: var(--surface-2);
    border: 0;
    border-radius: 10px;
    padding: 2px;
    gap: 2px;
    min-width: 0;
  }
  .mobile-tab-toggle button {
    flex: 1;
    background: transparent;
    border: 0;
    color: var(--text-2);
    font-family: inherit;
    font-size: 13px; font-weight: 600;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center; justify-content: center;
    gap: 5px;
    -webkit-tap-highlight-color: transparent;
    transition: all 0.18s ease;
    min-width: 0;
  }
  .mobile-tab-toggle button.active {
    background: var(--surface);
    color: var(--text);
    box-shadow: 0 1px 3px rgba(0,0,0,0.3),
                0 0 0 0.5px rgba(255,255,255,0.05);
  }
  .mobile-tab-toggle button .lbl {
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .mobile-tab-toggle button .cnt {
    font-size: 10px; font-weight: 700;
    background: var(--surface-3);
    color: var(--text-3);
    padding: 1px 6px;
    border-radius: var(--r-pill);
    min-width: 18px; text-align: center;
    flex-shrink: 0;
  }
  .mobile-tab-toggle button.active .cnt {
    background: var(--brand);
    color: white;
  }
  .mobile-filter-btn-2 {
    display: flex;
    align-items: center; gap: 6px;
    background: var(--surface-2);
    border: 0;
    color: var(--text);
    padding: 0 14px;
    border-radius: 10px;
    font-size: 13px; font-weight: 500;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    position: relative;
    flex-shrink: 0;
  }
  .mobile-filter-btn-2.has-filters {
    background: var(--brand-soft);
    color: var(--brand);
  }
  .filter-count-badge {
    background: var(--brand);
    color: white;
    font-size: 10px; font-weight: 700;
    padding: 1px 6px;
    border-radius: var(--r-pill);
    min-width: 18px; text-align: center;
  }
  .leads-toolbar .mobile-filter-btn { display: none; }
}
</style>
</head>
<body>

<div class="top">
  <h1><img src="/static/logo.png" alt="Devox"></h1>
  <div class="top-title" id="top-title">Leads</div>
  <div class="spacer"></div>
  <div class="user-info">
    <span id="online-now" class="live"></span>
    <span id="my-regions-badge" class="target-badge"
          title="Regions assigned to you" style="display:none;cursor:pointer">
      <span id="my-regions-count">0</span> regions
    </span>
    <span id="calls-today-badge" class="target-badge">0/20 today</span>
    <button class="user-menu-btn" id="user-menu-btn" type="button">
      <span class="avatar-wrap">
        <span class="user-avatar" id="user-avatar" data-uid="{{ user.id }}"></span>
        <span class="online-dot"></span>
      </span>
      <span class="user-name">{{ user.full_name }}</span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round" style="opacity:0.5">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>
  </div>
</div>

<!-- User dropdown menu -->
<div class="user-menu" id="user-menu">
  <div class="user-menu-header">
    <span class="user-avatar lg" id="user-avatar-lg"></span>
    <div>
      <div class="user-menu-name">{{ user.full_name }}</div>
      <div class="user-menu-role">{{ user.role }}</div>
    </div>
  </div>
  <a href="#" class="user-menu-item" data-action="account">
    <span class="ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round"
         stroke-linejoin="round"><circle cx="12" cy="8" r="4"></circle>
         <path d="M4 21v-2a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v2"></path></svg></span>
    Account
  </a>
  <a href="/download" target="_blank" class="user-menu-item">
    <span class="ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round"
         stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
         <polyline points="7 10 12 15 17 10"></polyline>
         <line x1="12" y1="15" x2="12" y2="3"></line></svg></span>
    Download apps
  </a>
  <div class="user-menu-divider"></div>
  <a href="/logout" class="user-menu-item danger">
    <span class="ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round"
         stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
         <polyline points="16 17 21 12 16 7"></polyline>
         <line x1="21" y1="12" x2="9" y2="12"></line></svg></span>
    Sign out
  </a>
</div>

<!-- Bottom tab bar (mobile only) -->
<nav class="bottom-tabs">
  <a id="btab-leads" class="active" data-view="leads">
    <span class="tab-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round">
        <path d="M9 11H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
        <path d="M17 11h-2a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
        <path d="M9 21H7a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
        <path d="M17 21h-2a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
      </svg>
    </span><span>Leads</span>
  </a>
  <a id="btab-plan" data-view="plan">
    <span class="tab-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
    </span><span>My Day</span>
  </a>
  <a id="btab-chat" data-view="chat">
    <span class="tab-icon" style="position:relative">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <span class="tab-badge" id="btab-chat-badge" style="display:none">0</span>
    </span><span>Chat</span>
  </a>
  <a id="btab-proposal" data-view="proposal">
    <span class="tab-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
      </svg>
    </span><span>Proposal</span>
  </a>
  <a id="btab-more" data-view="more">
    <span class="tab-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round"
           stroke-linejoin="round">
        <circle cx="12" cy="12" r="1"></circle>
        <circle cx="19" cy="12" r="1"></circle>
        <circle cx="5" cy="12" r="1"></circle>
      </svg>
    </span><span>More</span>
  </a>
</nav>

<!-- Mobile filter drawer -->
<div class="filter-drawer" id="filter-drawer">
  <div class="filter-drawer-inner">
    <button class="filter-drawer-close" id="filter-drawer-close">✕</button>
    <h3>Filters</h3>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">View</label>
      <div class="toggle-row">
        <button id="m-t-mine" data-mine="1">My Leads</button>
        <button id="m-t-all" class="active" data-mine="0">All Leads</button>
      </div>
    </div>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">Region</label>
      <select id="m-filter-region"><option value="">All regions</option></select>
    </div>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">Assignee</label>
      <select id="m-filter-assignee"><option value="">All assignees</option></select>
    </div>
    <div class="filter-group">
      <label class="fav-toggle-label" style="width:100%">
        <input id="m-filter-fav" type="checkbox">
        <span>⭐ Favorites only</span>
      </label>
    </div>
    <button class="btn" style="width:100%;padding:14px;margin-top:10px"
            id="filter-drawer-apply">Show results</button>
  </div>
</div>

<div class="container">
  <aside class="sidebar">
    <!-- Primary navigation (replaces top nav on desktop) -->
    <nav class="side-nav">
      <a class="side-nav-item active" id="nav-leads" data-view="leads">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <path d="M9 11H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
          <path d="M17 11h-2a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
          <path d="M9 21H7a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
          <path d="M17 21h-2a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2z"></path>
        </svg></span>
        <span class="side-nav-label">Leads</span>
      </a>
      <a class="side-nav-item" id="nav-plan" data-view="plan">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg></span>
        <span class="side-nav-label">My Day</span>
      </a>
      <a class="side-nav-item" id="nav-chat" data-view="chat">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg></span>
        <span class="side-nav-label">Chat</span>
        <span class="nav-badge" id="nav-chat-badge" style="display:none">0</span>
      </a>
      <a class="side-nav-item" id="nav-feed" data-view="feed">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
        </svg></span>
        <span class="side-nav-label">Activity</span>
      </a>
      <a class="side-nav-item" id="nav-resources" data-view="resources">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
        </svg></span>
        <span class="side-nav-label">Resources</span>
      </a>
      <a class="side-nav-item" id="nav-proposal" data-view="proposal">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg></span>
        <span class="side-nav-label">Proposal</span>
      </a>
      <a class="side-nav-item" id="nav-admin" data-view="admin" style="display:none">
        <span class="side-nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
          <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"></path>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
        </svg></span>
        <span class="side-nav-label">Admin</span>
      </a>
    </nav>

    <div class="side-divider"></div>

    <div id="sidebar-leads">
      <div class="side-section-title">View</div>
      <div class="filter-group">
        <div class="toggle-row">
          <button id="t-mine" data-mine="1">My Leads</button>
          <button id="t-all" class="active" data-mine="0">All Leads</button>
        </div>
      </div>
      <div class="filter-group" id="my-regions-toggle-row" style="display:none">
        <label class="fav-toggle-label" style="width:100%">
          <input id="filter-my-regions" type="checkbox">
          <span>Only my regions (<span id="my-regions-list-inline">—</span>)</span>
        </label>
      </div>

      <div class="side-section-title">Status</div>
      <div class="status-counts" id="status-counts"></div>
    </div>

    <div id="sidebar-admin" class="hidden">
      <div class="side-section-title">Users</div>
      <div id="users-list"></div>
      <button class="btn" id="btn-new-user" style="width:100%; margin-top:10px">
        + Create user
      </button>
    </div>
  </aside>

  <main class="main">
    <!-- LEADS VIEW -->
    <div id="view-leads">
      <!-- Mobile-only header: All / My toggle + Filters button -->
      <div class="mobile-leads-header">
        <div class="mobile-tab-toggle">
          <button id="mt-all" class="active" data-mine="0">
            <span class="lbl">All Leads</span>
            <span class="cnt" id="mt-all-count"></span>
          </button>
          <button id="mt-mine" data-mine="1">
            <span class="lbl">My Leads</span>
            <span class="cnt" id="mt-mine-count"></span>
          </button>
        </div>
        <button class="mobile-filter-btn-2" id="mobile-filter-btn-2">
          <span>⚙️</span>
          <span>Filters</span>
          <span class="filter-count-badge" id="filter-count-badge" style="display:none">0</span>
        </button>
      </div>

      <div class="country-chips" id="country-chips"></div>

      <div class="leads-toolbar">
        <input id="filter-text-top" type="text"
                placeholder="Search leads...">
        <select id="filter-country-top">
          <option value="">🌍 All countries</option>
        </select>
        <select id="filter-region-top">
          <option value="">All regions</option>
        </select>
        <select id="filter-assignee-top">
          <option value="">All assignees</option>
        </select>
        <label class="fav-toggle-label">
          <input id="filter-fav-top" type="checkbox">
          <span>★ Favorites</span>
        </label>
      </div>

      <div class="leads-header">
        <h2 style="margin:0">Leads
          <span id="lead-count" style="color:#8b92a6;font-weight:400;font-size:13px"></span>
        </h2>
        <div class="quick-filters" id="quick-status-filters"></div>
      </div>

      <table class="leads-table">
        <thead><tr>
          <th>★</th><th>Status</th><th>Name</th><th>Country</th>
          <th>Region</th><th>Online</th>
          <th>Phone</th><th>Domain</th><th>Assigned</th>
        </tr></thead>
        <tbody id="leads-body">
          <tr><td colspan="9" class="empty">Loading...</td></tr>
        </tbody>
      </table>

      <!-- Mobile card list -->
      <div class="leads-cards" id="leads-cards">
        <div class="empty">Loading...</div>
      </div>
    </div>

    <!-- DAILY PLAN VIEW -->
    <div id="view-plan" class="hidden">
      <h2>My Day</h2>
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:12px">
        <div class="dp-card">
          <h3>📞 Calls Today</h3>
          <div class="count" id="dp-calls">0</div>
          <div class="small">Target: 20</div>
        </div>
        <div class="dp-card">
          <h3>📅 Follow Ups</h3>
          <div class="count" id="dp-followups">0</div>
          <div class="small">scheduled today</div>
        </div>
        <div class="dp-card">
          <h3>🆕 New Leads</h3>
          <div class="count" id="dp-newleads">0</div>
          <div class="small">assigned to you</div>
        </div>
      </div>

      <h2 style="margin-top:24px">📅 Follow Ups</h2>
      <div id="dp-followup-list"></div>

      <h2>🆕 New Leads</h2>
      <div id="dp-new-list"></div>
    </div>

    <!-- ACTIVITY FEED VIEW -->
    <div id="view-feed" class="hidden">
      <h2>Team Activity (Live)</h2>
      <div style="display:grid;
                   grid-template-columns: 2fr 1fr 1fr 1fr;
                   gap:8px; margin-bottom: 14px">
        <input id="feed-search" type="text"
               placeholder="🔍 Search by hotel name, salesperson, note...">
        <select id="feed-region"><option value="">All regions</option></select>
        <select id="feed-user"><option value="">All users</option></select>
        <select id="feed-action">
          <option value="">All actions</option>
          <option value="called">📞 Calls</option>
          <option value="note">📝 Notes</option>
          <option value="status_change">🔄 Status changes</option>
          <option value="assigned">👤 Assignments</option>
        </select>
      </div>
      <div id="feed-list">
        <div class="empty">Loading activity...</div>
      </div>
    </div>

    <!-- RESOURCES VIEW -->
    <div id="view-resources" class="hidden">
      <h2>Resources</h2>
      <div style="display:grid;grid-template-columns:280px 1fr;gap:18px">
        <div id="resources-list" style="display:flex;flex-direction:column;
              gap:8px"></div>
        <div id="resource-content" class="markdown-body" style="background:#1a1d27;
              padding: 20px 24px; border-radius:8px; min-height:400px;
              overflow-y:auto;">
          <div class="empty">Select a resource on the left</div>
        </div>
      </div>
    </div>

    <!-- PROPOSAL VIEW -->
    <div id="view-proposal" class="hidden">
      <h2>Proposal</h2>
      <div class="proposal-layout">
        <div class="proposal-form">
          <div class="proposal-section">
            <div class="proposal-section-title">Property</div>
            <div class="filter-group">
              <label>Pre-fill from lead</label>
              <select id="prop-lead-select">
                <option value="">— Manual entry —</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Property name</label>
              <input id="prop-name" type="text" placeholder="e.g. Hotel Cyclades">
            </div>
            <div class="filter-group">
              <label>Type</label>
              <select id="prop-type">
                <option value="villa">Villa / House</option>
                <option value="hotel">Hotel</option>
                <option value="apartments">Apartments / Studios</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Location</label>
              <input id="prop-location" type="text" placeholder="e.g. Naoussa, Paros">
            </div>
            <div class="filter-group">
              <label>Date</label>
              <input id="prop-date" type="text" placeholder="DD/MM/YYYY">
            </div>
          </div>

          <div class="proposal-section">
            <div class="proposal-section-title">Author</div>
            <div class="filter-group">
              <label>Names</label>
              <input id="prop-authors" type="text"
                     placeholder="Οδυσσέας Στάβερης & Γιώργος Σπύρου">
            </div>
            <div class="filter-group">
              <label>Phone</label>
              <input id="prop-phone" type="text" value="+30 694 792 0875">
            </div>
            <div class="filter-group">
              <label>Email</label>
              <input id="prop-email" type="text" value="info@devox.gr">
            </div>
          </div>

          <div class="proposal-section">
            <div class="proposal-section-title">Pricing</div>
            <div class="filter-group">
              <label>Option A</label>
              <input id="prop-price-a" type="text" value="€700 – €900">
            </div>
            <div class="filter-group">
              <label>Option B</label>
              <input id="prop-price-b" type="text" value="€1.500 – €2.000">
            </div>
          </div>

          <div class="proposal-actions">
            <button class="btn ghost" id="prop-preview">Preview</button>
            <button class="btn" id="prop-download">Download HTML</button>
          </div>
        </div>
        <div id="prop-preview-area" class="proposal-preview">
          <div class="proposal-preview-empty">
            Fill the form and click Preview to see the proposal here.
          </div>
        </div>
      </div>
    </div>

    <!-- CHAT VIEW -->
    <div id="view-chat" class="hidden">
      <div class="chat-layout">
        <aside class="chat-sidebar">
          <div class="chat-sidebar-header">
            <h2 style="margin:0">Chats</h2>
            <button class="btn ghost sm" id="btn-new-dm" type="button"
                    title="Start a direct message">+ New</button>
          </div>
          <div class="chat-list" id="chat-list">
            <div class="empty">Loading...</div>
          </div>
        </aside>
        <section class="chat-thread" id="chat-thread">
          <div class="chat-thread-empty">
            Select a conversation to start chatting
          </div>
        </section>
      </div>
    </div>

    <!-- ADMIN VIEW -->
    <div id="view-admin" class="hidden">
      <h2>User Management</h2>
      <div id="admin-users"></div>
    </div>

    <!-- ACCOUNT VIEW -->
    <div id="view-account" class="hidden">
      <h2>Account</h2>
      <div class="account-card">
        <div class="account-head">
          <span class="avatar-wrap" id="account-avatar-wrap">
            <span class="user-avatar lg" id="account-avatar"></span>
          </span>
          <div style="flex:1">
            <div class="account-name">{{ user.full_name }}</div>
            <div class="account-meta">
              <span>@{{ user.username }}</span>
              <span class="dot">·</span>
              <span class="role">{{ user.role }}</span>
            </div>
          </div>
          <input type="file" id="account-avatar-input" accept="image/*"
                 style="display:none">
          <button class="btn ghost sm" id="account-avatar-btn">
            Change photo
          </button>
        </div>
        <div id="account-regions-line" class="account-regions" style="display:none">
          <span class="account-label">Assigned regions</span>
          <span id="account-regions-list"></span>
        </div>
      </div>

      <div class="account-section">
        <div class="account-section-title">Security</div>
        <button class="account-row" id="acc-change-pw">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Change password</div>
            <div class="account-row-sub">At least 6 characters</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="account-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>

      <div class="account-section">
        <div class="account-section-title">Notifications</div>
        <button class="account-row" id="acc-toggle-push">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
               <path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Push notifications</div>
            <div class="account-row-sub" id="acc-push-sub">
              Get pinged for new messages and lead assignments
            </div>
          </div>
          <span class="account-pill" id="acc-push-pill">Off</span>
        </button>
        <button class="account-row" id="acc-test-push" style="display:none">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Send test notification</div>
            <div class="account-row-sub">Confirm this device receives pushes</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="account-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
        <button class="account-row" id="acc-reset-push" style="display:none">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
               <polyline points="23 4 23 10 17 10"></polyline>
               <polyline points="1 20 1 14 7 14"></polyline>
               <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
               </svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Reset notifications</div>
            <div class="account-row-sub">Re-subscribe this device with fresh keys</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="account-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
        <button class="account-row" id="acc-diagnose-push"
                style="display:none">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
               <circle cx="12" cy="12" r="10"></circle>
               <line x1="12" y1="8" x2="12" y2="12"></line>
               <line x1="12" y1="16" x2="12.01" y2="16"></line>
               </svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Push diagnostics</div>
            <div class="account-row-sub">Show server's last error from the push gateway</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="account-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
        <button class="account-row danger" id="acc-rotate-keys"
                style="display:none">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
               <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
               </svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Rotate VAPID keys (admin)</div>
            <div class="account-row-sub">Server-side reset for everyone — last resort if delivery keeps failing</div>
          </div>
        </button>
        <div class="account-row static" id="acc-push-help" style="display:none">
          <span class="ic" style="background:var(--warning-soft);color:var(--warning)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </span>
          <div class="account-row-text">
            <div class="account-row-title">How to allow notifications</div>
            <div class="account-row-sub" id="acc-push-help-text"></div>
          </div>
        </div>
        <div class="account-row static">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle>
               <polyline points="12 6 12 12 16 14"></polyline></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Live activity</div>
            <div class="account-row-sub">Real-time updates while the app is open</div>
          </div>
          <span class="account-pill on">On</span>
        </div>
      </div>

      <div class="account-section">
        <div class="account-section-title">Device & app info</div>
        <div class="account-row static">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Running mode</div>
            <div class="account-row-sub" id="acc-mode-sub">—</div>
          </div>
          <span class="account-pill" id="acc-mode-pill">—</span>
        </div>
        <div class="account-row static" id="acc-twa-warning" style="display:none">
          <span class="ic" style="background:var(--warning-soft);color:var(--warning)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
              <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </span>
          <div class="account-row-text">
            <div class="account-row-title">URL bar visible? Reinstall the app</div>
            <div class="account-row-sub">
              Android caches the trust check the first time you install.
              If you installed before the latest update, uninstall and
              reinstall from <b>/download/android</b> — that fixes both
              the URL bar and notifications.
            </div>
          </div>
        </div>
      </div>

      <div class="account-section">
        <a class="account-row" href="/download" target="_blank">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
               <polyline points="7 10 12 15 17 10"></polyline>
               <line x1="12" y1="15" x2="12" y2="3"></line></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Download apps</div>
            <div class="account-row-sub">Windows installer & Android APK</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="account-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </a>
        <a class="account-row danger" href="/logout">
          <span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
               <polyline points="16 17 21 12 16 7"></polyline>
               <line x1="21" y1="12" x2="9" y2="12"></line></svg></span>
          <div class="account-row-text">
            <div class="account-row-title">Sign out</div>
          </div>
        </a>
      </div>
    </div>
  </main>
</div>

<!-- Side panel -->
<div class="panel-overlay" id="panel-overlay"></div>
<aside class="side-panel" id="side-panel">
  <div class="panel-header">
    <div>
      <div class="name" id="sp-name">—</div>
      <div class="meta" id="sp-meta">—</div>
    </div>
    <button class="panel-close" id="sp-close">✕</button>
  </div>
  <div class="panel-body" id="sp-body"></div>
</aside>

<script>
const ME = {{ user|tojson }};
let allLeads = [];
let activeStatus = null;
let myMode = 0;
let favOnly = false;
let myRegionsOnly = 0;
let users = [];
let activeFilterRegion = '';
let activeFilterCountry = '';
let activeFilterAssignee = '';
let filterText = '';
let searchTimer = null;
let selectedPhone = null;
let currentView = 'leads';

const COUNTRY_FLAGS = {
  'Greece': '🇬🇷', 'Netherlands': '🇳🇱',
  'Italy': '🇮🇹', 'Spain': '🇪🇸', 'Portugal': '🇵🇹',
  'France': '🇫🇷', 'Germany': '🇩🇪', 'Croatia': '🇭🇷',
  'Cyprus': '🇨🇾', 'Turkey': '🇹🇷', 'United Kingdom': '🇬🇧',
};
function flagFor(country) { return COUNTRY_FLAGS[country] || '🌍'; }
// Region -> country map, populated from /api/regions/all
let REGION_COUNTRY = {};

// Render assigned-regions UI bits based on what the server gave us in ME.
function renderMyRegionsUI() {
  const regs = (ME.regions || []);
  const badge = document.getElementById('my-regions-badge');
  const cnt = document.getElementById('my-regions-count');
  const row = document.getElementById('my-regions-toggle-row');
  const inline = document.getElementById('my-regions-list-inline');
  if (regs.length) {
    if (badge) {
      badge.style.display = '';
      badge.title = 'Assigned regions: ' + regs.join(', ');
    }
    if (cnt) cnt.textContent = regs.length;
    if (row) row.style.display = '';
    if (inline) {
      inline.textContent = regs.length <= 2
        ? regs.join(', ')
        : regs.slice(0, 2).join(', ') + ' +' + (regs.length - 2);
    }
  } else {
    if (badge) badge.style.display = 'none';
    if (row) row.style.display = 'none';
  }
  // Clicking the badge toggles the "only my regions" filter
  if (badge) {
    badge.onclick = () => {
      const cb = document.getElementById('filter-my-regions');
      if (!cb) return;
      cb.checked = !cb.checked;
      cb.dispatchEvent(new Event('change'));
    };
  }
}
renderMyRegionsUI();

// ----------------- View switching -----------------
function setView(v, opts) {
  opts = opts || {};
  const pushHistory = opts.pushHistory !== false;
  if (v === 'more') {
    showMoreMenu();
    return;
  }
  // Push a history entry so the system back button navigates between
  // views inside the app instead of jumping back to /login. We only
  // push when the view actually changes.
  if (pushHistory && currentView !== v) {
    try {
      history.pushState({ view: v }, '', '#' + v);
    } catch (e) {}
  }
  currentView = v;
  for (const id of ['leads', 'plan', 'feed', 'admin', 'resources',
                     'proposal', 'account', 'chat']) {
    const view = document.getElementById('view-' + id);
    if (view) view.classList.toggle('hidden', id !== v);
    const link = document.getElementById('nav-' + id);
    if (link) link.classList.toggle('active', id === v);
    const btab = document.getElementById('btab-' + id);
    if (btab) btab.classList.toggle('active', id === v);
  }
  // Top bar title reflects the current view on desktop
  const TITLE_FOR = {
    leads: 'Leads', plan: 'My Day', chat: 'Chat',
    feed: 'Activity', resources: 'Resources',
    proposal: 'Proposal', account: 'Account', admin: 'Admin',
  };
  const titleEl = document.getElementById('top-title');
  if (titleEl) titleEl.textContent = TITLE_FOR[v] || '';
  // Bottom tab "More" stays inactive once we navigate elsewhere
  const btabMore = document.getElementById('btab-more');
  if (btabMore) btabMore.classList.remove('active');
  document.getElementById('sidebar-leads').classList.toggle('hidden', v !== 'leads');
  document.getElementById('sidebar-admin').classList.toggle('hidden', v !== 'admin');
  if (v === 'plan') refreshPlan();
  if (v === 'admin') refreshUsers();
  if (v === 'feed') loadRecentActivity();
  if (v === 'resources') loadResources();
  if (v === 'proposal') initProposalForm();
  if (v === 'account') refreshAccountView();
  if (v === 'chat') openChatView();
}

async function compressSquareAvatar(file, size = 320, quality = 0.82) {
  const img = await new Promise((resolve, reject) => {
    const im = new Image();
    im.onload = () => resolve(im);
    im.onerror = reject;
    im.src = URL.createObjectURL(file);
  });
  const minSide = Math.min(img.width, img.height);
  const sx = (img.width - minSide) / 2;
  const sy = (img.height - minSide) / 2;
  const canvas = document.createElement('canvas');
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, size, size);
  ctx.drawImage(img, sx, sy, minSide, minSide, 0, 0, size, size);
  URL.revokeObjectURL(img.src);
  return canvas.toDataURL('image/jpeg', quality);
}

function paintAccountAvatar() {
  const wrap = document.getElementById('account-avatar-wrap');
  const av = document.getElementById('account-avatar');
  if (!av) return;
  // Refresh from cache
  if (ME.avatar) avatarCache.set(ME.id, ME.avatar);
  av.textContent = initials(ME.full_name);
  // Remove old img if any
  const old = wrap.querySelector('.user-avatar-img');
  if (old) old.remove();
  if (ME.avatar) {
    const img = document.createElement('img');
    img.className = 'user-avatar-img lg';
    img.src = ME.avatar;
    wrap.appendChild(img);
  }
}

function paintDeviceInfo() {
  const p = detectPlatform();
  const pill = document.getElementById('acc-mode-pill');
  const sub = document.getElementById('acc-mode-sub');
  const warn = document.getElementById('acc-twa-warning');
  if (!pill || !sub) return;
  let label, detail, isFullApp;
  if (p.isTWA) {
    label = 'Android app';
    detail = 'Trusted Web Activity (no URL bar) — full app mode.';
    isFullApp = true;
  } else if (p.isStandalone && p.isAndroid) {
    label = 'Android (PWA)';
    detail = 'Installed as a Progressive Web App. Reinstall the APK from /download/android for full TWA mode.';
    isFullApp = false;
  } else if (p.isAndroid) {
    label = 'Android (browser)';
    detail = 'Open as installed app from the home screen icon for the best experience.';
    isFullApp = false;
  } else if (p.isIOS && p.isStandalone) {
    label = 'iPhone (Home Screen)';
    detail = 'Installed via "Add to Home Screen" — fullscreen mode.';
    isFullApp = true;
  } else if (p.isIOS) {
    label = 'iPhone (Safari)';
    detail = 'Tap Share → Add to Home Screen for the best experience.';
    isFullApp = false;
  } else if (p.isStandalone) {
    label = 'Desktop (PWA)';
    detail = 'Installed as a desktop PWA.';
    isFullApp = true;
  } else {
    label = 'Desktop (browser)';
    detail = 'Use the Windows installer for a native window — see Download.';
    isFullApp = true;  // not really a problem, just an option
  }
  pill.textContent = label;
  pill.className = isFullApp ? 'account-pill on' : 'account-pill';
  sub.textContent = detail;

  // Show the reinstall warning only when Android user thinks they
  // installed but the TWA didn't kick in
  if (warn) {
    warn.style.display = (p.isAndroid && p.isStandalone && !p.isTWA)
      ? '' : 'none';
  }
}

function refreshAccountView() {
  paintAccountAvatar();
  paintDeviceInfo();
  const regs = ME.regions || [];
  const line = document.getElementById('account-regions-line');
  const list = document.getElementById('account-regions-list');
  if (line && list) {
    if (regs.length) {
      line.style.display = '';
      list.innerHTML = regs.map(r =>
        `<span class="assigned-pill">${escapeHtml(r)}</span>`).join(' ');
    } else {
      line.style.display = 'none';
    }
  }
  const pwBtn = document.getElementById('acc-change-pw');
  if (pwBtn) pwBtn.onclick = () => openChangePasswordModal();
  if (typeof updatePushUI === 'function') updatePushUI();

  // Avatar upload
  const avBtn = document.getElementById('account-avatar-btn');
  const avInput = document.getElementById('account-avatar-input');
  if (avBtn && avInput) {
    avBtn.onclick = () => avInput.click();
    avInput.onchange = async (e) => {
      const file = (e.target.files || [])[0];
      if (!file) return;
      try {
        const dataUrl = await compressSquareAvatar(file);
        const r = await fetch('/api/me/avatar', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ data: dataUrl }),
        });
        if (r.ok) {
          ME.avatar = dataUrl;
          avatarCache.set(ME.id, dataUrl);
          paintAccountAvatar();
          notify('Profile photo updated');
        } else {
          let msg = 'Upload failed';
          try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
          notify(msg);
        }
      } catch (err) {
        notify('Could not read image');
      }
      avInput.value = '';
    };
  }
}

function showMoreMenu() {
  // iOS-style "More" sheet: profile header + sectioned list of rows
  const drawer = document.getElementById('filter-drawer');
  const inner = drawer.querySelector('.filter-drawer-inner');
  const av = initials(ME.full_name);
  const regs = (ME.regions || []).length;
  const opts = [
    { v: 'account', label: 'Account', sub: 'Profile, password',
      icon: '<circle cx="12" cy="8" r="4"></circle><path d="M4 21v-2a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v2"></path>' },
    { v: 'feed', label: 'Activity', sub: 'Live team activity',
      icon: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>' },
    { v: 'resources', label: 'Resources', sub: 'Sales playbook & guides',
      icon: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>' },
  ];
  if (ME.role === 'admin') {
    opts.push({ v: 'admin', label: 'Admin', sub: 'Manage users & regions',
      icon: '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>' });
  }
  opts.push({ v: '__download', label: 'Download apps', sub: 'Windows & Android',
    icon: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>' });

  inner.innerHTML = `
    <div class="more-header">
      <span class="user-avatar lg">${escapeHtml(av)}</span>
      <div class="more-header-text">
        <div class="more-header-name">${escapeHtml(ME.full_name || '')}</div>
        <div class="more-header-meta">
          <span class="role">${escapeHtml(ME.role || 'sales')}</span>
          ${regs ? `<span class="dot">·</span><span>${regs} regions</span>` : ''}
        </div>
      </div>
    </div>
    <div class="more-list">
      ${opts.map(o => `
        <button class="more-row" data-more="${o.v}">
          <span class="ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">${o.icon}</svg></span>
          <span class="more-row-text">
            <span class="more-row-title">${o.label}</span>
            ${o.sub ? `<span class="more-row-sub">${o.sub}</span>` : ''}
          </span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" class="more-chevron">
               <polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      `).join('')}
      <button class="more-row danger" data-more="__logout">
        <span class="ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round"
             stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
             <polyline points="16 17 21 12 16 7"></polyline>
             <line x1="21" y1="12" x2="9" y2="12"></line></svg></span>
        <span class="more-row-text">
          <span class="more-row-title">Sign out</span>
        </span>
      </button>
    </div>
  `;
  drawer.classList.add('open');
  // Backdrop click closes
  drawer.onclick = (e) => {
    if (e.target === drawer) {
      drawer.classList.remove('open');
      rebuildFilterDrawer();
    }
  };
  for (const b of inner.querySelectorAll('button[data-more]')) {
    b.onclick = () => {
      drawer.classList.remove('open');
      const v = b.dataset.more;
      if (v === '__logout') { window.location.href = '/logout'; return; }
      if (v === '__download') { window.open('/download', '_blank'); rebuildFilterDrawer(); return; }
      rebuildFilterDrawer();
      setView(v);
    };
  }
}

// ----------------- Self-service password change -----------------
function openChangePasswordModal() {
  let modal = document.getElementById('pw-modal');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'pw-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);'+
    'z-index:200;display:flex;align-items:center;justify-content:center;padding:20px';
  modal.innerHTML = `
    <div style="background:#14171f;border:1px solid #2a2f3d;border-radius:12px;
                width:420px;max-width:100%">
      <div style="padding:18px 22px;border-bottom:1px solid #2a2f3d;
                  display:flex;justify-content:space-between;align-items:center">
        <div style="font-size:17px;font-weight:700">🔑 Change password</div>
        <button id="pw-close" style="background:transparent;border:0;
                color:#8b92a6;font-size:22px;cursor:pointer;padding:4px 8px">✕</button>
      </div>
      <div style="padding:18px 22px">
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Current password</label>
          <input id="pw-current" type="password" autocomplete="current-password">
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">New password</label>
          <input id="pw-new" type="password" autocomplete="new-password">
          <div style="font-size:11px;color:#6b7280;margin-top:4px">
            At least 6 characters
          </div>
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Confirm new password</label>
          <input id="pw-confirm" type="password" autocomplete="new-password">
        </div>
        <div id="pw-error" style="color:#fca5a5;font-size:13px;
                  margin:8px 0;display:none"></div>
      </div>
      <div style="padding:14px 22px;border-top:1px solid #2a2f3d;
                  display:flex;justify-content:flex-end;gap:8px">
        <button class="btn secondary" id="pw-cancel">Cancel</button>
        <button class="btn" id="pw-save">Update password</button>
      </div>
    </div>`;
  document.body.appendChild(modal);

  function showErr(msg) {
    const el = document.getElementById('pw-error');
    el.textContent = msg;
    el.style.display = msg ? 'block' : 'none';
  }
  const close = () => modal.remove();
  document.getElementById('pw-close').onclick = close;
  document.getElementById('pw-cancel').onclick = close;
  modal.onclick = (e) => { if (e.target === modal) close(); };
  setTimeout(() => document.getElementById('pw-current').focus(), 50);

  async function submit() {
    showErr('');
    const cur = document.getElementById('pw-current').value;
    const nw = document.getElementById('pw-new').value;
    const cf = document.getElementById('pw-confirm').value;
    if (!cur || !nw || !cf) { showErr('All fields are required'); return; }
    if (nw !== cf) { showErr('New passwords do not match'); return; }
    if (nw.length < 6) { showErr('New password must be at least 6 characters'); return; }
    if (nw === cur) { showErr('New password must differ from current'); return; }
    const r = await fetch('/api/me/password', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ current_password: cur, new_password: nw }),
    });
    if (r.ok) {
      notify('Password updated');
      close();
    } else {
      let msg = 'Failed to update password';
      try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
      showErr(msg);
    }
  }
  document.getElementById('pw-save').onclick = submit;
  for (const id of ['pw-current','pw-new','pw-confirm']) {
    document.getElementById(id).onkeydown = (e) => {
      if (e.key === 'Enter') submit();
    };
  }
}
window.openChangePasswordModal = openChangePasswordModal;

for (const link of document.querySelectorAll('.side-nav-item, .bottom-tabs a')) {
  link.onclick = (e) => {
    e.preventDefault();
    setView(link.dataset.view);
  };
}

// User dropdown menu (desktop)
function initials(name) {
  return (name || '').trim().split(/\s+/)
    .slice(0, 2).map(s => s[0] || '').join('').toUpperCase() || '?';
}
const _avatarText = initials(ME.full_name);
for (const el of document.querySelectorAll('#user-avatar, #user-avatar-lg')) {
  if (el) el.textContent = _avatarText;
}
const userMenuBtn = document.getElementById('user-menu-btn');
const userMenu = document.getElementById('user-menu');
if (userMenuBtn && userMenu) {
  userMenuBtn.onclick = (e) => {
    e.stopPropagation();
    userMenu.classList.toggle('open');
  };
  document.addEventListener('click', (e) => {
    if (!userMenu.contains(e.target) && !userMenuBtn.contains(e.target)) {
      userMenu.classList.remove('open');
    }
  });
  for (const item of userMenu.querySelectorAll('.user-menu-item')) {
    const action = item.dataset.action;
    if (!action) continue;
    item.onclick = (e) => {
      e.preventDefault();
      userMenu.classList.remove('open');
      if (action === 'account') setView('account');
    };
  }
}

if (ME.role === 'admin') {
  document.getElementById('nav-admin').style.display = '';
}

// ----------------- Helpers -----------------
function escapeHtml(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

const STATUS_LABEL = {
  new: 'New', called: 'Called', reached: 'Reached',
  interested: 'Interested', not_interested: 'Not Interested',
  follow_up: 'Follow Up', closed_won: 'Won', closed_lost: 'Lost',
  disqualified: 'Disqualified',
};

function notify(msg) {
  const div = document.createElement('div');
  div.className = 'notify';
  div.textContent = msg;
  document.body.appendChild(div);
  setTimeout(() => { div.classList.add('fade'); }, 2500);
  setTimeout(() => { div.remove(); }, 3500);
}

// ----------------- Leads -----------------
async function refreshLeads() {
  const params = new URLSearchParams();
  if (myMode) params.set('mine', '1');
  if (myRegionsOnly) params.set('my_regions', '1');
  if (favOnly) params.set('favorites', '1');
  if (activeStatus) params.set('status', activeStatus);
  if (activeFilterCountry) params.set('country', activeFilterCountry);
  if (activeFilterRegion) params.set('region', activeFilterRegion);
  if (activeFilterAssignee) params.set('assigned_to', activeFilterAssignee);
  if (filterText) params.set('q', filterText);

  const r = await fetch('/api/leads?' + params.toString());
  const data = await r.json();
  allLeads = data.leads;

  const allStatuses = ['new','called','reached','interested','follow_up',
                        'not_interested','closed_won','closed_lost','disqualified'];

  // Sidebar quick stats (compact list)
  const statusEl = document.getElementById('status-counts');
  let html = '';
  if (activeStatus) {
    html += `<button class="clear-filter-btn" id="clear-status-filter">
      Clear status filter</button>`;
  }
  html += allStatuses.map(s => {
    const n = data.by_status[s] || 0;
    const cls = s === activeStatus ? 'row active' : 'row';
    return `<div class="${cls} dot-${s}" data-status="${s}">
      <span class="label">${STATUS_LABEL[s]}</span>
      <span class="count">${n}</span>
    </div>`;
  }).join('');
  statusEl.innerHTML = html;
  for (const row of statusEl.querySelectorAll('.row')) {
    row.onclick = () => {
      activeStatus = activeStatus === row.dataset.status ? null : row.dataset.status;
      refreshLeads();
    };
  }
  const clearBtn = document.getElementById('clear-status-filter');
  if (clearBtn) clearBtn.onclick = () => { activeStatus = null; refreshLeads(); };

  // Top quick status filter pills (more prominent)
  const quickEl = document.getElementById('quick-status-filters');
  if (quickEl) {
    quickEl.innerHTML = allStatuses.map(s => {
      const n = data.by_status[s] || 0;
      if (n === 0 && s !== activeStatus) return '';
      const cls = s === activeStatus
        ? `quick-filter-pill dot-${s} active`
        : `quick-filter-pill dot-${s}`;
      return `<span class="${cls}" data-status="${s}">
        ${STATUS_LABEL[s]}
        <span class="count">${n}</span>
      </span>`;
    }).join('');
    for (const pill of quickEl.querySelectorAll('.quick-filter-pill')) {
      pill.onclick = () => {
        activeStatus = activeStatus === pill.dataset.status ? null : pill.dataset.status;
        refreshLeads();
      };
    }
  }

  // Country chips (above toolbar). "All countries" plus one per country.
  const countryEl = document.getElementById('country-chips');
  const byCountry = data.by_country || [];
  if (countryEl) {
    if (byCountry.length <= 1 && !activeFilterCountry) {
      // Only one country present — chips don't add value, hide them.
      countryEl.style.display = 'none';
    } else {
      countryEl.style.display = '';
      countryEl.innerHTML =
        `<div class="country-chip ${!activeFilterCountry?'active':''}" data-c="">
           <span class="flag">🌍</span>All <span class="count">${data.total}</span>
         </div>` +
        byCountry.filter(c => c.country).map(c =>
          `<div class="country-chip ${activeFilterCountry===c.country?'active':''}" data-c="${escapeHtml(c.country)}">
             <span class="flag">${flagFor(c.country)}</span>${escapeHtml(c.country)} <span class="count">${c.count}</span>
           </div>`).join('');
      for (const ch of countryEl.querySelectorAll('.country-chip')) {
        ch.onclick = () => {
          const newC = ch.dataset.c || '';
          if (newC === activeFilterCountry) return;
          activeFilterCountry = newC;
          // If the active region doesn't belong to the chosen country, clear it
          if (activeFilterRegion && newC &&
              REGION_COUNTRY[activeFilterRegion] !== newC) {
            activeFilterRegion = '';
          }
          refreshLeads();
        };
      }
    }
  }

  // Country dropdown in toolbar (parity with chips, plus mobile-friendly)
  const cSel = document.getElementById('filter-country-top');
  if (cSel) {
    const cur = activeFilterCountry;
    cSel.innerHTML = `<option value="">🌍 All countries</option>` +
      byCountry.filter(c => c.country).map(c =>
        `<option value="${escapeHtml(c.country)}">${flagFor(c.country)} ${escapeHtml(c.country)} (${c.count})</option>`
      ).join('');
    cSel.value = cur;
  }

  // Region dropdown (top) — narrowed to active country if set.
  // When in My Leads mode, the placeholder shows "My regions" because
  // only the user's assigned regions appear here.
  const regSel = document.getElementById('filter-region-top');
  if (regSel) {
    const cur = regSel.value;
    const visibleRegions = activeFilterCountry
      ? data.by_region.filter(r =>
          (REGION_COUNTRY[r.region] || '') === activeFilterCountry)
      : data.by_region;
    const placeholder = myMode
      ? `📍 All my regions (${visibleRegions.length})`
      : '📍 All regions';
    regSel.innerHTML = `<option value="">${placeholder}</option>` +
      visibleRegions.map(r =>
        `<option value="${escapeHtml(r.region)}">${escapeHtml(r.region)} (${r.count})</option>`
      ).join('');
    regSel.value = cur;
  }

  updateMobileToggleCounts();
  updateActiveFilterBadge();
  renderLeads();
}

// Fetch the count for the OTHER mode (so the toggle button shows
// both numbers), without re-rendering the whole table.
async function updateMobileToggleCounts() {
  const myEl = document.getElementById('mt-mine-count');
  const allEl = document.getElementById('mt-all-count');
  if (!myEl || !allEl) return;
  // Current mode count is allLeads.length
  const currentCount = allLeads.length;
  if (myMode) myEl.textContent = currentCount;
  else allEl.textContent = currentCount;
  // Fetch the other side cheaply (same filters minus mine)
  try {
    const params = new URLSearchParams();
    if (!myMode) params.set('mine', '1');
    if (favOnly) params.set('favorites', '1');
    if (activeStatus) params.set('status', activeStatus);
    if (activeFilterRegion) params.set('region', activeFilterRegion);
    if (activeFilterAssignee) params.set('assigned_to', activeFilterAssignee);
    if (filterText) params.set('q', filterText);
    const r = await fetch('/api/leads?' + params.toString());
    if (!r.ok) return;
    const d = await r.json();
    if (myMode) allEl.textContent = d.total;
    else myEl.textContent = d.total;
  } catch {}
}

function updateActiveFilterBadge() {
  // Count the filters that are not in their default state
  let n = 0;
  if (favOnly) n++;
  if (activeStatus) n++;
  if (activeFilterCountry) n++;
  if (activeFilterRegion) n++;
  if (activeFilterAssignee) n++;
  if (filterText) n++;
  const btn = document.getElementById('mobile-filter-btn-2');
  const badge = document.getElementById('filter-count-badge');
  if (!btn || !badge) return;
  if (n > 0) {
    btn.classList.add('has-filters');
    badge.style.display = '';
    badge.textContent = n;
  } else {
    btn.classList.remove('has-filters');
    badge.style.display = 'none';
  }
}

function renderLeads() {
  const rows = allLeads;
  document.getElementById('lead-count').textContent = `(${rows.length} shown)`;
  const tbody = document.getElementById('leads-body');
  const cardsEl = document.getElementById('leads-cards');
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="9" class="empty">No leads match</td></tr>';
    if (cardsEl) cardsEl.innerHTML = '<div class="empty">No leads match</div>';
    return;
  }
  // Mobile cards
  if (cardsEl) {
    cardsEl.innerHTML = rows.map(l => {
      const op = (l.online_presence||'').toLowerCase() || 'none';
      const status = l.status || 'new';
      const phone = (l.phone||'');
      const waPhone = phone.replace(/[^\d+]/g,'').replace('+','').replace(/^00/,'');
      const starCls = l.is_favorite ? 'lc-star active' : 'lc-star';
      const starChar = l.is_favorite ? '★' : '☆';
      const propCount = l.property_count || 1;
      const propBadge = propCount > 1
        ? `<span class="multi-prop-badge">📦 ${propCount}</span>` : '';
      let assigned = '<span class="assigned-pill unassigned">unassigned</span>';
      if (l.assigned_to_name) {
        const cls = l.assigned_to === ME.id ? 'assigned-pill mine' : 'assigned-pill';
        assigned = `<span class="${cls}">${escapeHtml(l.assigned_to_name)}</span>`;
      }
      return `<div class="lead-card" data-phone="${escapeHtml(phone)}">
        <div class="lc-top">
          <button class="${starCls}" data-phone="${escapeHtml(phone)}" data-fav="${l.is_favorite?1:0}">${starChar}</button>
          <div class="lc-info">
            <div class="lc-name">${escapeHtml(l.name||'')}${propBadge}</div>
            <div class="lc-region">${flagFor(l.country || REGION_COUNTRY[l.region] || '')} ${escapeHtml(l.region||'')} • ${escapeHtml(l.category||'')}</div>
            <div class="lc-badges">
              <span class="status-badge s-${status}">${STATUS_LABEL[status]||status}</span>
              <span class="op-badge op-${op}">${escapeHtml(op)}</span>
              ${assigned}
            </div>
          </div>
        </div>
        <div class="lc-phone">
          <a href="tel:${escapeHtml(phone)}" onclick="event.stopPropagation()">📞 ${escapeHtml(phone)}</a>
          ${waPhone ? `<a class="wa" target="_blank" href="https://wa.me/${waPhone}" onclick="event.stopPropagation()">💬</a>` : ''}
        </div>
      </div>`;
    }).join('');
    for (const card of cardsEl.querySelectorAll('.lead-card')) {
      card.onclick = (e) => {
        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' ||
            e.target.closest('a') || e.target.closest('button')) return;
        openPanel(card.dataset.phone);
      };
    }
    for (const star of cardsEl.querySelectorAll('.lc-star')) {
      star.onclick = async (e) => {
        e.stopPropagation();
        const ph = star.dataset.phone;
        const isCurrentlyFav = star.dataset.fav === '1';
        const method = isCurrentlyFav ? 'DELETE' : 'POST';
        await fetch('/api/lead/' + encodeURIComponent(ph) + '/favorite', { method });
        star.dataset.fav = isCurrentlyFav ? '0' : '1';
        star.textContent = isCurrentlyFav ? '☆' : '★';
        star.classList.toggle('active', !isCurrentlyFav);
        const lead = allLeads.find(x => x.phone === ph);
        if (lead) lead.is_favorite = isCurrentlyFav ? 0 : 1;
        if (favOnly && isCurrentlyFav) refreshLeads();
      };
    }
  }
  tbody.innerHTML = rows.map(l => {
    const op = (l.online_presence||'').toLowerCase() || 'none';
    const status = l.status || 'new';
    const phone = (l.phone||'');
    const sug = l.domain_suggestion || '';
    const grA = l.domain_gr_available;
    let domain = '<span style="color:#6b7280">—</span>';
    if (sug) domain = `<span style="color:#4ade80">✓ ${escapeHtml(sug)}</span>`;
    else if (grA === 'no') domain = '<span style="color:#6b7280">taken</span>';

    let assigned = '<span class="assigned-pill unassigned">unassigned</span>';
    if (l.assigned_to_name) {
      const cls = l.assigned_to === ME.id ? 'assigned-pill mine' : 'assigned-pill';
      assigned = `<span class="${cls}">${escapeHtml(l.assigned_to_name)}</span>`;
    }
    const rowClass = phone === selectedPhone ? 'lead-row selected' : 'lead-row';
    const starCls = l.is_favorite ? 'fav-star active' : 'fav-star';
    const starChar = l.is_favorite ? '★' : '☆';
    const propCount = l.property_count || 1;
    const propBadge = propCount > 1
      ? `<span class="multi-prop-badge" title="Owner has ${propCount} properties">📦 ${propCount}</span>`
      : '';
    const country = l.country || REGION_COUNTRY[l.region] || '';
    const countryCell = country
      ? `<span title="${escapeHtml(country)}" style="font-size:16px">${flagFor(country)}</span>`
      : '<span style="color:#6b7280">—</span>';
    return `<tr class="${rowClass}" data-phone="${escapeHtml(phone)}">
       <td><button class="${starCls}" data-phone="${escapeHtml(phone)}" data-fav="${l.is_favorite?1:0}">${starChar}</button></td>
       <td><span class="status-badge s-${status}">${STATUS_LABEL[status]||status}</span></td>
       <td><b>${escapeHtml(l.name||'')}</b>${propBadge}<br>
           <span style="color:#8b92a6;font-size:11px">${escapeHtml(l.category||'')}</span></td>
       <td>${countryCell}</td>
       <td>${escapeHtml(l.region||'')}</td>
       <td><span class="op-badge op-${op}">${escapeHtml(op)}</span></td>
       <td><a href="tel:${escapeHtml(phone)}" style="color:#60a5fa" onclick="event.stopPropagation()">${escapeHtml(phone)}</a></td>
       <td>${domain}</td>
       <td>${assigned}</td>
    </tr>`;
  }).join('');
  for (const tr of tbody.querySelectorAll('tr.lead-row')) {
    tr.onclick = (e) => {
      if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') return;
      openPanel(tr.dataset.phone);
    };
  }
  // Favorite star toggles
  for (const star of tbody.querySelectorAll('.fav-star')) {
    star.onclick = async (e) => {
      e.stopPropagation();
      const ph = star.dataset.phone;
      const isCurrentlyFav = star.dataset.fav === '1';
      const method = isCurrentlyFav ? 'DELETE' : 'POST';
      await fetch('/api/lead/' + encodeURIComponent(ph) + '/favorite',
                    { method });
      // Optimistic update
      star.dataset.fav = isCurrentlyFav ? '0' : '1';
      star.textContent = isCurrentlyFav ? '☆' : '★';
      star.classList.toggle('active', !isCurrentlyFav);
      // Update local cache
      const lead = allLeads.find(x => x.phone === ph);
      if (lead) lead.is_favorite = isCurrentlyFav ? 0 : 1;
      // If favOnly filter is on, refresh to drop unfavored rows
      if (favOnly && isCurrentlyFav) refreshLeads();
    };
  }
}

function setMyMode(v) {
  myMode = v ? 1 : 0;
  document.getElementById('t-mine').classList.toggle('active', myMode === 1);
  document.getElementById('t-all').classList.toggle('active', myMode === 0);
  const mtMine = document.getElementById('mt-mine');
  const mtAll = document.getElementById('mt-all');
  if (mtMine) mtMine.classList.toggle('active', myMode === 1);
  if (mtAll) mtAll.classList.toggle('active', myMode === 0);
  refreshLeads();
}
document.getElementById('t-mine').onclick = () => setMyMode(1);
document.getElementById('t-all').onclick = () => setMyMode(0);
const mtMineEl = document.getElementById('mt-mine');
const mtAllEl = document.getElementById('mt-all');
if (mtMineEl) mtMineEl.onclick = () => setMyMode(1);
if (mtAllEl) mtAllEl.onclick = () => setMyMode(0);

// Wire the second mobile filter button (in the new mobile-leads-header)
const mobFilterBtn2 = document.getElementById('mobile-filter-btn-2');
if (mobFilterBtn2) {
  mobFilterBtn2.onclick = () => {
    rebuildFilterDrawer();
    document.getElementById('filter-drawer').classList.add('open');
  };
}
document.getElementById('filter-text-top').oninput = e => {
  filterText = e.target.value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(refreshLeads, 250);
};
const _filterCountryTop = document.getElementById('filter-country-top');
if (_filterCountryTop) {
  _filterCountryTop.onchange = e => {
    activeFilterCountry = e.target.value;
    if (activeFilterRegion && activeFilterCountry &&
        REGION_COUNTRY[activeFilterRegion] !== activeFilterCountry) {
      activeFilterRegion = '';
    }
    refreshLeads();
  };
}
document.getElementById('filter-region-top').onchange = e => {
  activeFilterRegion = e.target.value;
  refreshLeads();
};
document.getElementById('filter-assignee-top').onchange = e => {
  activeFilterAssignee = e.target.value; refreshLeads();
};
document.getElementById('filter-fav-top').onchange = e => {
  favOnly = e.target.checked; refreshLeads();
};

// "Only my regions" filter (sidebar toggle)
const filterMyRegionsCb = document.getElementById('filter-my-regions');
if (filterMyRegionsCb) {
  filterMyRegionsCb.onchange = e => {
    myRegionsOnly = e.target.checked ? 1 : 0;
    // Visual feedback on the badge in the top bar
    const badge = document.getElementById('my-regions-badge');
    if (badge) badge.classList.toggle('met', !!myRegionsOnly);
    refreshLeads();
  };
}

// ----------------- Mobile filter drawer -----------------
function rebuildFilterDrawer() {
  const inner = document.querySelector('#filter-drawer .filter-drawer-inner');
  if (!inner) return;
  const STATUS_LABEL_LOCAL = STATUS_LABEL;
  const STATUS_KEYS = ['new','called','reached','interested','follow_up',
                        'not_interested','closed_won','closed_lost','disqualified'];
  inner.innerHTML = `
    <button class="filter-drawer-close" id="filter-drawer-close">✕</button>
    <h3 style="display:flex;justify-content:space-between;align-items:center">
      <span>Filters</span>
      <button id="filter-drawer-clear" style="background:transparent;border:0;
              color:#60a5fa;font-size:12px;cursor:pointer;padding:0">
        Clear all
      </button>
    </h3>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">View</label>
      <div class="toggle-row">
        <button id="m-t-all" data-mine="0" class="${!myMode?'active':''}">All Leads</button>
        <button id="m-t-mine" data-mine="1" class="${myMode?'active':''}">My Leads</button>
      </div>
    </div>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">Status</label>
      <select id="m-filter-status">
        <option value="">Any status</option>
        ${STATUS_KEYS.map(k => `
          <option value="${k}" ${activeStatus === k ? 'selected' : ''}>
            ${STATUS_LABEL_LOCAL[k] || k}
          </option>`).join('')}
      </select>
    </div>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">Region</label>
      <select id="m-filter-region"></select>
    </div>
    <div class="filter-group">
      <label style="font-size:11px;color:#8b92a6">Assignee</label>
      <select id="m-filter-assignee"></select>
    </div>
    <div class="filter-group">
      <label class="fav-toggle-label" style="width:100%">
        <input id="m-filter-fav" type="checkbox" ${favOnly?'checked':''}>
        <span>⭐ Favorites only</span>
      </label>
    </div>
    <button class="btn" style="width:100%;padding:14px;margin-top:10px"
            id="filter-drawer-apply">Show results</button>
  `;
  // Mirror options from desktop selects
  const regSrc = document.getElementById('filter-region-top');
  const regDst = document.getElementById('m-filter-region');
  if (regSrc && regDst) {
    regDst.innerHTML = regSrc.innerHTML;
    regDst.value = activeFilterRegion;
  }
  const asgSrc = document.getElementById('filter-assignee-top');
  const asgDst = document.getElementById('m-filter-assignee');
  if (asgSrc && asgDst) {
    asgDst.innerHTML = asgSrc.innerHTML;
    asgDst.value = activeFilterAssignee;
  }
  inner.querySelector('#filter-drawer-close').onclick = () => {
    document.getElementById('filter-drawer').classList.remove('open');
  };
  inner.querySelector('#filter-drawer-clear').onclick = () => {
    // Reset all filters and apply
    activeStatus = null;
    activeFilterRegion = '';
    activeFilterAssignee = '';
    favOnly = false;
    myMode = 0;
    if (regSrc) regSrc.value = '';
    if (asgSrc) asgSrc.value = '';
    document.getElementById('filter-fav-top').checked = false;
    document.getElementById('t-mine').classList.remove('active');
    document.getElementById('t-all').classList.add('active');
    const mtMine = document.getElementById('mt-mine');
    const mtAll = document.getElementById('mt-all');
    if (mtMine) mtMine.classList.remove('active');
    if (mtAll) mtAll.classList.add('active');
    document.getElementById('filter-drawer').classList.remove('open');
    refreshLeads();
  };
  let drawerMyMode = myMode;
  inner.querySelector('#m-t-mine').onclick = () => {
    drawerMyMode = 1;
    inner.querySelector('#m-t-mine').classList.add('active');
    inner.querySelector('#m-t-all').classList.remove('active');
  };
  inner.querySelector('#m-t-all').onclick = () => {
    drawerMyMode = 0;
    inner.querySelector('#m-t-all').classList.add('active');
    inner.querySelector('#m-t-mine').classList.remove('active');
  };
  inner.querySelector('#filter-drawer-apply').onclick = () => {
    myMode = drawerMyMode;
    activeStatus = inner.querySelector('#m-filter-status').value || null;
    activeFilterRegion = inner.querySelector('#m-filter-region').value;
    activeFilterAssignee = inner.querySelector('#m-filter-assignee').value;
    favOnly = inner.querySelector('#m-filter-fav').checked;
    // Sync desktop / outer UI
    if (regSrc) regSrc.value = activeFilterRegion;
    if (asgSrc) asgSrc.value = activeFilterAssignee;
    document.getElementById('filter-fav-top').checked = favOnly;
    document.getElementById('t-mine').classList.toggle('active', myMode === 1);
    document.getElementById('t-all').classList.toggle('active', myMode === 0);
    const mtMine = document.getElementById('mt-mine');
    const mtAll = document.getElementById('mt-all');
    if (mtMine) mtMine.classList.toggle('active', myMode === 1);
    if (mtAll) mtAll.classList.toggle('active', myMode === 0);
    document.getElementById('filter-drawer').classList.remove('open');
    refreshLeads();
  };
}

const mobFilterBtn = document.getElementById('mobile-filter-btn');
if (mobFilterBtn) {
  mobFilterBtn.onclick = () => {
    rebuildFilterDrawer();
    document.getElementById('filter-drawer').classList.add('open');
  };
}
// Close drawer on backdrop click
const fdrawer = document.getElementById('filter-drawer');
if (fdrawer) {
  fdrawer.addEventListener('click', (e) => {
    if (e.target === fdrawer) fdrawer.classList.remove('open');
  });
}

// ----------------- Side panel -----------------
async function openPanel(phone) {
  selectedPhone = phone;
  renderLeads();
  document.getElementById('panel-overlay').classList.add('open');
  document.getElementById('side-panel').classList.add('open');
  document.getElementById('sp-name').textContent = 'Loading...';
  document.getElementById('sp-meta').textContent = '';
  document.getElementById('sp-body').innerHTML = '';

  const r = await fetch('/api/lead/' + encodeURIComponent(phone));
  if (!r.ok) {
    document.getElementById('sp-body').innerHTML =
      '<div style="color:#fca5a5">Error loading lead</div>';
    return;
  }
  const data = await r.json();
  renderPanel(data.lead, data.activity || []);
}

function closePanel() {
  document.getElementById('panel-overlay').classList.remove('open');
  document.getElementById('side-panel').classList.remove('open');
  selectedPhone = null;
  renderLeads();
}
document.getElementById('sp-close').onclick = closePanel;
document.getElementById('panel-overlay').onclick = closePanel;
document.addEventListener('keydown', e => { if (e.key === 'Escape') closePanel(); });

// Pending state — assignment changes happen instantly (separate flow),
// but call outcome + note + status + follow-up are batched into Save.
let pendingDraft = null;

function renderPanel(l, activity) {
  const nameEl = document.getElementById('sp-name');
  const isFav = !!l.is_favorite;
  nameEl.innerHTML = `
    <button class="fav-star fav-toggle ${isFav?'active':''}"
            id="sp-fav" data-phone="${escapeHtml(l.phone)}" data-fav="${isFav?1:0}">
      ${isFav?'★':'☆'}
    </button>
    <span>${escapeHtml(l.name || '—')}</span>`;
  document.getElementById('sp-meta').textContent =
    [l.region, l.category].filter(Boolean).join(' • ');

  pendingDraft = {
    phone: l.phone,
    status: l.status || 'new',
    follow_up_date: l.follow_up_date || '',
    call_outcome: null,   // null | 'answered' | 'no_answer' | 'wrong_number'
    note: '',
    _baseline: {
      status: l.status || 'new',
      follow_up_date: l.follow_up_date || '',
    },
  };

  const phone = (l.phone || '').replace(/[^\d+]/g, '');
  const waPhone = phone.replace('+','').replace(/^00/,'');
  const email = l.email || '';
  const status = l.status || 'new';

  const userOpts = users.map(u =>
    `<option value="${u.id}" ${u.id===l.assigned_to?'selected':''}>${escapeHtml(u.full_name)}</option>`
  ).join('');

  const sug = l.domain_suggestion || '';
  const grA = l.domain_gr_available, comA = l.domain_com_available;
  let domainBlock = '';
  if (grA || comA) {
    domainBlock = `
      <h3>Domain</h3>
      <div class="info-row"><span class="label">.gr</span>
        <span class="value">${grA==='yes'?'<span style="color:#4ade80">✓ free</span>':'<span style="color:#6b7280">'+escapeHtml(grA||'—')+'</span>'}</span></div>
      <div class="info-row"><span class="label">.com</span>
        <span class="value">${comA==='yes'?'<span style="color:#4ade80">✓ free</span>':'<span style="color:#6b7280">'+escapeHtml(comA||'—')+'</span>'}</span></div>
      ${sug ? `<div class="info-row"><span class="label">Suggested</span>
        <span class="value"><b>${escapeHtml(sug)}</b>
          <button class="copy-btn" onclick="copyText('${escapeHtml(sug)}', this)">copy</button>
        </span></div>` : ''}
    `;
  }

  document.getElementById('sp-body').innerHTML = `
    <div class="panel-actions">
      <a class="${phone?'':'disabled'}" href="tel:${phone}">📞 Call</a>
      <a class="wa ${waPhone?'':'disabled'}" target="_blank" href="https://wa.me/${waPhone}">💬 WA</a>
      <a class="email ${email?'':'disabled'}" href="mailto:${email}">✉️ Email</a>
    </div>

    <h3>Log this contact</h3>
    <div class="action-row" id="sp-call-row">
      <button data-outcome="answered">✅ Answered</button>
      <button data-outcome="no_answer">⏱️ No answer</button>
      <button data-outcome="wrong_number">❌ Wrong #</button>
    </div>

    <textarea id="sp-note" placeholder="Σχόλια / τι ειπώθηκε / next step..."></textarea>

    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-top:10px">
      <div>
        <label style="font-size:11px;color:#8b92a6;text-transform:uppercase">Status</label>
        <select id="sp-status">
          ${Object.entries(STATUS_LABEL).map(([k,v]) =>
            `<option value="${k}" ${k===status?'selected':''}>${v}</option>`).join('')}
        </select>
      </div>
      <div>
        <label style="font-size:11px;color:#8b92a6;text-transform:uppercase">Follow-up date</label>
        <input id="sp-followup" type="date" value="${l.follow_up_date || ''}">
      </div>
    </div>

    <div class="save-bar">
      <div class="dirty-indicator" id="sp-dirty">● unsaved changes</div>
      <button class="btn" id="sp-save" style="width:100%; padding:12px">Save</button>
    </div>

    <h3>Assignment</h3>
    <div class="info-row"><span class="label">Assigned to</span>
      <span class="value">
        <select id="sp-assign" style="width:auto; min-width:160px">
          <option value="">— Unassigned —</option>${userOpts}
        </select>
      </span></div>

    ${(l.properties_list && l.properties_list.length > 1) ? `
    <h3>📦 Owner's Properties (${l.properties_list.length})</h3>
    <div class="props-list">
      ${l.properties_list.map(p => `
        <div class="prop">
          <div class="name">${escapeHtml(p.name||'')}</div>
          <div class="meta">${escapeHtml(p.region||'')} • ${escapeHtml(p.category||'—')}
            ${p.gmaps_url ? ` • <a href="${escapeHtml(p.gmaps_url)}" target="_blank" style="color:#60a5fa">Maps</a>` : ''}
          </div>
        </div>`).join('')}
    </div>
    <div style="font-size:11px;color:#fbbf24;margin-top:8px;line-height:1.4">
      💡 Tip: Pitch a single multi-property site instead of separate sites
      for each listing.
    </div>` : ''}

    <h3>Contact</h3>
    <div class="info-row"><span class="label">Phone</span>
      <span class="value">${escapeHtml(phone)}
        ${phone?`<button class="copy-btn" onclick="copyText('${phone}', this)">copy</button>`:''}</span></div>
    <div class="info-row"><span class="label">Email</span>
      <span class="value">${escapeHtml(email||'—')}
        ${email?`<button class="copy-btn" onclick="copyText('${email}', this)">copy</button>`:''}</span></div>
    ${l.gmaps_url?`<div class="info-row"><span class="label">Maps</span>
      <span class="value"><a href="${escapeHtml(l.gmaps_url)}" target="_blank" style="color:#60a5fa">Open in Google Maps →</a></span></div>`:''}

    ${domainBlock}

    <button class="btn" style="width:100%; margin-top:14px"
            onclick="goToProposal('${escapeHtml(l.phone)}')">
      📄 Generate Proposal for this Lead
    </button>

    <h3>Activity History</h3>
    <div class="timeline" id="sp-timeline">
      ${activity.length ? activity.map(a => renderActivityItem(a)).join('')
                         : '<div class="empty">No activity yet</div>'}
    </div>
  `;

  // Wire favorite toggle in panel header
  const favBtn = document.getElementById('sp-fav');
  if (favBtn) {
    favBtn.onclick = async () => {
      const ph = favBtn.dataset.phone;
      const cur = favBtn.dataset.fav === '1';
      const method = cur ? 'DELETE' : 'POST';
      await fetch('/api/lead/' + encodeURIComponent(ph) + '/favorite',
                    { method });
      favBtn.dataset.fav = cur ? '0' : '1';
      favBtn.textContent = cur ? '☆' : '★';
      favBtn.classList.toggle('active', !cur);
      const lead = allLeads.find(x => x.phone === ph);
      if (lead) lead.is_favorite = cur ? 0 : 1;
      // Refresh table star
      const tableStar = document.querySelector(
        `tr.lead-row[data-phone="${CSS.escape(ph)}"] .fav-star`);
      if (tableStar) {
        tableStar.dataset.fav = cur ? '0' : '1';
        tableStar.textContent = cur ? '☆' : '★';
        tableStar.classList.toggle('active', !cur);
      }
    };
  }
  wireActivityActions();

  // Quick action buttons — only mark in pendingDraft, no API call
  for (const btn of document.querySelectorAll('#sp-call-row button')) {
    btn.onclick = () => {
      const outcome = btn.dataset.outcome;
      // Toggle: clicking the same button again deselects
      if (pendingDraft.call_outcome === outcome) {
        pendingDraft.call_outcome = null;
        btn.classList.remove('active', 'no-answer', 'wrong-number');
      } else {
        pendingDraft.call_outcome = outcome;
        for (const b of document.querySelectorAll('#sp-call-row button')) {
          b.classList.remove('active', 'no-answer', 'wrong-number');
        }
        btn.classList.add('active');
        if (outcome === 'no_answer') btn.classList.add('no-answer');
        if (outcome === 'wrong_number') btn.classList.add('wrong-number');
      }
      markDirty();
    };
  }

  document.getElementById('sp-note').oninput = (e) => {
    pendingDraft.note = e.target.value;
    markDirty();
  };
  document.getElementById('sp-status').onchange = (e) => {
    pendingDraft.status = e.target.value;
    markDirty();
  };
  document.getElementById('sp-followup').onchange = (e) => {
    pendingDraft.follow_up_date = e.target.value;
    markDirty();
  };
  document.getElementById('sp-save').onclick = () => savePanel();

  // Assignment is independent — saves instantly
  document.getElementById('sp-assign').onchange = (e) =>
    assignTo(pendingDraft.phone, e.target.value);
}

function markDirty() {
  const original = pendingDraft._original || null;
  let dirty = pendingDraft.call_outcome != null ||
              pendingDraft.note.trim() !== '' ||
              false;
  // Compare to baseline: status/follow-up changed?
  if (pendingDraft._baseline) {
    if (pendingDraft.status !== pendingDraft._baseline.status) dirty = true;
    if (pendingDraft.follow_up_date !== pendingDraft._baseline.follow_up_date) dirty = true;
  }
  document.getElementById('sp-dirty').classList.toggle('show', dirty);
}

async function savePanel() {
  if (!pendingDraft || !pendingDraft.phone) return;
  const d = pendingDraft;
  const phone = d.phone;

  // Auto-promote status if user hasn't manually changed it but did
  // log a call / write a note. Only applies when the lead was 'new'.
  const userChangedStatus = d._baseline && d.status !== d._baseline.status;
  if (!userChangedStatus && d._baseline && d._baseline.status === 'new') {
    if (d.call_outcome === 'answered') d.status = 'reached';
    else if (d.call_outcome === 'no_answer') d.status = 'called';
    else if (d.call_outcome === 'wrong_number') d.status = 'disqualified';
    else if (d.note.trim()) d.status = 'called';
  }

  const tasks = [];

  // 1) Log call (if outcome chosen)
  if (d.call_outcome) {
    tasks.push(fetch('/api/lead/' + encodeURIComponent(phone) + '/log_call', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ outcome: d.call_outcome, note: d.note }),
    }));
  } else if (d.note.trim()) {
    tasks.push(fetch('/api/lead/' + encodeURIComponent(phone) + '/note', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ note: d.note }),
    }));
  }

  // 2) Update status / follow-up — fires if either user changed it,
  //    or auto-promotion changed it.
  const statusChanged = (!d._baseline) ||
                         d.status !== d._baseline.status ||
                         d.follow_up_date !== d._baseline.follow_up_date;
  if (statusChanged) {
    tasks.push(fetch('/api/lead/' + encodeURIComponent(phone) + '/status', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        status: d.status,
        follow_up_date: d.follow_up_date || null,
      }),
    }));
  }

  if (!tasks.length) {
    notify('Nothing to save');
    return;
  }

  await Promise.all(tasks);
  notify('Saved');
  refreshDailyCounter();
  if (selectedPhone === phone) openPanel(phone);
  refreshLeads();
}

async function assignTo(phone, user_id) {
  await fetch('/api/lead/' + encodeURIComponent(phone) + '/assign', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ user_id: user_id ? +user_id : null }),
  });
  notify('Assignment updated');
  refreshLeads();
}

function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const old = btn.textContent;
    btn.textContent = '✓';
    setTimeout(() => btn.textContent = old, 1200);
  });
}

function renderActivityItem(a) {
  const canEdit = ME.role === 'admin' || a.user_id === ME.id;
  const actions = canEdit ? `
    <span class="actions">
      <button data-edit="${a.id}">edit</button>
      <button data-del="${a.id}">delete</button>
    </span>` : '';
  return `
    <div class="item action-${escapeHtml(a.action)}" data-id="${a.id}">
      <div class="meta-line">
        ${escapeHtml(a.full_name||'?')} • ${escapeHtml(a.action)} •
        ${escapeHtml((a.created_at||'').replace('T',' ').slice(0,16))}
        ${actions}
      </div>
      <div class="details" data-details>${escapeHtml(a.details||'')}</div>
    </div>`;
}

function wireActivityActions() {
  const tl = document.getElementById('sp-timeline');
  if (!tl) return;
  for (const btn of tl.querySelectorAll('button[data-del]')) {
    btn.onclick = async () => {
      if (!confirm('Delete this activity entry?')) return;
      const id = btn.dataset.del;
      const r = await fetch('/api/activity/' + id, { method: 'DELETE' });
      if (r.ok) {
        btn.closest('.item').remove();
        notify('Deleted');
      } else {
        alert('Failed to delete');
      }
    };
  }
  for (const btn of tl.querySelectorAll('button[data-edit]')) {
    btn.onclick = () => {
      const item = btn.closest('.item');
      const detailsDiv = item.querySelector('[data-details]');
      const current = detailsDiv.textContent;
      item.classList.add('editing');
      detailsDiv.innerHTML = `
        <textarea class="edit-area">${escapeHtml(current)}</textarea>
        <div style="margin-top:6px">
          <button class="btn" data-save>Save</button>
          <button class="btn secondary" data-cancel>Cancel</button>
        </div>`;
      const ta = detailsDiv.querySelector('textarea');
      ta.focus();
      detailsDiv.querySelector('[data-cancel]').onclick = () => {
        detailsDiv.textContent = current;
        item.classList.remove('editing');
      };
      detailsDiv.querySelector('[data-save]').onclick = async () => {
        const newVal = ta.value.trim();
        const id = btn.dataset.edit;
        const r = await fetch('/api/activity/' + id, {
          method: 'PATCH', headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ details: newVal }),
        });
        if (r.ok) {
          detailsDiv.textContent = newVal;
          item.classList.remove('editing');
          notify('Updated');
        } else {
          alert('Failed to save');
        }
      };
    };
  }
}

function appendActivityToTimeline(a) {
  const tl = document.getElementById('sp-timeline');
  if (!tl) return;
  const wrap = document.createElement('div');
  wrap.innerHTML = renderActivityItem(a);
  tl.insertBefore(wrap.firstElementChild, tl.firstChild);
  wireActivityActions();
}
window.copyText = copyText;
window.goToProposal = function(phone) {
  closePanel();
  setView('proposal');
  // Reset and pre-select the lead
  setTimeout(() => {
    const sel = document.getElementById('prop-lead-select');
    // Make sure lead options are populated
    if (sel.options.length <= 1) initProposalForm();
    sel.value = phone;
    sel.dispatchEvent(new Event('change'));
  }, 100);
};

// ----------------- Users (admin) -----------------
async function loadUsers() {
  const r = await fetch('/api/users');
  users = await r.json();
  for (const u of users) {
    if (u.avatar) avatarCache.set(u.id, u.avatar);
  }
  // Seed the cache with my own avatar from ME
  if (ME.avatar) avatarCache.set(ME.id, ME.avatar);
  // Top assignee dropdown
  const topSel = document.getElementById('filter-assignee-top');
  if (topSel) {
    const cur = topSel.value;
    topSel.innerHTML = '<option value="">All assignees</option>' +
      '<option value="unassigned">— Unassigned —</option>' +
      users.map(u => `<option value="${u.id}">${escapeHtml(u.full_name)}</option>`).join('');
    topSel.value = cur;
  }
}

async function refreshUsers() {
  // Admin-only: include inactive users in the management list
  const url = ME.role === 'admin'
    ? '/api/users?include_inactive=1'
    : '/api/users';
  const r = await fetch(url);
  const allUsers = await r.json();
  // Update the global `users` list (active only) used elsewhere
  // (assignee dropdowns shouldn't show deactivated users)
  users = allUsers.filter(u => u.is_active);

  // Refresh dependent dropdowns from the active users
  const topSel = document.getElementById('filter-assignee-top');
  if (topSel) {
    const cur = topSel.value;
    topSel.innerHTML = '<option value="">👤 All assignees</option>' +
      '<option value="unassigned">— Unassigned —</option>' +
      users.map(u => `<option value="${u.id}">${escapeHtml(u.full_name)}</option>`).join('');
    topSel.value = cur;
  }

  // Fetch each user's assigned regions for the admin list (active only)
  const regionsByUser = {};
  await Promise.all(users.map(async u => {
    try {
      const r = await fetch('/api/users/' + u.id + '/regions');
      if (r.ok) {
        const d = await r.json();
        regionsByUser[u.id] = d.regions || [];
      }
    } catch {}
  }));

  const list = document.getElementById('admin-users');
  list.innerHTML = allUsers.map(u => {
    const inactive = !u.is_active;
    if (inactive) {
      return `
      <div class="user-row" style="flex-wrap:wrap; opacity:0.55">
        <div class="name" style="flex:1 1 200px">
          <b>${escapeHtml(u.full_name)}</b>
          <span style="color:#8b92a6"> · @${escapeHtml(u.username)}</span>
          <span style="margin-left:8px;font-size:10px;background:#4a1d1d;
                color:#fca5a5;padding:2px 8px;border-radius:10px;
                text-transform:uppercase">deactivated</span>
        </div>
        <span class="role ${u.role}">${escapeHtml(u.role)}</span>
        <button class="btn success" onclick="reactivateUser(${u.id})">Reactivate</button>
      </div>`;
    }
    const regs = regionsByUser[u.id] || [];
    const regSummary = regs.length === 0
      ? '<span style="color:#6b7280;font-style:italic">no regions</span>'
      : (regs.length <= 3
          ? regs.map(r => `<span class="assigned-pill">${escapeHtml(r)}</span>`).join(' ')
          : `<span class="assigned-pill">${regs.length} regions</span>`);
    return `
    <div class="user-row" style="flex-wrap:wrap">
      <div class="name" style="flex:1 1 200px">
        <b>${escapeHtml(u.full_name)}</b>
        <span style="color:#8b92a6"> · @${escapeHtml(u.username)}</span>
        <div style="margin-top:4px; font-size:11px">${regSummary}</div>
      </div>
      <span class="role ${u.role}">${escapeHtml(u.role)}</span>
      <button class="btn secondary" onclick="openRegionPicker(${u.id})">📍 Regions</button>
      ${u.id !== ME.id ? `
        <button class="btn secondary" onclick="changeRole(${u.id}, '${u.role === 'admin' ? 'sales' : 'admin'}')">
          ${u.role === 'admin' ? '↓ Demote to Sales' : '↑ Promote to Admin'}
        </button>
        <button class="btn secondary" onclick="resetPwd(${u.id})">Reset PW</button>
        <button class="btn danger" onclick="deactivateUser(${u.id})">Deactivate</button>
      ` : ''}
    </div>
  `;}).join('');
}

async function changeRole(uid, newRole) {
  const target = users.find(u => u.id === uid);
  const name = target ? target.full_name : 'this user';
  const verb = newRole === 'admin' ? 'promote' : 'demote';
  if (!confirm(`${verb === 'promote' ? '↑ Promote' : '↓ Demote'} ${name} to ${newRole}?\n\n` +
      (newRole === 'admin'
        ? 'They will gain full admin powers — manage users, assign regions, deactivate accounts.'
        : 'They will lose admin powers and become a regular sales user.'))) {
    return;
  }
  const r = await fetch('/api/users/' + uid + '/role', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ role: newRole }),
  });
  if (r.ok) {
    notify(`${name} is now ${newRole}`);
    refreshUsers();
  } else {
    let msg = 'Failed to change role';
    try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
    alert(msg);
  }
}
window.changeRole = changeRole;

// ----------------- Region picker (admin only) -----------------
let _regionPickerCache = null;
let _countriesCache = null;

async function loadAllRegions() {
  if (_regionPickerCache) return _regionPickerCache;
  const r = await fetch('/api/regions/all');
  _regionPickerCache = await r.json();
  // Update the global region->country map so the leads UI can use it too
  for (const row of _regionPickerCache) {
    if (row.region && row.country) REGION_COUNTRY[row.region] = row.country;
  }
  return _regionPickerCache;
}

async function loadCountries() {
  if (_countriesCache) return _countriesCache;
  try {
    const r = await fetch('/api/countries');
    if (!r.ok) return null;
    const data = await r.json();
    _countriesCache = data.countries || {};
    // Also populate REGION_COUNTRY from the catalogue (covers regions
    // that don't yet have a lead in the DB)
    for (const [cName, cData] of Object.entries(_countriesCache)) {
      for (const regions of Object.values(cData.groups || {})) {
        for (const r of regions) {
          if (!REGION_COUNTRY[r]) REGION_COUNTRY[r] = cName;
        }
      }
    }
    return _countriesCache;
  } catch { return null; }
}

async function openRegionPicker(uid) {
  const target = users.find(u => u.id === uid);
  if (!target) return;
  // Fetch current regions + full region list + country catalogue in parallel
  const [allRegions, countries, currentResp] = await Promise.all([
    loadAllRegions(),
    loadCountries(),
    fetch('/api/users/' + uid + '/regions'),
  ]);
  const currentData = currentResp.ok ? await currentResp.json() : { regions: [] };
  const current = new Set(currentData.regions || []);

  // Build a lead-count lookup from the regions-with-counts response
  const leadCount = {};
  for (const r of allRegions) leadCount[r.region] = r.lead_count;

  // Build the country -> group -> regions structure to render. Start from
  // the official catalogue (from /api/countries); if some region only
  // exists in the leads table (e.g. ad-hoc), fold it under "Other".
  const knownRegions = new Set();
  const structured = {};
  if (countries) {
    for (const [cName, cData] of Object.entries(countries)) {
      structured[cName] = { flag: cData.flag || '🌍', groups: {} };
      for (const [grpName, regions] of Object.entries(cData.groups || {})) {
        structured[cName].groups[grpName] = regions.slice();
        for (const r of regions) knownRegions.add(r);
      }
    }
  }
  const orphaned = allRegions
    .map(r => r.region).filter(r => r && !knownRegions.has(r));
  if (orphaned.length) {
    structured['Other'] = structured['Other'] ||
      { flag: '🌍', groups: { 'Uncategorized': [] } };
    for (const r of orphaned) {
      structured['Other'].groups['Uncategorized'].push(r);
    }
  }

  let modal = document.getElementById('region-picker-modal');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'region-picker-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);'+
    'z-index:200;display:flex;align-items:center;justify-content:center;padding:20px';
  modal.innerHTML = `
    <div style="background:#14171f;border:1px solid #2a2f3d;border-radius:12px;
                width:760px;max-width:100%;max-height:88vh;display:flex;
                flex-direction:column">
      <div style="padding:18px 22px;border-bottom:1px solid #2a2f3d;
                  display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:17px;font-weight:700">📍 Assign regions</div>
          <div style="font-size:13px;color:#8b92a6;margin-top:2px">
            ${escapeHtml(target.full_name)} · @${escapeHtml(target.username)}
          </div>
        </div>
        <button id="rp-close" style="background:transparent;border:0;
                color:#8b92a6;font-size:22px;cursor:pointer;padding:4px 8px">✕</button>
      </div>
      <div style="padding:14px 22px;border-bottom:1px solid #2a2f3d;
                  display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <input id="rp-search" type="text" placeholder="🔍 Filter regions..."
               style="flex:1;min-width:200px">
        <button class="btn secondary" id="rp-select-all">Select all</button>
        <button class="btn secondary" id="rp-clear">Clear</button>
        <span id="rp-count" style="color:#8b92a6;font-size:12px">
          ${current.size} selected
        </span>
      </div>
      <div id="rp-list" style="padding:14px 22px;overflow-y:auto;flex:1"></div>
      <div style="padding:14px 22px;border-top:1px solid #2a2f3d;
                  display:flex;justify-content:flex-end;gap:8px">
        <button class="btn secondary" id="rp-cancel">Cancel</button>
        <button class="btn" id="rp-save">Save</button>
      </div>
    </div>`;
  document.body.appendChild(modal);

  function updateCounter() {
    document.getElementById('rp-count').textContent =
      current.size + ' selected';
  }

  function renderList(filter) {
    const f = (filter || '').trim().toLowerCase();
    const list = document.getElementById('rp-list');
    const parts = [];
    for (const [cName, cData] of Object.entries(structured)) {
      const groupParts = [];
      let countryTotal = 0, countrySelected = 0;
      for (const [grpName, regions] of Object.entries(cData.groups)) {
        const visible = regions.filter(r =>
          !f || r.toLowerCase().includes(f));
        if (!visible.length) continue;
        const selectedInGroup = visible.filter(r => current.has(r)).length;
        countryTotal += visible.length;
        countrySelected += selectedInGroup;
        const itemsHtml = visible.map(r => {
          const checked = current.has(r) ? 'checked' : '';
          const cnt = leadCount[r] || 0;
          return `<label style="display:flex;align-items:center;gap:8px;
                                padding:6px 10px;background:#1a1d27;
                                border-radius:6px;cursor:pointer;font-size:13px;
                                user-select:none">
            <input type="checkbox" class="rp-region" data-region="${escapeHtml(r)}" ${checked}>
            <span style="flex:1">${escapeHtml(r)}</span>
            <span style="color:#6b7280;font-size:11px">${cnt}</span>
          </label>`;
        }).join('');
        groupParts.push(`
          <div style="margin:8px 0 12px">
            <label style="display:flex;align-items:center;gap:8px;
                          padding:4px 0 6px 4px;cursor:pointer;
                          border-bottom:1px solid #2a2f3d;margin-bottom:6px">
              <input type="checkbox" class="rp-group"
                     data-group="${escapeHtml(grpName)}"
                     ${selectedInGroup === visible.length ? 'checked' : ''}>
              <span style="flex:1;font-weight:600;font-size:12px;color:#cbd5e1">
                ${escapeHtml(grpName)}
              </span>
              <span style="color:#6b7280;font-size:11px">
                ${selectedInGroup}/${visible.length}
              </span>
            </label>
            <div style="display:grid;
                        grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
                        gap:4px 8px;padding-left:10px">
              ${itemsHtml}
            </div>
          </div>`);
      }
      if (!groupParts.length) continue;
      parts.push(`
        <div style="margin-bottom:18px" data-country="${escapeHtml(cName)}">
          <label style="display:flex;align-items:center;gap:10px;
                        padding:8px 10px;background:#11141c;border-radius:6px;
                        margin-bottom:8px;cursor:pointer">
            <input type="checkbox" class="rp-country"
                   data-country="${escapeHtml(cName)}"
                   ${countrySelected === countryTotal ? 'checked' : ''}>
            <span style="font-size:16px">${cData.flag}</span>
            <span style="flex:1;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.4px;color:#93c5fd">
              ${escapeHtml(cName)}
            </span>
            <span style="color:#6b7280;font-size:12px">
              ${countrySelected}/${countryTotal} selected
            </span>
          </label>
          ${groupParts.join('')}
        </div>`);
    }
    if (!parts.length) {
      list.innerHTML =
        '<div style="color:#6b7280;text-align:center;padding:40px">' +
        'No regions match this filter.</div>';
      return;
    }
    list.innerHTML = parts.join('');

    // Wire individual region checkboxes
    for (const cb of list.querySelectorAll('input.rp-region')) {
      cb.onchange = () => {
        if (cb.checked) current.add(cb.dataset.region);
        else current.delete(cb.dataset.region);
        updateCounter();
        // Re-render to refresh group/country tri-state checkboxes
        renderList(document.getElementById('rp-search').value);
      };
    }
    // Group checkboxes: toggle every region in that group (only the
    // currently visible ones, so search doesn't surprise the user)
    for (const cb of list.querySelectorAll('input.rp-group')) {
      cb.onchange = () => {
        const items = cb.closest('div').parentElement
          .querySelectorAll('input.rp-region');
        for (const it of items) {
          if (cb.checked) current.add(it.dataset.region);
          else current.delete(it.dataset.region);
        }
        updateCounter();
        renderList(document.getElementById('rp-search').value);
      };
    }
    // Country checkboxes: toggle every region in that country (visible)
    for (const cb of list.querySelectorAll('input.rp-country')) {
      cb.onchange = () => {
        const items = cb.closest('div[data-country]')
          .querySelectorAll('input.rp-region');
        for (const it of items) {
          if (cb.checked) current.add(it.dataset.region);
          else current.delete(it.dataset.region);
        }
        updateCounter();
        renderList(document.getElementById('rp-search').value);
      };
    }
  }
  renderList('');

  document.getElementById('rp-search').oninput = e => renderList(e.target.value);
  document.getElementById('rp-select-all').onclick = () => {
    for (const r of allRegions) current.add(r.region);
    updateCounter();
    renderList(document.getElementById('rp-search').value);
  };
  document.getElementById('rp-clear').onclick = () => {
    current.clear();
    updateCounter();
    renderList(document.getElementById('rp-search').value);
  };
  const close = () => modal.remove();
  document.getElementById('rp-close').onclick = close;
  document.getElementById('rp-cancel').onclick = close;
  modal.onclick = (e) => { if (e.target === modal) close(); };
  document.getElementById('rp-save').onclick = async () => {
    const r = await fetch('/api/users/' + uid + '/regions', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ regions: Array.from(current) }),
    });
    if (r.ok) {
      const d = await r.json();
      let msg = `Saved ${current.size} regions for ${target.full_name}`;
      if (d.bulk_assigned) msg += ` · ${d.bulk_assigned} leads assigned`;
      if (d.bulk_unassigned) msg += ` · ${d.bulk_unassigned} leads unassigned`;
      notify(msg);
      close();
      refreshUsers();
    } else {
      alert('Failed to save regions');
    }
  };
}
window.openRegionPicker = openRegionPicker;

async function resetPwd(uid) {
  const pw = prompt('New password:');
  if (!pw) return;
  const r = await fetch('/api/users/' + uid + '/password', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ password: pw }),
  });
  if (r.ok) notify('Password reset');
}
async function deactivateUser(uid) {
  const target = users.find(u => u.id === uid);
  const name = target ? target.full_name : 'this user';
  if (!confirm(
    `Deactivate ${name}?\n\n` +
    `• They won't be able to log in anymore\n` +
    `• Any active sessions get terminated immediately\n` +
    `• Their assigned leads will go back to unassigned\n` +
    `• Their region assignments will be removed\n\n` +
    `You can reactivate them later from this same screen.`)) {
    return;
  }
  const r = await fetch('/api/users/' + uid, { method: 'DELETE' });
  if (r.ok) {
    notify(`Deactivated ${name}`);
    refreshUsers();
    refreshLeads();  // unassigned leads may have shifted
  } else {
    let msg = 'Failed to deactivate';
    try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
    alert(msg);
  }
}

async function reactivateUser(uid) {
  const r = await fetch('/api/users/' + uid + '/activate', { method: 'POST' });
  if (r.ok) {
    notify('User reactivated');
    refreshUsers();
  } else {
    let msg = 'Failed to reactivate';
    try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
    alert(msg);
  }
}

window.resetPwd = resetPwd;
window.deactivateUser = deactivateUser;
window.reactivateUser = reactivateUser;

function openNewUserModal() {
  let modal = document.getElementById('new-user-modal');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'new-user-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);'+
    'z-index:200;display:flex;align-items:center;justify-content:center;padding:20px';
  modal.innerHTML = `
    <div style="background:#14171f;border:1px solid #2a2f3d;border-radius:12px;
                width:460px;max-width:100%">
      <div style="padding:18px 22px;border-bottom:1px solid #2a2f3d;
                  display:flex;justify-content:space-between;align-items:center">
        <div style="font-size:17px;font-weight:700">➕ Create user</div>
        <button id="nu-close" style="background:transparent;border:0;
                color:#8b92a6;font-size:22px;cursor:pointer;padding:4px 8px">✕</button>
      </div>
      <div style="padding:18px 22px">
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Username</label>
          <input id="nu-username" type="text" autocomplete="off"
                  placeholder="no spaces, e.g. giorgos">
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Full name</label>
          <input id="nu-fullname" type="text" placeholder="e.g. Γιώργος Σπύρου">
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Password</label>
          <input id="nu-password" type="password" placeholder="min 6 chars">
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:#8b92a6;
                  margin-bottom:6px;text-transform:uppercase">Role</label>
          <div class="toggle-row">
            <button type="button" id="nu-role-sales" class="active">Sales</button>
            <button type="button" id="nu-role-admin">Admin</button>
          </div>
          <div style="font-size:11px;color:#6b7280;margin-top:6px">
            Admins can manage users, assign regions, and deactivate accounts.
          </div>
        </div>
        <div id="nu-error" style="color:#fca5a5;font-size:13px;
                  margin:8px 0;display:none"></div>
      </div>
      <div style="padding:14px 22px;border-top:1px solid #2a2f3d;
                  display:flex;justify-content:flex-end;gap:8px">
        <button class="btn secondary" id="nu-cancel">Cancel</button>
        <button class="btn" id="nu-save">Create</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
  let role = 'sales';
  function showErr(msg) {
    const el = document.getElementById('nu-error');
    el.textContent = msg;
    el.style.display = msg ? 'block' : 'none';
  }
  const close = () => modal.remove();
  document.getElementById('nu-close').onclick = close;
  document.getElementById('nu-cancel').onclick = close;
  modal.onclick = (e) => { if (e.target === modal) close(); };
  document.getElementById('nu-role-sales').onclick = () => {
    role = 'sales';
    document.getElementById('nu-role-sales').classList.add('active');
    document.getElementById('nu-role-admin').classList.remove('active');
  };
  document.getElementById('nu-role-admin').onclick = () => {
    role = 'admin';
    document.getElementById('nu-role-admin').classList.add('active');
    document.getElementById('nu-role-sales').classList.remove('active');
  };
  setTimeout(() => document.getElementById('nu-username').focus(), 50);

  async function submit() {
    showErr('');
    const username = document.getElementById('nu-username').value.trim();
    const full_name = document.getElementById('nu-fullname').value.trim();
    const password = document.getElementById('nu-password').value;
    if (!username) { showErr('Username is required'); return; }
    if (/\s/.test(username)) { showErr('Username cannot contain spaces'); return; }
    if (!full_name) { showErr('Full name is required'); return; }
    if (password.length < 6) { showErr('Password must be at least 6 characters'); return; }
    const r = await fetch('/api/users', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ username, full_name, password, role }),
    });
    if (r.ok) {
      notify(`Created ${full_name} (${role})`);
      close();
      refreshUsers();
    } else {
      let msg = 'Failed to create user';
      try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
      showErr(msg);
    }
  }
  document.getElementById('nu-save').onclick = submit;
  for (const id of ['nu-username','nu-fullname','nu-password']) {
    document.getElementById(id).onkeydown = (e) => {
      if (e.key === 'Enter') submit();
    };
  }
}

document.getElementById('btn-new-user').onclick = openNewUserModal;

// ----------------- Daily plan -----------------
async function refreshPlan() {
  const r = await fetch('/api/daily_plan');
  const d = await r.json();
  document.getElementById('dp-calls').textContent = d.calls_today;
  document.getElementById('dp-followups').textContent = d.follow_ups.length;
  document.getElementById('dp-newleads').textContent = d.new_leads.length;
  document.getElementById('dp-followup-list').innerHTML = d.follow_ups.length ?
    d.follow_ups.map(l => leadCard(l)).join('') :
    '<div class="empty">No follow ups today</div>';
  document.getElementById('dp-new-list').innerHTML = d.new_leads.length ?
    d.new_leads.slice(0, 30).map(l => leadCard(l)).join('') :
    '<div class="empty">No new leads assigned</div>';
}

function leadCard(l) {
  return `<div class="user-row" style="cursor:pointer" onclick="openPanel('${escapeHtml(l.phone)}')">
    <div class="name"><b>${escapeHtml(l.name)}</b>
      <span style="color:#8b92a6"> · ${escapeHtml(l.region)}</span></div>
    <span class="status-badge s-${l.status||'new'}">${STATUS_LABEL[l.status||'new']}</span>
  </div>`;
}

async function refreshDailyCounter() {
  const r = await fetch('/api/daily_plan');
  const d = await r.json();
  const badge = document.getElementById('calls-today-badge');
  badge.textContent = `${d.calls_today}/${d.target} calls today`;
  badge.classList.toggle('met', d.calls_today >= d.target);
}

// ----------------- SSE -----------------
const feed = [];
const evt = new EventSource('/events');
evt.onmessage = (e) => {
  try {
    const data = JSON.parse(e.data);
    if (data.type === 'connected') return;
    if (data.type === 'chat_message') {
      onIncomingChatMessage(data);
      return;
    }
    if (data.type === 'leads_synced') {
      notify(`${data.count} new leads imported`);
      refreshLeads();
      return;
    }
    if (data.type === 'user_deactivated') {
      // If MY account just got deactivated, send me to /login
      if (data.user_id === ME.id) {
        alert('Your account has been deactivated by an admin.');
        window.location.href = '/logout';
        return;
      }
      if (currentView === 'admin') refreshUsers();
      // Drop them from the active users list used in dropdowns
      users = users.filter(u => u.id !== data.user_id);
      return;
    }
    if (data.type === 'user_activated') {
      if (currentView === 'admin') refreshUsers();
      return;
    }
    if (data.type === 'user_role_changed') {
      if (data.user_id === ME.id) {
        // My own role changed — reload to refresh navigation/UI
        notify(`Your role is now ${data.role} — reloading...`);
        setTimeout(() => window.location.reload(), 800);
        return;
      }
      if (currentView === 'admin') refreshUsers();
      return;
    }
    if (data.type === 'regions_assigned') {
      // If admin reassigned MY regions, refresh ME and the badge
      if (data.user_id === ME.id) {
        ME.regions = data.regions || [];
        renderMyRegionsUI();
        const ba = data.bulk_assigned || 0;
        const bu = data.bulk_unassigned || 0;
        let msg = `Your regions updated (${ME.regions.length})`;
        if (ba) msg += ` · +${ba} leads in My Leads`;
        if (bu) msg += ` · -${bu} leads removed`;
        notify(msg);
        refreshLeads();
      } else if (currentView === 'admin') {
        refreshUsers();
      }
      return;
    }
    if (data.type === 'activity') {
      feed.unshift(data);
      if (feed.length > 100) feed.pop();
      renderFeed();
      // Refresh leads view if relevant
      refreshLeads();
      // If panel is open on this lead, refresh ONLY if we have no unsaved
      // draft — otherwise we'd lose the user's typing
      if (selectedPhone && selectedPhone.replace(/[^\d+]/g,'') ===
          (data.lead_phone||'').replace(/[^\d+]/g,'')) {
        const isDirty = pendingDraft && (
          pendingDraft.call_outcome != null ||
          pendingDraft.note.trim() !== '' ||
          (pendingDraft._baseline && (
            pendingDraft.status !== pendingDraft._baseline.status ||
            pendingDraft.follow_up_date !== pendingDraft._baseline.follow_up_date
          ))
        );
        if (!isDirty) openPanel(selectedPhone);
        else appendActivityToTimeline(data);
      }
      // Refresh counter if it's our action
      if (data.user_id === ME.id) refreshDailyCounter();
    }
  } catch (err) { console.warn(err); }
};

let feedFilters = { search: '', region: '', user: '', action: '' };

async function loadRecentActivity() {
  const r = await fetch('/api/activity/recent');
  if (!r.ok) return;
  const rows = await r.json();
  feed.length = 0;
  for (const a of rows) {
    feed.push({
      type: 'activity',
      lead_phone: a.lead_phone,
      lead_name: a.lead_name,
      lead_region: a.lead_region,
      user_id: a.user_id,
      username: a.username,
      full_name: a.full_name,
      action: a.action,
      details: a.details,
      created_at: a.created_at,
    });
  }
  populateFeedDropdowns();
  renderFeed();
}

function populateFeedDropdowns() {
  // Regions present in feed
  const regions = [...new Set(feed.map(f => f.lead_region).filter(Boolean))].sort();
  const regSel = document.getElementById('feed-region');
  if (regSel) {
    const cur = regSel.value;
    regSel.innerHTML = '<option value="">All regions</option>' +
      regions.map(r => `<option value="${escapeHtml(r)}">${escapeHtml(r)}</option>`).join('');
    regSel.value = cur;
  }
  // Users — pull from global users list
  const userSel = document.getElementById('feed-user');
  if (userSel && users.length) {
    const cur = userSel.value;
    userSel.innerHTML = '<option value="">All users</option>' +
      users.map(u => `<option value="${u.id}">${escapeHtml(u.full_name)}</option>`).join('');
    userSel.value = cur;
  }
}

function applyFeedFilters() {
  let rows = feed;
  if (feedFilters.search) {
    const q = feedFilters.search.toLowerCase();
    rows = rows.filter(f =>
      (f.lead_name||'').toLowerCase().includes(q) ||
      (f.full_name||'').toLowerCase().includes(q) ||
      (f.details||'').toLowerCase().includes(q));
  }
  if (feedFilters.region) {
    rows = rows.filter(f => f.lead_region === feedFilters.region);
  }
  if (feedFilters.user) {
    rows = rows.filter(f => String(f.user_id) === feedFilters.user);
  }
  if (feedFilters.action) {
    rows = rows.filter(f => f.action === feedFilters.action);
  }
  return rows;
}

function renderFeed() {
  const el = document.getElementById('feed-list');
  const rows = applyFeedFilters();
  if (!rows.length) {
    el.innerHTML = '<div class="empty">No matching activity</div>';
    return;
  }
  el.innerHTML = rows.map(f => `
    <div class="feed-item">
      <div class="meta-line">${escapeHtml(f.full_name||'?')} • ${escapeHtml((f.created_at||'').replace('T',' ').slice(0,16))}</div>
      <div><b>${escapeHtml(f.action)}</b> on
        <a style="color:#60a5fa;cursor:pointer" onclick="openPanel('${escapeHtml(f.lead_phone)}')">${escapeHtml(f.lead_name||'(unknown lead)')}</a>
        <span style="color:#8b92a6"> (${escapeHtml(f.lead_region||'')})</span></div>
      ${f.details ? `<div style="margin-top:4px;color:#d6d3d1">${escapeHtml(f.details)}</div>` : ''}
    </div>
  `).join('');
}

// Wire feed filter inputs
let feedSearchTimer = null;
document.getElementById('feed-search').oninput = e => {
  clearTimeout(feedSearchTimer);
  feedFilters.search = e.target.value;
  feedSearchTimer = setTimeout(renderFeed, 200);
};
document.getElementById('feed-region').onchange = e => {
  feedFilters.region = e.target.value; renderFeed();
};
document.getElementById('feed-user').onchange = e => {
  feedFilters.user = e.target.value; renderFeed();
};
document.getElementById('feed-action').onchange = e => {
  feedFilters.action = e.target.value; renderFeed();
};

window.openPanel = openPanel;

// ----------------- Resources -----------------
async function loadResources() {
  const r = await fetch('/api/resources');
  const list = await r.json();
  const sidebar = document.getElementById('resources-list');
  sidebar.innerHTML = list.map(res => `
    <div class="res-card" data-slug="${res.slug}">
      <div class="title">${escapeHtml(res.title)}</div>
      <div class="subtitle">${escapeHtml(res.subtitle)}</div>
    </div>`).join('');
  for (const card of sidebar.querySelectorAll('.res-card')) {
    card.onclick = () => loadResource(card.dataset.slug);
  }
  // Auto-load first
  if (list.length) loadResource(list[0].slug);
}

async function loadResource(slug) {
  for (const c of document.querySelectorAll('.res-card')) {
    c.classList.toggle('active', c.dataset.slug === slug);
  }
  const r = await fetch('/api/resources/' + slug);
  if (!r.ok) return;
  const data = await r.json();
  document.getElementById('resource-content').innerHTML = data.html;
}

// ----------------- Proposal Generator -----------------
function initProposalForm() {
  // Populate lead dropdown
  const sel = document.getElementById('prop-lead-select');
  if (sel.options.length <= 1) {
    sel.innerHTML = '<option value="">— Manual entry —</option>' +
      allLeads.map(l => `<option value="${escapeHtml(l.phone)}">
        ${escapeHtml(l.name)} (${escapeHtml(l.region)})</option>`).join('');
    sel.onchange = () => {
      const ph = sel.value;
      if (!ph) return;
      const l = allLeads.find(x => x.phone === ph);
      if (!l) return;
      document.getElementById('prop-name').value = l.name || '';
      document.getElementById('prop-location').value = l.region || '';
      // Guess type from category
      const cat = (l.category || '').toLowerCase();
      const typeSel = document.getElementById('prop-type');
      if (cat.includes('villa') || cat.includes('house')) typeSel.value = 'villa';
      else if (cat.includes('hotel') || cat.includes('resort')) typeSel.value = 'hotel';
      else typeSel.value = 'apartments';
    };
  }
  // Default author
  if (!document.getElementById('prop-authors').value) {
    document.getElementById('prop-authors').value = ME.full_name || '';
  }
  // Auto date — DD/MM/YYYY
  const dateField = document.getElementById('prop-date');
  if (!dateField.value) {
    const now = new Date();
    const dd = String(now.getDate()).padStart(2, '0');
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const yyyy = now.getFullYear();
    dateField.value = `${dd}/${mm}/${yyyy}`;
  }
}

function getProposalPayload() {
  return {
    hotel_name: document.getElementById('prop-name').value.trim(),
    property_type: document.getElementById('prop-type').value,
    location: document.getElementById('prop-location').value.trim(),
    location_long: document.getElementById('prop-location').value.trim(),
    location_short: document.getElementById('prop-location').value.trim().split(',')[0],
    date: document.getElementById('prop-date').value.trim(),
    author_names: document.getElementById('prop-authors').value.trim(),
    author_phone: document.getElementById('prop-phone').value.trim(),
    author_email: document.getElementById('prop-email').value.trim(),
    option_a_price: document.getElementById('prop-price-a').value.trim(),
    option_b_price: document.getElementById('prop-price-b').value.trim(),
    lead_phone: document.getElementById('prop-lead-select').value,
  };
}

async function generateProposal() {
  const payload = getProposalPayload();
  if (!payload.hotel_name) { alert('Hotel name is required'); return null; }
  const r = await fetch('/api/proposal/generate', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    alert('Failed to generate proposal');
    return null;
  }
  const data = await r.json();
  return { html: data.html, payload };
}

document.getElementById('prop-preview').onclick = async () => {
  const result = await generateProposal();
  if (!result) return;
  // Render in iframe so the proposal styles don't bleed into our UI
  const area = document.getElementById('prop-preview-area');
  area.innerHTML = '';
  const iframe = document.createElement('iframe');
  iframe.style.width = '100%';
  iframe.style.minHeight = '720px';
  iframe.style.border = '0';
  iframe.style.borderRadius = '8px';
  area.appendChild(iframe);
  iframe.contentDocument.open();
  iframe.contentDocument.write(result.html);
  iframe.contentDocument.close();
};

document.getElementById('prop-download').onclick = async () => {
  const result = await generateProposal();
  if (!result) return;
  const blob = new Blob([result.html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const slug = (result.payload.hotel_name || 'proposal')
    .replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 40);
  a.href = url;
  a.download = `proposal_${slug}.html`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  notify('Downloaded');
};

// ----------------- Chat -----------------
let chats = [];
let activeChatId = null;
let onlineUsers = new Set();
let totalUnread = 0;
let pendingAttachments = [];

// Compress an image client-side: max 1280px on the long edge,
// JPEG quality 0.78. Returns a data URL.
async function compressImage(file, maxEdge = 1280, quality = 0.78) {
  const img = await new Promise((resolve, reject) => {
    const im = new Image();
    im.onload = () => resolve(im);
    im.onerror = reject;
    im.src = URL.createObjectURL(file);
  });
  const longEdge = Math.max(img.width, img.height);
  const scale = longEdge > maxEdge ? maxEdge / longEdge : 1;
  const w = Math.round(img.width * scale);
  const h = Math.round(img.height * scale);
  const canvas = document.createElement('canvas');
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, w, h);
  ctx.drawImage(img, 0, 0, w, h);
  URL.revokeObjectURL(img.src);
  return canvas.toDataURL('image/jpeg', quality);
}

function renderComposerAttachments() {
  const wrap = document.getElementById('composer-attachments');
  if (!wrap) return;
  if (pendingAttachments.length === 0) { wrap.innerHTML = ''; return; }
  wrap.innerHTML = pendingAttachments.map((a, i) => `
    <div class="composer-attachment">
      <img src="${a.data}" alt="">
      <button class="remove" data-idx="${i}" type="button">×</button>
    </div>
  `).join('');
  for (const b of wrap.querySelectorAll('.remove')) {
    b.onclick = () => {
      pendingAttachments.splice(+b.dataset.idx, 1);
      renderComposerAttachments();
      const send = document.getElementById('chat-send');
      const input = document.getElementById('chat-input');
      if (send && input) {
        send.disabled = !input.value.trim() && pendingAttachments.length === 0;
      }
    };
  }
}

async function openChatEditModal(chat) {
  let pendingAvatar = chat.avatar || null;
  let modal = document.getElementById('chat-edit-modal');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'chat-edit-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);'+
    'z-index:200;display:flex;align-items:center;justify-content:center;padding:20px';
  modal.innerHTML = `
    <div style="background:var(--surface);border:1px solid var(--border);
                border-radius:14px;width:420px;max-width:100%">
      <div style="padding:16px 20px;border-bottom:1px solid var(--border);
                  display:flex;justify-content:space-between;align-items:center">
        <div style="font-size:16px;font-weight:600">Edit chat</div>
        <button class="filter-drawer-close" id="ce-close">✕</button>
      </div>
      <div style="padding:20px">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px">
          <span class="avatar-wrap" id="ce-av-wrap">
            <span class="user-avatar lg"
                  style="background:linear-gradient(135deg,#2ecc71,#5cd0ff)">#</span>
            ${pendingAvatar ? `<img class="user-avatar-img lg" src="${pendingAvatar}">` : ''}
          </span>
          <input type="file" id="ce-file" accept="image/*" style="display:none">
          <div style="display:flex;flex-direction:column;gap:6px">
            <button class="btn ghost sm" id="ce-pick">Change photo</button>
            <button class="btn ghost sm" id="ce-clear">Remove photo</button>
          </div>
        </div>
        <div class="filter-group">
          <label style="display:block;font-size:11px;color:var(--text-3);
                  margin-bottom:6px;font-weight:600;text-transform:uppercase">
            Chat name
          </label>
          <input id="ce-name" type="text" value="${escapeHtml(chat.name || '')}"
                 maxlength="60">
        </div>
        <div id="ce-error" style="color:var(--danger);font-size:13px;
              margin-top:8px;display:none"></div>
      </div>
      <div style="padding:14px 20px;border-top:1px solid var(--border);
                  display:flex;justify-content:flex-end;gap:8px">
        <button class="btn secondary" id="ce-cancel">Cancel</button>
        <button class="btn" id="ce-save">Save</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
  function showErr(msg) {
    const e = document.getElementById('ce-error');
    e.textContent = msg; e.style.display = msg ? 'block' : 'none';
  }
  function refreshPreview() {
    const wrap = document.getElementById('ce-av-wrap');
    const old = wrap.querySelector('.user-avatar-img');
    if (old) old.remove();
    if (pendingAvatar) {
      const img = document.createElement('img');
      img.className = 'user-avatar-img lg';
      img.src = pendingAvatar;
      wrap.appendChild(img);
    }
  }
  const close = () => modal.remove();
  document.getElementById('ce-close').onclick = close;
  document.getElementById('ce-cancel').onclick = close;
  modal.onclick = (e) => { if (e.target === modal) close(); };
  document.getElementById('ce-pick').onclick = () =>
    document.getElementById('ce-file').click();
  document.getElementById('ce-clear').onclick = () => {
    pendingAvatar = null;
    refreshPreview();
  };
  document.getElementById('ce-file').onchange = async (e) => {
    const f = (e.target.files || [])[0];
    if (!f) return;
    try {
      pendingAvatar = await compressSquareAvatar(f);
      refreshPreview();
    } catch { showErr('Could not read image'); }
    e.target.value = '';
  };
  document.getElementById('ce-save').onclick = async () => {
    showErr('');
    const name = document.getElementById('ce-name').value.trim();
    const body = { name, avatar: pendingAvatar };
    const r = await fetch('/api/chats/' + chat.id, {
      method: 'PATCH', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(body),
    });
    if (r.ok) {
      notify('Chat updated');
      close();
      // Reload current chat to reflect changes
      if (activeChatId === chat.id) openChat(chat.id);
      refreshChatList();
    } else {
      let msg = 'Failed to save';
      try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
      showErr(msg);
    }
  };
}

function openImageLightbox(src) {
  const lb = document.createElement('div');
  lb.className = 'image-lightbox';
  lb.innerHTML = `<img src="${src}" alt="">`;
  lb.onclick = () => lb.remove();
  document.body.appendChild(lb);
}
window.openImageLightbox = openImageLightbox;

// Cache of avatar data URLs by user id, populated when /api/users
// is loaded. avatarHTML() pulls from this if there's a real image,
// falls back to initials otherwise.
const avatarCache = new Map();

function avatarHTML(userId, fullName, online, size) {
  const init = initials(fullName || '');
  const cls = (online ? 'avatar-wrap online' : 'avatar-wrap');
  const sizeCls = size === 'lg' ? ' lg' : '';
  const img = userId ? avatarCache.get(userId) : null;
  const imgHtml = img
    ? `<img class="user-avatar-img${sizeCls}" src="${img}" alt="">`
    : '';
  return `<span class="${cls}">
    <span class="user-avatar${sizeCls}" data-uid="${userId || ''}">${escapeHtml(init)}</span>
    ${imgHtml}
    <span class="online-dot"></span>
  </span>`;
}

function fmtChatTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  const today = new Date();
  const sameDay = d.toDateString() === today.toDateString();
  if (sameDay) {
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  const yest = new Date(today); yest.setDate(yest.getDate() - 1);
  if (d.toDateString() === yest.toDateString()) return 'Yesterday';
  return d.toLocaleDateString([], { day: '2-digit', month: 'short' });
}

function fmtMsgTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function onIncomingChatMessage(msg) {
  // Update local cache for the chat list
  const chat = chats.find(c => c.id === msg.chat_id);
  if (chat) {
    chat.last_message = {
      id: msg.id, body: msg.body, created_at: msg.created_at,
      user_id: msg.user_id, full_name: msg.full_name,
    };
    if (activeChatId === msg.chat_id && currentView === 'chat') {
      // Mark as read because the user is looking at it right now
      fetch('/api/chats/' + msg.chat_id + '/read', { method: 'POST' });
    } else if (msg.user_id !== ME.id) {
      chat.unread = (chat.unread || 0) + 1;
    }
  }
  // If we're viewing this chat, append the message
  if (activeChatId === msg.chat_id && currentView === 'chat') {
    appendMessage(msg);
  }
  recomputeUnreadBadge();
  if (currentView === 'chat') renderChatList();
  // Notify if from another user and chat view is not focused
  if (msg.user_id !== ME.id &&
      (currentView !== 'chat' || activeChatId !== msg.chat_id)) {
    const sender = (msg.full_name || '').split(' ')[0] || 'New message';
    notify(`${sender}: ${msg.body.length > 60 ? msg.body.slice(0,57)+'…' : msg.body}`);
  }
}

function recomputeUnreadBadge() {
  totalUnread = chats.reduce((sum, c) => sum + (c.unread || 0), 0);
  for (const id of ['nav-chat-badge', 'btab-chat-badge']) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (totalUnread > 0) {
      el.style.display = '';
      el.textContent = totalUnread > 99 ? '99+' : totalUnread;
    } else {
      el.style.display = 'none';
    }
  }
}

async function refreshChatList() {
  try {
    const r = await fetch('/api/chats');
    const d = await r.json();
    chats = d.chats || [];
    recomputeUnreadBadge();
    if (currentView === 'chat') renderChatList();
  } catch {}
}

function renderChatList() {
  const list = document.getElementById('chat-list');
  if (!list) return;
  if (!chats.length) {
    list.innerHTML = '<div class="empty">No conversations yet</div>';
    return;
  }
  list.innerHTML = chats.map(c => {
    let avatarUid = null;
    let avatarOnline = false;
    if (c.type === 'dm') {
      const peer = c.members.find(m => m.user_id !== ME.id);
      if (peer) {
        avatarUid = peer.user_id;
        avatarOnline = onlineUsers.has(peer.user_id);
      }
    }
    const isActive = c.id === activeChatId ? ' active' : '';
    const lastBody = c.last_message
      ? (c.last_message.user_id === ME.id ? 'You: ' : '') + c.last_message.body
      : 'No messages yet';
    const lastTime = c.last_message ? fmtChatTime(c.last_message.created_at) : '';
    const unreadHtml = c.unread
      ? `<span class="chat-unread">${c.unread > 99 ? '99+' : c.unread}</span>`
      : '';
    let avatarHtml;
    if (c.type === 'team' || c.type === 'group') {
      const imgPart = c.avatar
        ? `<img class="user-avatar-img" src="${c.avatar}">` : '';
      avatarHtml = `<span class="avatar-wrap"
        style="width:38px;height:38px;display:inline-block;position:relative">
        <span class="user-avatar" style="width:38px;height:38px;font-size:13px;
              background:linear-gradient(135deg,#2ecc71,#5cd0ff)">#</span>
        ${imgPart}
      </span>`;
    } else {
      avatarHtml = avatarHTML(avatarUid, c.name, avatarOnline);
    }
    return `<button class="chat-row${isActive}" data-chat-id="${c.id}">
      ${avatarHtml}
      <div class="chat-row-info">
        <div class="chat-row-name">${escapeHtml(c.name || 'Unknown')}</div>
        <div class="chat-row-last">${escapeHtml(lastBody)}</div>
      </div>
      <div class="chat-row-meta">
        <span class="chat-row-time">${lastTime}</span>
        ${unreadHtml}
      </div>
    </button>`;
  }).join('');
  for (const row of list.querySelectorAll('.chat-row')) {
    row.onclick = () => openChat(parseInt(row.dataset.chatId, 10));
  }
}

async function openChatView() {
  await refreshChatList();
  renderChatList();
  // Auto-select team chat if nothing selected, on desktop
  if (!activeChatId && chats.length && window.innerWidth > 768) {
    openChat(chats[0].id);
  } else if (activeChatId) {
    openChat(activeChatId);
  } else {
    document.getElementById('chat-thread').innerHTML =
      '<div class="chat-thread-empty">Select a conversation to start chatting</div>';
    document.getElementById('chat-thread').classList.remove('active-on-mobile');
    document.querySelector('.chat-sidebar').classList.remove('hidden-on-mobile');
  }
}

let chatLoadingId = null;
async function openChat(chatId) {
  activeChatId = chatId;
  chatLoadingId = chatId;
  // Mobile: show thread, hide sidebar
  document.querySelector('.chat-sidebar').classList.add('hidden-on-mobile');
  document.getElementById('chat-thread').classList.add('active-on-mobile');
  renderChatList();

  const thread = document.getElementById('chat-thread');
  thread.innerHTML = '<div class="chat-thread-empty">Loading...</div>';

  const r = await fetch('/api/chats/' + chatId + '/messages');
  if (!r.ok) {
    thread.innerHTML = '<div class="chat-thread-empty">Failed to load chat</div>';
    return;
  }
  if (chatLoadingId !== chatId) return; // user opened a different chat
  const data = await r.json();
  const chat = data.chat;
  let headerAvatar;
  let headerSub = '';
  if (chat.type === 'team' || chat.type === 'group') {
    if (chat.avatar) {
      headerAvatar = `<span class="avatar-wrap">
        <span class="user-avatar" style="width:36px;height:36px;font-size:13px;
              background:var(--surface-3)">#</span>
        <img class="user-avatar-img" src="${chat.avatar}"
             style="width:36px;height:36px"></span>`;
    } else {
      headerAvatar = `<span class="user-avatar"
        style="background:linear-gradient(135deg,#2ecc71,#5cd0ff);width:36px;height:36px;font-size:13px">#</span>`;
    }
    headerSub = `${chat.members.length} members`;
  } else {
    const peer = chat.members.find(m => m.user_id !== ME.id);
    const peerOnline = peer && onlineUsers.has(peer.user_id);
    headerAvatar = avatarHTML(peer && peer.user_id, chat.name, peerOnline);
    headerSub = peerOnline ? 'Online now' : 'Offline';
  }
  const adminEditBtn = (ME.role === 'admin' && chat.type !== 'dm')
    ? `<button class="chat-edit-btn" id="chat-edit-btn" title="Edit chat">
         <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
           <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
           <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
         </svg>
       </button>` : '';
  thread.innerHTML = `
    <div class="chat-thread-header">
      <button class="chat-back-btn" id="chat-back">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
             stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </button>
      ${headerAvatar}
      <div style="flex:1; min-width:0">
        <div class="name">${escapeHtml(chat.name)}</div>
        <div class="sub">${escapeHtml(headerSub)}</div>
      </div>
      ${adminEditBtn}
    </div>
    <div class="chat-messages" id="chat-messages"></div>
    <div class="chat-composer">
      <div class="composer-attachments" id="composer-attachments"></div>
      <div class="chat-composer-row">
        <button class="icon-btn" id="chat-attach" type="button"
                title="Attach photo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </button>
        <input id="chat-file-input" type="file" accept="image/*"
               multiple style="display:none">
        <textarea id="chat-input" placeholder="Type a message..." rows="1"></textarea>
        <button class="send-btn" id="chat-send" disabled
                title="Send (Enter)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>`;
  // Wire back button on mobile
  document.getElementById('chat-back').onclick = () => {
    activeChatId = null;
    document.querySelector('.chat-sidebar').classList.remove('hidden-on-mobile');
    document.getElementById('chat-thread').classList.remove('active-on-mobile');
    document.getElementById('chat-thread').innerHTML =
      '<div class="chat-thread-empty">Select a conversation to start chatting</div>';
    renderChatList();
  };
  // Admin edit-chat button
  const editBtn = document.getElementById('chat-edit-btn');
  if (editBtn) editBtn.onclick = () => openChatEditModal(chat);
  // Render messages
  const msgs = document.getElementById('chat-messages');
  msgs.innerHTML = '';
  let lastAuthor = null;
  let lastDay = null;
  for (const m of data.messages) {
    const day = new Date(m.created_at).toDateString();
    if (day !== lastDay) {
      const div = document.createElement('div');
      div.className = 'chat-day-divider';
      const today = new Date().toDateString();
      const y = new Date(); y.setDate(y.getDate() - 1);
      let label;
      if (day === today) label = 'Today';
      else if (day === y.toDateString()) label = 'Yesterday';
      else label = new Date(m.created_at).toLocaleDateString(
        [], { weekday: 'short', day: '2-digit', month: 'short' });
      div.textContent = label;
      msgs.appendChild(div);
      lastAuthor = null;
      lastDay = day;
    }
    msgs.appendChild(makeMsgEl(m, m.user_id === lastAuthor));
    lastAuthor = m.user_id;
  }
  msgs.scrollTop = msgs.scrollHeight;

  // Composer
  pendingAttachments = [];
  renderComposerAttachments();
  const input = document.getElementById('chat-input');
  const send = document.getElementById('chat-send');
  const updateSendEnabled = () => {
    send.disabled = !input.value.trim() && pendingAttachments.length === 0;
  };
  input.oninput = () => {
    updateSendEnabled();
    input.style.height = 'auto';
    input.style.height = Math.min(120, input.scrollHeight) + 'px';
  };
  input.onkeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChatMessage();
    }
  };
  send.onclick = sendChatMessage;

  // Image attachments
  const fileInput = document.getElementById('chat-file-input');
  document.getElementById('chat-attach').onclick = () => fileInput.click();
  fileInput.onchange = async (e) => {
    const files = Array.from(e.target.files || []);
    for (const f of files) {
      if (pendingAttachments.length >= 4) {
        notify('Max 4 photos per message');
        break;
      }
      if (!f.type.startsWith('image/')) continue;
      try {
        const dataUrl = await compressImage(f);
        pendingAttachments.push({ type: 'image', data: dataUrl });
      } catch (err) {
        console.warn('Image compression failed', err);
      }
    }
    fileInput.value = '';
    renderComposerAttachments();
    updateSendEnabled();
  };

  // Mark read
  await fetch('/api/chats/' + chatId + '/read', { method: 'POST' });
  const c = chats.find(x => x.id === chatId);
  if (c) c.unread = 0;
  recomputeUnreadBadge();
  renderChatList();
  setTimeout(() => { input.focus(); }, 50);
}

function makeMsgEl(m, sameAuthor) {
  const div = document.createElement('div');
  div.className = 'chat-msg' + (sameAuthor ? ' same-author' : '') +
    (m.user_id === ME.id ? ' mine' : '');
  const atts = m.attachments || [];
  const attHtml = atts.length ? `<div class="chat-msg-attachments">
    ${atts.map(a => a.type === 'image' ?
      `<button class="chat-msg-attachment" type="button"
              onclick="openImageLightbox('${a.data}')">
         <img src="${a.data}" alt="">
       </button>` : '').join('')}
  </div>` : '';
  const bodyHtml = m.body
    ? `<div class="chat-msg-text">${escapeHtml(m.body)}</div>` : '';
  div.innerHTML = `
    <div class="chat-msg-avatar">${avatarHTML(m.user_id, m.full_name,
      onlineUsers.has(m.user_id))}</div>
    <div class="chat-msg-body">
      <div class="chat-msg-meta">
        <span class="chat-msg-author">${escapeHtml(m.full_name || '')}</span>
        <span class="chat-msg-time">${fmtMsgTime(m.created_at)}</span>
      </div>
      ${bodyHtml}
      ${attHtml}
    </div>`;
  return div;
}

function appendMessage(m) {
  const msgs = document.getElementById('chat-messages');
  if (!msgs) return;
  // Detect same author / same day vs the last message
  const last = msgs.querySelector('.chat-msg:last-of-type');
  let sameAuthor = false;
  if (last) {
    const lastUid = last.querySelector('.user-avatar[data-uid]');
    if (lastUid && +lastUid.dataset.uid === m.user_id) sameAuthor = true;
  }
  msgs.appendChild(makeMsgEl(m, sameAuthor));
  msgs.scrollTop = msgs.scrollHeight;
}

async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const send = document.getElementById('chat-send');
  if (!input || !activeChatId) return;
  const body = input.value.trim();
  const atts = pendingAttachments.slice();
  if (!body && atts.length === 0) return;
  send.disabled = true;
  const r = await fetch('/api/chats/' + activeChatId + '/messages', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ body, attachments: atts }),
  });
  if (r.ok) {
    input.value = '';
    input.style.height = 'auto';
    pendingAttachments = [];
    renderComposerAttachments();
    // SSE will deliver the message back to us — no need to append here
  } else {
    let msg = 'Failed to send';
    try { const d = await r.json(); if (d.error) msg = d.error; } catch {}
    notify(msg);
    send.disabled = false;
  }
}

// New DM picker
async function openNewDmPicker() {
  // Get all active users besides me
  const r = await fetch('/api/users');
  const all = await r.json();
  const candidates = all.filter(u => u.id !== ME.id && u.is_active);
  let modal = document.getElementById('dm-picker');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'dm-picker';
  modal.className = 'dm-picker';
  modal.innerHTML = `
    <div class="dm-picker-inner">
      <div class="dm-picker-header">
        <h3>Start a conversation</h3>
        <button class="filter-drawer-close" id="dm-close">✕</button>
      </div>
      <div class="dm-picker-list">
        ${candidates.length === 0
          ? '<div class="empty">No other users yet</div>'
          : candidates.map(u => `
            <div class="dm-picker-row" data-uid="${u.id}">
              ${avatarHTML(u.id, u.full_name, onlineUsers.has(u.id))}
              <div>
                <div class="name">${escapeHtml(u.full_name)}</div>
                <div class="role">${escapeHtml(u.role)} · @${escapeHtml(u.username)}</div>
              </div>
            </div>
          `).join('')}
      </div>
    </div>
  `;
  document.body.appendChild(modal);
  const close = () => modal.remove();
  modal.onclick = (e) => { if (e.target === modal) close(); };
  document.getElementById('dm-close').onclick = close;
  for (const row of modal.querySelectorAll('.dm-picker-row')) {
    row.onclick = async () => {
      const uid = +row.dataset.uid;
      const r = await fetch('/api/chats/dm/' + uid, { method: 'POST' });
      if (r.ok) {
        const d = await r.json();
        close();
        await refreshChatList();
        openChat(d.chat_id);
      }
    };
  }
}

// Wire the "+ New" button (needs to wait for the chat view to be present)
document.addEventListener('click', (e) => {
  if (e.target.closest('#btn-new-dm')) {
    openNewDmPicker();
  }
});

// ----------------- Push notifications -----------------
// Two delivery paths:
//   1. Web push (browser / TWA fallback): VAPID + service worker.
//   2. Native (Capacitor APK): @capacitor/local-notifications fired
//      from the SSE chat_message handler. No FCM round-trip, no Chrome
//      icon, no "Running in Chrome" banner — feels like a native app.
const isNativeApp = !!(window.Capacitor && window.Capacitor.isNativePlatform &&
                        window.Capacitor.isNativePlatform());
let nativeNotificationsReady = false;
let pushSupported = !isNativeApp && ('serviceWorker' in navigator) &&
                    ('PushManager' in window) && ('Notification' in window);
let swRegistration = null;
let pushSubscription = null;

async function setupNativeNotifications() {
  if (!isNativeApp) return false;
  try {
    const LN = window.Capacitor.Plugins.LocalNotifications;
    if (!LN) return false;
    const perm = await LN.checkPermissions();
    if (perm.display !== 'granted') {
      const req = await LN.requestPermissions();
      if (req.display !== 'granted') return false;
    }
    nativeNotificationsReady = true;
    return true;
  } catch (e) {
    console.warn('Native notifications setup failed:', e);
    return false;
  }
}

async function fireNativeNotification(title, body, data) {
  if (!isNativeApp || !nativeNotificationsReady) return;
  try {
    const LN = window.Capacitor.Plugins.LocalNotifications;
    if (!LN) return;
    await LN.schedule({
      notifications: [{
        id: Math.floor(Math.random() * 2147483647),
        title: title,
        body: body,
        smallIcon: 'ic_launcher',
        iconColor: '#4F7CFF',
        ongoing: false,
        autoCancel: true,
        extra: data || {},
      }],
    });
  } catch (e) {
    console.warn('schedule failed:', e);
  }
}

function urlBase64ToUint8Array(b64) {
  const padding = '='.repeat((4 - b64.length % 4) % 4);
  const base64 = (b64 + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(base64);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; ++i) out[i] = raw.charCodeAt(i);
  return out;
}

async function initPush() {
  if (!pushSupported) return;
  try {
    swRegistration = await navigator.serviceWorker.register('/sw.js');
    pushSubscription = await swRegistration.pushManager.getSubscription();
    updatePushUI();
  } catch (e) {
    console.warn('SW register failed', e);
  }
}

async function enablePush() {
  if (!pushSupported) {
    alert('Your browser does not support push notifications.');
    return;
  }
  if (!swRegistration) {
    swRegistration = await navigator.serviceWorker.register('/sw.js');
  }
  // Wipe any stale server-side subscription before subscribing fresh.
  // Without this, a subscription signed against an old VAPID key may
  // persist and silently fail every send.
  try { await fetch('/api/push/reset', { method: 'POST' }); } catch {}
  // Also unsubscribe any existing browser-side subscription
  try {
    const existing = await swRegistration.pushManager.getSubscription();
    if (existing) await existing.unsubscribe();
  } catch {}
  const perm = await Notification.requestPermission();
  if (perm !== 'granted') {
    notify('Notifications are blocked. Allow them in your browser settings.');
    return;
  }
  // Get VAPID public key (always fetched fresh so we use the
  // current server-side keys, not anything cached client-side)
  const r = await fetch('/api/push/public-key');
  const { key } = await r.json();
  const sub = await swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(key),
  });
  // POST it to the server
  const subJson = sub.toJSON();
  await fetch('/api/push/subscribe', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(subJson),
  });
  pushSubscription = sub;
  notify('Notifications enabled');
  // Send a test ping so the user sees one immediately
  try { await fetch('/api/push/test', { method: 'POST' }); } catch {}
  updatePushUI();
}

async function autoRecoverPush() {
  // Forces a clean re-subscribe: clears server side, unsubscribes the
  // browser, then runs enablePush() again.
  try { await fetch('/api/push/reset', { method: 'POST' }); } catch {}
  if (pushSubscription) {
    try { await pushSubscription.unsubscribe(); } catch {}
    pushSubscription = null;
  }
  if (swRegistration) {
    const existing = await swRegistration.pushManager.getSubscription();
    if (existing) try { await existing.unsubscribe(); } catch {}
  }
  await enablePush();
}

async function disablePush() {
  if (!pushSubscription) { updatePushUI(); return; }
  try {
    await fetch('/api/push/unsubscribe', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ endpoint: pushSubscription.endpoint }),
    });
    await pushSubscription.unsubscribe();
  } catch {}
  pushSubscription = null;
  notify('Notifications disabled');
  updatePushUI();
}

// Detect runtime environment so we can give the right instructions
function detectPlatform() {
  const ua = navigator.userAgent;
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches
                        || window.navigator.standalone === true;
  const isAndroid = /Android/i.test(ua);
  const isIOS = /iPhone|iPad|iPod/i.test(ua);
  // TWA leaves the android-app:// referrer on first load only — after
  // a soft reload it goes empty. We cache the original referrer in
  // sessionStorage so detection survives navigation.
  let originalRef = '';
  try { originalRef = sessionStorage.getItem('_orig_ref') || ''; } catch {}
  if (!originalRef) {
    originalRef = document.referrer || '';
    try { sessionStorage.setItem('_orig_ref', originalRef); } catch {}
  }
  const isTWA = isStandalone && isAndroid &&
                originalRef.startsWith('android-app://');
  const isPWA = isStandalone && !isTWA;
  return {
    isAndroid, isIOS, isStandalone, isTWA, isPWA,
    referrer: originalRef,
    displayMode: isStandalone ? 'standalone' : 'browser',
  };
}

function pushHelpText(state) {
  const p = detectPlatform();
  if (state === 'denied') {
    if (p.isAndroid && p.isTWA) {
      return 'Open Android Settings → Apps → Devox Sales → Notifications → turn on. Then come back and tap "Push notifications" again.';
    }
    if (p.isAndroid) {
      return 'In Chrome: tap the lock icon next to the URL → Permissions → Notifications → Allow. Or Settings → Site settings → Notifications.';
    }
    if (p.isIOS) {
      return 'Settings → Notifications → Devox Sales → turn Allow Notifications on.';
    }
    return 'Click the lock icon in your browser address bar → Site permissions → Notifications → Allow.';
  }
  if (state === 'unsupported-ios-tab') {
    return 'On iPhone, open this site in Safari, then tap Share → Add to Home Screen. Notifications only work after that.';
  }
  if (state === 'unsupported') {
    return 'This browser does not support push notifications. Use Chrome on Android or Safari on iOS 16.4+ (Add to Home Screen first).';
  }
  return '';
}

function updatePushUI() {
  const pill = document.getElementById('acc-push-pill');
  const sub = document.getElementById('acc-push-sub');
  const btn = document.getElementById('acc-toggle-push');
  const test = document.getElementById('acc-test-push');
  const help = document.getElementById('acc-push-help');
  const helpText = document.getElementById('acc-push-help-text');
  if (!pill || !btn) return;

  const p = detectPlatform();
  // iOS Safari supports push only when installed to Home Screen
  if (p.isIOS && !p.isStandalone) {
    pill.textContent = 'iOS — install first';
    pill.className = 'account-pill';
    btn.disabled = true;
    if (sub) sub.textContent = 'Tap Share → Add to Home Screen, then enable from there.';
    if (help) help.style.display = '';
    if (helpText) helpText.textContent = pushHelpText('unsupported-ios-tab');
    if (test) test.style.display = 'none';
    return;
  }

  if (!pushSupported) {
    pill.textContent = 'Unsupported';
    pill.className = 'account-pill';
    btn.disabled = true;
    if (sub) sub.textContent = 'This browser cannot deliver push notifications.';
    if (help) help.style.display = '';
    if (helpText) helpText.textContent = pushHelpText('unsupported');
    if (test) test.style.display = 'none';
    return;
  }

  const perm = ('Notification' in window) ? Notification.permission : 'default';

  const reset = document.getElementById('acc-reset-push');
  if (pushSubscription && perm === 'granted') {
    pill.textContent = 'On';
    pill.className = 'account-pill on';
    if (sub) sub.textContent = "You'll get pings for new messages and assignments.";
    if (help) help.style.display = 'none';
    if (test) test.style.display = '';
    if (reset) {
      reset.style.display = '';
      reset.onclick = async () => {
        if (!confirm('Reset this device’s notification subscription? You may need to re-allow notifications.')) return;
        notify('Resetting...');
        await autoRecoverPush();
      };
    }
    const diag = document.getElementById('acc-diagnose-push');
    if (diag) {
      diag.style.display = '';
      diag.onclick = async () => {
        const r = await fetch('/api/push/diagnose');
        if (!r.ok) { notify('Could not load diagnostics'); return; }
        const d = await r.json();
        const p = detectPlatform();
        const lines = [
          '=== Server ===',
          `pywebpush: ${d.pywebpush_version}`,
          `py_vapid: ${d.py_vapid_version}`,
          `Public key prefix: ${d.vapid_public_key_prefix || '(not set)'}`,
          `Subscriptions: ${(d.subscriptions || []).length}`,
          '',
          '=== Device ===',
          `Display mode: ${p.displayMode}`,
          `isStandalone: ${p.isStandalone}`,
          `isAndroid: ${p.isAndroid}`,
          `isIOS: ${p.isIOS}`,
          `isTWA: ${p.isTWA}`,
          `Referrer: ${p.referrer || '(empty)'}`,
          `Notification.permission: ${('Notification' in window) ? Notification.permission : 'n/a'}`,
        ];
        for (const s of (d.subscriptions || [])) {
          lines.push('');
          lines.push('=== Subscription ===');
          lines.push(`Via: ${s.endpoint_host}`);
          if (s.last_error) {
            lines.push(`Last error (${s.last_error_at}):`);
            lines.push(s.last_error);
          } else {
            lines.push('No errors recorded');
          }
        }
        alert(lines.join('\n'));
      };
    }
    const rotate = document.getElementById('acc-rotate-keys');
    if (rotate) {
      rotate.style.display = ME.role === 'admin' ? '' : 'none';
      rotate.onclick = async () => {
        if (!confirm('Rotate the server VAPID keys?\n\nThis wipes EVERY user\'s push subscription. Each user will have to toggle Notifications Off → On again. Use this only if normal delivery keeps failing.')) return;
        const r = await fetch('/api/admin/push/rotate-keys', { method: 'POST' });
        if (!r.ok) { notify('Rotation failed'); return; }
        notify('Keys rotated. Resubscribing this device...');
        await new Promise(res => setTimeout(res, 600));
        await autoRecoverPush();
      };
    }
  } else if (perm === 'denied') {
    pill.textContent = 'Blocked';
    pill.className = 'account-pill';
    if (sub) sub.textContent = 'Notifications are blocked by your browser/OS.';
    if (help) help.style.display = '';
    if (helpText) helpText.textContent = pushHelpText('denied');
    if (test) test.style.display = 'none';
    if (reset) reset.style.display = 'none';
    const diag2 = document.getElementById('acc-diagnose-push');
    if (diag2) diag2.style.display = 'none';
  } else {
    pill.textContent = 'Off';
    pill.className = 'account-pill';
    if (sub) sub.textContent = 'Tap to enable. Your browser will ask for permission.';
    if (help) help.style.display = 'none';
    if (test) test.style.display = 'none';
    if (reset) reset.style.display = 'none';
    const diag2 = document.getElementById('acc-diagnose-push');
    if (diag2) diag2.style.display = 'none';
  }

  btn.onclick = () => {
    if (perm === 'denied') {
      // Show clear instructions instead of trying to re-prompt (which
      // most browsers/OSes won't honor once denied)
      alert(pushHelpText('denied'));
      return;
    }
    if (pushSubscription) disablePush();
    else enablePush();
  };
  if (test) {
    test.onclick = async () => {
      const r = await fetch('/api/push/test', { method: 'POST' });
      if (!r.ok) { notify('Test failed — server error'); return; }
      const d = await r.json();
      if (d.subscriptions_before === 0 && d.subscriptions === 0) {
        notify('No device subscribed. Toggle "Push notifications" off and on again.');
        return;
      }
      if (d.sent > 0) {
        notify(`Test sent to ${d.sent}/${d.subscriptions_before} device${d.sent>1?'s':''}`);
        return;
      }
      // Subs existed but the server already pruned them as dead
      // (HTTP 401/403/404/410). Auto-recover by re-subscribing.
      if (d.pruned > 0) {
        notify('Stale subscription — refreshing now...');
        await autoRecoverPush();
        return;
      }
      // Subscription still on file but delivery failed for some
      // other reason. Auto-recover instead of showing a wall of text.
      notify('Delivery failed — refreshing subscription...');
      await autoRecoverPush();
    };
  }
}

// Bootstrap push as soon as the page loads (registers SW so we're ready
// the first time the user opens Account → Push notifications).
initPush();

// Service worker → page channel: when the user clicks a notification
// the SW posts a navigate message, route to the relevant view.
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('message', (e) => {
    if (e.data && e.data.type === 'navigate') {
      // Currently we only route to /, so no-op. Hook for future.
    }
  });
}

// ----------------- Presence -----------------
async function pingPresence() {
  if (document.hidden) return;  // don't waste cycles on backgrounded tabs
  try {
    await fetch('/api/presence/ping', { method: 'POST' });
  } catch {}
}

async function refreshPresence() {
  if (document.hidden) return;
  try {
    const r = await fetch('/api/presence');
    if (!r.ok) return;
    const d = await r.json();
    const newSet = new Set(d.online || []);
    onlineUsers = newSet;
    // Update online dots throughout the page
    for (const w of document.querySelectorAll('.avatar-wrap')) {
      const av = w.querySelector('.user-avatar[data-uid]');
      if (!av) continue;
      const uid = +av.dataset.uid;
      w.classList.toggle('online', onlineUsers.has(uid));
    }
    // Update "online now" counter in top bar
    const cnt = document.getElementById('online-now');
    if (cnt) {
      const others = Array.from(onlineUsers).filter(id => id !== ME.id).length;
      cnt.textContent = others > 0 ? `${others} online` : '';
    }
  } catch {}
}

// Catch up immediately when the tab becomes visible again
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    pingPresence();
    refreshPresence();
  }
});

pingPresence();
refreshPresence();
// Slower polling: presence is non-critical, prefer responsiveness on
// the user's actual interactions.
setInterval(pingPresence, 60000);
setInterval(refreshPresence, 60000);

// Don't pre-fetch the chat list on init — it costs 4 DB queries that
// the user usually doesn't need until they tap the Chat tab. The
// unread badge will catch up either via the SSE chat_message channel
// or when the user opens Chat for the first time.
// (The first-paint price for Leads dropped by ~300ms with this off.)

// Wire the system back button to navigate between SPA views instead
// of jumping back to /login. We seed a base history entry for "leads"
// so the first back-press from any other view drops the user on Leads
// instead of leaving the app or hitting the login page.
try {
  if (!history.state || !history.state.view) {
    history.replaceState({ view: 'leads' }, '', '#leads');
  }
} catch (e) {}

window.addEventListener('popstate', (e) => {
  // Close any open overlays first — that's what the user expects from
  // back: dismiss the modal, not navigate away.
  const closables = [
    document.querySelector('.dm-picker'),
    document.getElementById('region-picker-modal'),
    document.getElementById('pw-modal'),
    document.getElementById('new-user-modal'),
  ];
  for (const c of closables) { if (c) { c.remove(); /* eat back */
    history.pushState({ view: currentView }, '', '#' + currentView);
    return; } }
  const drawer = document.getElementById('filter-drawer');
  if (drawer && drawer.classList.contains('open')) {
    drawer.classList.remove('open');
    rebuildFilterDrawer();
    history.pushState({ view: currentView }, '', '#' + currentView);
    return;
  }
  // Close the lead detail panel if it's open
  const panel = document.getElementById('side-panel');
  if (panel && panel.classList.contains('open')) {
    closePanel();
    history.pushState({ view: currentView }, '', '#' + currentView);
    return;
  }
  // Otherwise, pop into the matching view
  const target = (e.state && e.state.view) || 'leads';
  if (target !== currentView) {
    setView(target, { pushHistory: false });
  }
});

// If the URL has a #view hash on first load (e.g. from a deep link),
// honour it instead of the default Leads view.
const _initialHash = (location.hash || '').replace(/^#/, '');
const _validViews = new Set(['leads', 'plan', 'feed', 'admin',
  'resources', 'proposal', 'account', 'chat']);
if (_initialHash && _validViews.has(_initialHash)) {
  setView(_initialHash, { pushHistory: false });
}

// Init — every user lands in All Leads by default. The My Leads tab
// shows only the leads that admin has assigned to them via regions
// or one-by-one. Switching is one click from the sidebar.
loadUsers();
// Pre-load the country catalogue so REGION_COUNTRY is populated before
// the user clicks a country chip (lets the region dropdown narrow correctly
// without an extra round-trip).
loadCountries().catch(() => {});
refreshLeads();
refreshDailyCounter();
setInterval(refreshDailyCounter, 30000);
</script>
</body>
</html>"""
