"""HTML/CSS/JS for the CRM workspace UI."""

INDEX_HTML = r"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<title>Devox CRM</title>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, Segoe UI, sans-serif; margin: 0;
       background: #0f1117; color: #e8eaf0; }
.top { padding: 14px 22px; background: #1a1d27;
       border-bottom: 1px solid #2a2f3d; display: flex;
       align-items: center; gap: 22px; }
.top h1 { margin: 0; font-size: 17px; font-weight: 700; display: flex;
          align-items: center; gap: 10px; }
.top h1 img { height: 28px; width: auto;
              filter: brightness(0) invert(1); }
.top .center-title { position: absolute; left: 50%;
                      transform: translateX(-50%); font-size: 16px;
                      font-weight: 700; letter-spacing: 1px;
                      text-transform: uppercase; color: #e8eaf0; }
.top { position: relative; }
.top .nav { display: flex; gap: 18px; margin-left: 12px; }
.top .nav a { color: #8b92a6; text-decoration: none; font-size: 14px;
              padding: 6px 0; border-bottom: 2px solid transparent;
              cursor: pointer; }
.top .nav a.active, .top .nav a:hover { color: #e8eaf0;
                                          border-bottom-color: #2563eb; }
.top .spacer { flex: 1; }
.top .user-info { font-size: 13px; color: #8b92a6; display: flex;
                  align-items: center; gap: 10px; }
.user-info .badge { padding: 4px 10px; background: #2a2f3d; border-radius: 12px;
                    font-size: 12px; }
.user-info .live { color: #4ade80; }
.user-info a { color: #8b92a6; text-decoration: none; padding: 4px 8px; }
.user-info a:hover { color: #fca5a5; }
.target-badge { background: #1e3a8a; color: #93c5fd; padding: 4px 10px;
                border-radius: 12px; font-size: 12px; font-weight: 600; }
.target-badge.met { background: #14532d; color: #4ade80; }

.container { display: grid; grid-template-columns: 280px 1fr;
             height: calc(100vh - 56px); }
.sidebar { padding: 18px; border-right: 1px solid #2a2f3d;
           overflow-y: auto; background: #14171f; }
.main { padding: 18px 22px; overflow-y: auto; }
.sidebar h2, .main h2 { font-size: 11px; text-transform: uppercase;
                         color: #8b92a6; margin: 16px 0 8px;
                         letter-spacing: 0.5px; }
.sidebar h2:first-child, .main h2:first-child { margin-top: 0; }

.btn { background: #2563eb; color: white; border: 0; padding: 8px 14px;
       border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 13px; }
.btn:hover { background: #1d4ed8; }
.btn.secondary { background: #2a2f3d; color: #e8eaf0; }
.btn.secondary:hover { background: #3a3f4d; }
.btn.danger { background: #dc2626; }
.btn.success { background: #16a34a; }

select, input[type=text], input[type=number], input[type=date],
input[type=password], textarea {
  background: #0a0c12; color: #e8eaf0; border: 1px solid #2a2f3d;
  padding: 8px 10px; border-radius: 6px; font-size: 13px;
  width: 100%; font-family: inherit;
}
textarea { resize: vertical; min-height: 60px; }

.filter-group { margin-bottom: 12px; }
.filter-group label { display: block; font-size: 11px; color: #8b92a6;
                       margin-bottom: 4px; text-transform: uppercase;
                       letter-spacing: 0.5px; }

.toggle-row { display: flex; gap: 4px; background: #0a0c12; padding: 4px;
              border-radius: 6px; }
.toggle-row button { flex: 1; padding: 6px; background: transparent;
                      color: #8b92a6; border: 0; cursor: pointer;
                      border-radius: 4px; font-size: 12px; font-weight: 600; }
.toggle-row button.active { background: #2563eb; color: white; }

.status-counts { display: flex; flex-direction: column; gap: 4px; }
.status-counts .row { display: flex; justify-content: space-between;
                       align-items: center; padding: 6px 10px;
                       cursor: pointer; border-radius: 6px;
                       font-size: 12px; background: #0a0c12;
                       border-left: 3px solid transparent; }
.status-counts .row:hover { background: #1a1d27; }
.status-counts .row.active { background: #1e40af; color: white;
                              border-left-color: #60a5fa; }
.status-counts .row .label { font-weight: 600; }
.status-counts .row .count { background: #2a2f3d; color: #d6d3d1;
                              padding: 1px 8px; border-radius: 10px;
                              font-size: 11px; min-width: 24px;
                              text-align: center; }
.status-counts .row.active .count { background: rgba(255,255,255,0.2);
                                      color: white; }
.status-counts .row.dot-new { border-left-color: #d6d3d1; }
.status-counts .row.dot-called { border-left-color: #93c5fd; }
.status-counts .row.dot-reached { border-left-color: #bfdbfe; }
.status-counts .row.dot-interested { border-left-color: #4ade80; }
.status-counts .row.dot-not_interested { border-left-color: #f87171; }
.status-counts .row.dot-follow_up { border-left-color: #fbbf24; }
.status-counts .row.dot-closed_won { border-left-color: #6ee7b7; }
.status-counts .row.dot-closed_lost { border-left-color: #f87171; }
.status-counts .row.dot-disqualified { border-left-color: #6b7280; }
.clear-filter-btn { font-size: 11px; color: #60a5fa; cursor: pointer;
                     background: transparent; border: 0; padding: 4px 0;
                     margin-bottom: 6px; }
.clear-filter-btn:hover { color: #93c5fd; text-decoration: underline; }

table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; padding: 10px; background: #1a1d27; color: #8b92a6;
     font-weight: 600; text-transform: uppercase; font-size: 11px;
     letter-spacing: 0.5px; position: sticky; top: 0; z-index: 1; }
td { padding: 10px; border-bottom: 1px solid #1a1d27; vertical-align: middle; }
tr.lead-row { cursor: pointer; }
tr.lead-row:hover td { background: #161922; }
tr.lead-row.selected td { background: #1e293b; }

.status-badge { padding: 3px 8px; border-radius: 12px; font-size: 11px;
                font-weight: 600; }
.s-new { background: #44403c; color: #d6d3d1; }
.s-called { background: #1e3a8a; color: #93c5fd; }
.s-reached { background: #1e40af; color: #bfdbfe; }
.s-interested { background: #14532d; color: #4ade80; }
.s-not_interested { background: #4a1d1d; color: #fca5a5; }
.s-follow_up { background: #78350f; color: #fbbf24; }
.s-closed_won { background: #064e3b; color: #6ee7b7; }
.s-closed_lost { background: #4a1d1d; color: #fca5a5; }
.s-disqualified { background: #1f2937; color: #6b7280; }

.op-badge { padding: 2px 7px; border-radius: 4px; font-size: 11px;
            font-weight: 600; text-transform: uppercase; display: inline-block; }
.op-none { background: #4a1d1d; color: #fca5a5; }
.op-facebook { background: #1e3a8a; color: #93c5fd; }
.op-instagram { background: #831843; color: #f9a8d4; }
.op-booking { background: #1e40af; color: #bfdbfe; }
.op-airbnb { background: #7f1d1d; color: #fca5a5; }
.op-tripadvisor { background: #14532d; color: #86efac; }
.op-link-in-bio { background: #44403c; color: #d6d3d1; }
.op-whatsapp { background: #064e3b; color: #6ee7b7; }
.op-other, .op-ota-aggregator { background: #422006; color: #fcd34d; }

.assigned-pill { background: #2a2f3d; color: #d6d3d1; padding: 3px 8px;
                  border-radius: 12px; font-size: 11px; }
.assigned-pill.unassigned { color: #6b7280; font-style: italic; }
.assigned-pill.mine { background: #1e3a8a; color: #93c5fd; }

.multi-prop-badge { background: #422006; color: #fbbf24; padding: 2px 7px;
                     border-radius: 10px; font-size: 10px; font-weight: 700;
                     margin-left: 6px; }

.props-list { background: #1a1d27; border-radius: 8px; padding: 10px;
              border-left: 3px solid #fbbf24; }
.props-list .prop { padding: 8px 0; border-bottom: 1px solid #2a2f3d;
                     font-size: 13px; }
.props-list .prop:last-child { border-bottom: 0; }
.props-list .prop .name { font-weight: 600; color: #e8eaf0; }
.props-list .prop .meta { color: #8b92a6; font-size: 11px; margin-top: 2px; }

.res-card { background: #1a1d27; padding: 14px; border-radius: 8px;
            cursor: pointer; border: 2px solid transparent; }
.res-card:hover { border-color: #2563eb; }
.res-card.active { border-color: #2563eb; background: #1e293b; }
.res-card .title { font-weight: 600; font-size: 14px; color: #e8eaf0; }
.res-card .subtitle { font-size: 12px; color: #8b92a6; margin-top: 4px; }

.markdown-body { color: #d6d3d1; line-height: 1.6; font-size: 14px; }
.markdown-body h1 { font-size: 22px; margin: 0 0 12px;
                     color: #e8eaf0; border-bottom: 1px solid #2a2f3d;
                     padding-bottom: 8px; }
.markdown-body h2 { font-size: 18px; margin: 22px 0 10px; color: #e8eaf0;
                     text-transform: none; letter-spacing: 0; }
.markdown-body h3 { font-size: 15px; margin: 18px 0 8px; color: #e8eaf0;
                     text-transform: none; letter-spacing: 0; }
.markdown-body p { margin: 8px 0; }
.markdown-body ul, .markdown-body ol { margin: 8px 0 8px 24px; }
.markdown-body li { margin: 3px 0; }
.markdown-body code { background: #0a0c12; padding: 2px 6px;
                       border-radius: 3px; font-size: 12px;
                       font-family: Consolas, monospace; }
.markdown-body pre { background: #0a0c12; padding: 12px;
                      border-radius: 6px; overflow-x: auto;
                      font-size: 12px; font-family: Consolas, monospace; }
.markdown-body pre code { background: transparent; padding: 0; }
.markdown-body blockquote { border-left: 3px solid #2563eb;
                             padding-left: 12px; color: #8b92a6;
                             margin: 8px 0; }
.markdown-body table { border-collapse: collapse; margin: 12px 0; }
.markdown-body th, .markdown-body td { border: 1px solid #2a2f3d;
                                         padding: 6px 10px; }
.markdown-body th { background: #0a0c12; }
.markdown-body a { color: #60a5fa; }
.markdown-body strong { color: #e8eaf0; }
.markdown-body hr { border: 0; border-top: 1px solid #2a2f3d; margin: 18px 0; }

.empty { text-align: center; padding: 40px; color: #6b7280; }

.leads-toolbar {
  display: grid;
  grid-template-columns: 1fr 200px 200px auto;
  gap: 10px;
  background: #1a1d27;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #2a2f3d;
  margin-bottom: 14px;
  align-items: center;
}
.leads-toolbar input[type="text"] {
  font-size: 14px;
  padding: 11px 14px;
  background: #0a0c12;
  border: 1px solid #2a2f3d;
  border-radius: 8px;
  color: #e8eaf0;
  width: 100%;
  transition: border-color 0.15s;
}
.leads-toolbar input[type="text"]:focus {
  outline: none;
  border-color: #2563eb;
}
.leads-toolbar select {
  padding: 10px 12px;
  font-size: 13px;
  background: #0a0c12;
  border: 1px solid #2a2f3d;
  border-radius: 8px;
  color: #e8eaf0;
  cursor: pointer;
}
.fav-toggle-label {
  display: flex; align-items: center; gap: 8px;
  background: #0a0c12; padding: 10px 14px; border-radius: 8px;
  border: 1px solid #2a2f3d; cursor: pointer; user-select: none;
  font-size: 13px; color: #d6d3d1; white-space: nowrap;
}
.fav-toggle-label:hover { border-color: #fbbf24; }
.fav-toggle-label input { cursor: pointer; }

.leads-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px; gap: 12px; flex-wrap: wrap;
}

.quick-filters {
  display: flex; gap: 6px; flex-wrap: wrap;
}
.quick-filter-pill {
  padding: 5px 11px; border-radius: 20px; font-size: 12px;
  font-weight: 600; cursor: pointer; user-select: none;
  background: #1a1d27; color: #8b92a6;
  border: 1px solid #2a2f3d; display: inline-flex;
  align-items: center; gap: 6px; transition: all 0.15s;
}
.quick-filter-pill:hover { color: #e8eaf0; border-color: #3a3f4d; }
.quick-filter-pill .count {
  background: #2a2f3d; padding: 1px 7px; border-radius: 10px;
  font-size: 10px; color: #d6d3d1;
}
.quick-filter-pill.active {
  background: #1e40af; color: white; border-color: #60a5fa;
}
.quick-filter-pill.active .count {
  background: rgba(255,255,255,0.25); color: white;
}
.quick-filter-pill.dot-new { border-left: 3px solid #d6d3d1; }
.quick-filter-pill.dot-called { border-left: 3px solid #93c5fd; }
.quick-filter-pill.dot-reached { border-left: 3px solid #bfdbfe; }
.quick-filter-pill.dot-interested { border-left: 3px solid #4ade80; }
.quick-filter-pill.dot-follow_up { border-left: 3px solid #fbbf24; }
.quick-filter-pill.dot-not_interested { border-left: 3px solid #f87171; }
.quick-filter-pill.dot-closed_won { border-left: 3px solid #6ee7b7; }
.quick-filter-pill.dot-closed_lost { border-left: 3px solid #f87171; }
.quick-filter-pill.dot-disqualified { border-left: 3px solid #6b7280; }

.action-btn { background: #1e40af; color: #bfdbfe; padding: 4px 8px;
              border-radius: 4px; font-size: 11px; font-weight: 500;
              text-decoration: none; }
.action-btn:hover { background: #2563eb; color: white; }

/* Side panel */
.panel-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5);
                  display: none; z-index: 100; }
.panel-overlay.open { display: block; }
.side-panel { position: fixed; top: 0; right: 0; bottom: 0; width: 480px;
              background: #14171f; border-left: 1px solid #2a2f3d;
              z-index: 101; transform: translateX(100%);
              transition: transform 0.25s; overflow-y: auto; }
.side-panel.open { transform: translateX(0); }
.panel-header { padding: 18px 20px; border-bottom: 1px solid #2a2f3d;
                display: flex; justify-content: space-between;
                align-items: flex-start; gap: 12px; position: sticky;
                top: 0; background: #14171f; z-index: 1; }
.panel-close { background: transparent; color: #8b92a6; border: 0;
               font-size: 20px; cursor: pointer; padding: 4px 8px; }
.panel-body { padding: 18px 20px; }
.panel-body h3 { font-size: 11px; text-transform: uppercase; color: #8b92a6;
                  letter-spacing: 0.5px; margin: 18px 0 8px; }
.panel-body h3:first-child { margin-top: 0; }
.panel-body .name { font-size: 19px; font-weight: 700; color: #e8eaf0; }
.panel-body .meta { font-size: 13px; color: #8b92a6; margin-top: 2px; }

.panel-actions { display: grid; grid-template-columns: 1fr 1fr 1fr;
                  gap: 6px; margin: 12px 0 18px; }
.panel-actions a { background: #2563eb; color: white; padding: 9px;
                    border-radius: 6px; text-align: center; font-size: 13px;
                    font-weight: 600; text-decoration: none;
                    display: flex; align-items: center; justify-content: center;
                    gap: 6px; }
.panel-actions a.wa { background: #16a34a; }
.panel-actions a.email { background: #7c3aed; }
.panel-actions a.disabled { opacity: 0.4; pointer-events: none; }

.info-row { display: flex; justify-content: space-between; padding: 7px 0;
            border-bottom: 1px solid #1a1d27; font-size: 13px; }
.info-row .label { color: #8b92a6; }
.info-row .value { color: #e8eaf0; max-width: 60%; text-align: right;
                    word-break: break-word; }
.copy-btn { background: #1a1d27; border: 1px solid #2a2f3d; color: #8b92a6;
             padding: 2px 6px; border-radius: 4px; font-size: 11px;
             cursor: pointer; margin-left: 6px; }
.copy-btn:hover { color: #e8eaf0; }

.action-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px;
              margin: 10px 0; }
.action-row button { padding: 10px 6px; font-size: 12px; background: #2a2f3d;
                      color: #d6d3d1; border: 2px solid transparent;
                      border-radius: 6px; cursor: pointer; font-weight: 600; }
.action-row button:hover { background: #3a3f4d; }
.action-row button.active { background: #1e40af; color: white;
                              border-color: #60a5fa; }
.action-row button.active.no-answer { background: #78350f; border-color: #fbbf24; }
.action-row button.active.wrong-number { background: #4a1d1d; border-color: #f87171; }
.save-bar { background: #1a1d27; border: 1px solid #2a2f3d;
            padding: 12px; border-radius: 8px; margin-top: 16px;
            position: sticky; bottom: 0; }
.dirty-indicator { color: #fbbf24; font-size: 11px; margin-bottom: 6px;
                    display: none; }
.dirty-indicator.show { display: block; }

.fav-star { background: transparent; border: 0; cursor: pointer;
            font-size: 18px; padding: 2px 6px; color: #4b5563;
            transition: color 0.15s, transform 0.15s; }
.fav-star:hover { color: #fbbf24; transform: scale(1.15); }
.fav-star.active { color: #fbbf24; }
.fav-toggle { padding: 6px 10px; }

.timeline .item .actions { float: right; display: none; gap: 4px; }
.timeline .item:hover .actions { display: inline-flex; }
.timeline .item .actions button { background: transparent; border: 0;
                                    color: #6b7280; cursor: pointer;
                                    font-size: 11px; padding: 2px 6px; }
.timeline .item .actions button:hover { color: #fca5a5; }
.timeline .item.editing { background: #1e293b; }
.timeline .item textarea { width: 100%; min-height: 50px; margin-top: 4px; }

.timeline { margin-top: 8px; }
.timeline .item { padding: 10px 12px; background: #1a1d27;
                   border-left: 3px solid #2563eb; border-radius: 4px;
                   margin-bottom: 6px; font-size: 13px; }
.timeline .item .meta-line { color: #8b92a6; font-size: 11px;
                              margin-bottom: 3px; }
.timeline .item.action-status_change { border-left-color: #fbbf24; }
.timeline .item.action-called { border-left-color: #93c5fd; }
.timeline .item.action-reached { border-left-color: #4ade80; }
.timeline .item.action-note { border-left-color: #c084fc; }
.timeline .item.action-assigned { border-left-color: #f59e0b; }

.feed-item { padding: 10px 14px; background: #1a1d27; border-radius: 6px;
              margin-bottom: 8px; font-size: 13px; }
.feed-item .meta-line { color: #8b92a6; font-size: 11px; margin-bottom: 4px; }

.hidden { display: none !important; }

.notify { position: fixed; top: 70px; right: 20px; background: #14532d;
          color: #4ade80; padding: 10px 16px; border-radius: 6px;
          font-size: 13px; font-weight: 600; z-index: 200;
          box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.notify.fade { opacity: 0; transition: opacity 0.5s; }

/* Daily plan */
.dp-card { background: #1a1d27; padding: 16px; border-radius: 8px;
            margin-bottom: 12px; }
.dp-card h3 { font-size: 14px; color: #e8eaf0; margin: 0 0 8px;
               text-transform: none; letter-spacing: 0; }
.dp-card .count { font-size: 28px; font-weight: 700; color: #60a5fa; }
.dp-card .small { color: #8b92a6; font-size: 12px; }

/* Admin */
.user-row { display: flex; align-items: center; gap: 10px; padding: 10px;
             background: #1a1d27; border-radius: 6px; margin-bottom: 6px; }
.user-row .name { flex: 1; }
.user-row .role { font-size: 11px; padding: 3px 8px; border-radius: 12px;
                   background: #2a2f3d; color: #d6d3d1; }
.user-row .role.admin { background: #422006; color: #fbbf24; }
</style>
</head>
<body>

<div class="top">
  <h1><img src="/static/logo.png" alt="Devox"></h1>
  <div class="center-title">Sales</div>
  <div class="nav">
    <a id="nav-leads" class="active" data-view="leads">Leads</a>
    <a id="nav-plan" data-view="plan">My Day</a>
    <a id="nav-feed" data-view="feed">Activity</a>
    <a id="nav-resources" data-view="resources">📚 Resources</a>
    <a id="nav-proposal" data-view="proposal">📄 Proposal</a>
    <a id="nav-admin" data-view="admin" style="display:none">Admin</a>
  </div>
  <div class="spacer"></div>
  <div class="user-info">
    <span id="online-now" class="live"></span>
    <span class="badge">Hi, {{ user.full_name }}</span>
    <span id="calls-today-badge" class="target-badge">0/20 calls today</span>
    <a href="/logout">Logout</a>
  </div>
</div>

<div class="container">
  <aside class="sidebar">
    <div id="sidebar-leads">
      <h2>View</h2>
      <div class="filter-group">
        <div class="toggle-row">
          <button id="t-mine" data-mine="1">My Leads</button>
          <button id="t-all" class="active" data-mine="0">All Leads</button>
        </div>
      </div>

      <h2>Quick Stats</h2>
      <div class="status-counts" id="status-counts"></div>
    </div>

    <div id="sidebar-admin" class="hidden">
      <h2>Users</h2>
      <div id="users-list"></div>
      <button class="btn" id="btn-new-user" style="width:100%; margin-top:10px">
        + Create user
      </button>
    </div>
  </aside>

  <main class="main">
    <!-- LEADS VIEW -->
    <div id="view-leads">
      <div class="leads-toolbar">
        <input id="filter-text-top" type="text"
                placeholder="🔍 Search leads by name, phone, region, category, email...">
        <select id="filter-region-top">
          <option value="">📍 All regions</option>
        </select>
        <select id="filter-assignee-top">
          <option value="">👤 All assignees</option>
        </select>
        <label class="fav-toggle-label">
          <input id="filter-fav-top" type="checkbox">
          <span>⭐ Favorites</span>
        </label>
      </div>

      <div class="leads-header">
        <h2 style="margin:0">Leads
          <span id="lead-count" style="color:#8b92a6;font-weight:400;font-size:13px"></span>
        </h2>
        <div class="quick-filters" id="quick-status-filters"></div>
      </div>

      <table>
        <thead><tr>
          <th>★</th><th>Status</th><th>Name</th><th>Region</th><th>Online</th>
          <th>Phone</th><th>Domain</th><th>Assigned</th>
        </tr></thead>
        <tbody id="leads-body">
          <tr><td colspan="8" class="empty">Loading...</td></tr>
        </tbody>
      </table>
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
      <h2>Proposal Generator</h2>
      <div style="display:grid;grid-template-columns:380px 1fr;gap:18px">
        <div style="background:#1a1d27;padding:18px;border-radius:8px">
          <div class="filter-group">
            <label>Lead (optional — autofills from selected lead)</label>
            <select id="prop-lead-select">
              <option value="">— Manual entry —</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Hotel / Property name</label>
            <input id="prop-name" type="text" placeholder="e.g. Hotel Cyclades">
          </div>
          <div class="filter-group">
            <label>Property type</label>
            <select id="prop-type">
              <option value="villa">Villa / House</option>
              <option value="hotel">Hotel</option>
              <option value="apartments">Apartments / Studios</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Location (full)</label>
            <input id="prop-location" type="text" placeholder="e.g. Naoussa, Paros">
          </div>
          <div class="filter-group">
            <label>Date</label>
            <input id="prop-date" type="text" placeholder="DD/MM/YYYY">
          </div>
          <div class="filter-group">
            <label>Author names</label>
            <input id="prop-authors" type="text"
                   placeholder="e.g. Οδυσσέας Στάβερης & Γιώργος Σπύρου">
          </div>
          <div class="filter-group">
            <label>Author phone</label>
            <input id="prop-phone" type="text" value="+30 694 792 0875">
          </div>
          <div class="filter-group">
            <label>Author email</label>
            <input id="prop-email" type="text" value="info@devox.gr">
          </div>
          <div class="filter-group">
            <label>Option A price</label>
            <input id="prop-price-a" type="text" value="€700 – €900">
          </div>
          <div class="filter-group">
            <label>Option B price</label>
            <input id="prop-price-b" type="text" value="€1.500 – €2.000">
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <button class="btn" id="prop-preview">👁 Preview</button>
            <button class="btn success" id="prop-download">⬇ Download HTML</button>
          </div>
        </div>
        <div id="prop-preview-area"
             style="background:white;border-radius:8px;
                    min-height:600px;overflow:auto">
          <div style="color:#6b7280;padding:40px;text-align:center">
            Fill the form and click Preview to see the proposal here.
          </div>
        </div>
      </div>
    </div>

    <!-- ADMIN VIEW -->
    <div id="view-admin" class="hidden">
      <h2>User Management</h2>
      <div id="admin-users"></div>
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
let users = [];
let activeFilterRegion = '';
let activeFilterAssignee = '';
let filterText = '';
let searchTimer = null;
let selectedPhone = null;
let currentView = 'leads';

// ----------------- View switching -----------------
function setView(v) {
  currentView = v;
  for (const id of ['leads', 'plan', 'feed', 'admin', 'resources', 'proposal']) {
    const view = document.getElementById('view-' + id);
    if (view) view.classList.toggle('hidden', id !== v);
    const link = document.getElementById('nav-' + id);
    if (link) link.classList.toggle('active', id === v);
  }
  document.getElementById('sidebar-leads').classList.toggle('hidden', v !== 'leads');
  document.getElementById('sidebar-admin').classList.toggle('hidden', v !== 'admin');
  if (v === 'plan') refreshPlan();
  if (v === 'admin') refreshUsers();
  if (v === 'feed') loadRecentActivity();
  if (v === 'resources') loadResources();
  if (v === 'proposal') initProposalForm();
}

for (const link of document.querySelectorAll('.nav a')) {
  link.onclick = () => setView(link.dataset.view);
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
  if (favOnly) params.set('favorites', '1');
  if (activeStatus) params.set('status', activeStatus);
  if (activeFilterRegion) params.set('region', activeFilterRegion);
  if (activeFilterAssignee) params.set('assigned_to', activeFilterAssignee);
  if (filterText) params.set('q', filterText);

  const r = await fetch('/api/leads?' + params.toString());
  const data = await r.json();
  allLeads = data.leads;

  const allStatuses = ['new','called','reached','interested','follow_up',
                        'not_interested','closed_won','closed_lost','disqualified'];
  const STATUS_ICONS = {
    new: '🆕', called: '📞', reached: '💬', interested: '✅',
    follow_up: '📅', not_interested: '❌', closed_won: '🤝',
    closed_lost: '🚫', disqualified: '🗑️',
  };

  // Sidebar quick stats (compact list)
  const statusEl = document.getElementById('status-counts');
  let html = '';
  if (activeStatus) {
    html += `<button class="clear-filter-btn" id="clear-status-filter">
      ✕ Clear status filter</button>`;
  }
  html += allStatuses.map(s => {
    const n = data.by_status[s] || 0;
    const cls = s === activeStatus ? 'row active' : 'row';
    return `<div class="${cls} dot-${s}" data-status="${s}">
      <span class="label">${STATUS_ICONS[s]||''} ${STATUS_LABEL[s]}</span>
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
        ${STATUS_ICONS[s]||''} ${STATUS_LABEL[s]}
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

  // Region dropdown (top)
  const regSel = document.getElementById('filter-region-top');
  if (regSel) {
    const cur = regSel.value;
    regSel.innerHTML = '<option value="">📍 All regions</option>' +
      data.by_region.map(r =>
        `<option value="${escapeHtml(r.region)}">${escapeHtml(r.region)} (${r.count})</option>`
      ).join('');
    regSel.value = cur;
  }

  renderLeads();
}

function renderLeads() {
  const rows = allLeads;
  document.getElementById('lead-count').textContent = `(${rows.length} shown)`;
  const tbody = document.getElementById('leads-body');
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="empty">No leads match</td></tr>';
    return;
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
    return `<tr class="${rowClass}" data-phone="${escapeHtml(phone)}">
       <td><button class="${starCls}" data-phone="${escapeHtml(phone)}" data-fav="${l.is_favorite?1:0}">${starChar}</button></td>
       <td><span class="status-badge s-${status}">${STATUS_LABEL[status]||status}</span></td>
       <td><b>${escapeHtml(l.name||'')}</b>${propBadge}<br>
           <span style="color:#8b92a6;font-size:11px">${escapeHtml(l.category||'')}</span></td>
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

document.getElementById('t-mine').onclick = () => {
  myMode = 1; document.getElementById('t-mine').classList.add('active');
  document.getElementById('t-all').classList.remove('active');
  refreshLeads();
};
document.getElementById('t-all').onclick = () => {
  myMode = 0; document.getElementById('t-all').classList.add('active');
  document.getElementById('t-mine').classList.remove('active');
  refreshLeads();
};
document.getElementById('filter-text-top').oninput = e => {
  filterText = e.target.value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(refreshLeads, 250);
};
document.getElementById('filter-region-top').onchange = e => {
  activeFilterRegion = e.target.value;
  if (activeFilterRegion && !activeStatus) activeStatus = 'new';
  refreshLeads();
};
document.getElementById('filter-assignee-top').onchange = e => {
  activeFilterAssignee = e.target.value; refreshLeads();
};
document.getElementById('filter-fav-top').onchange = e => {
  favOnly = e.target.checked; refreshLeads();
};

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
  // Top assignee dropdown
  const topSel = document.getElementById('filter-assignee-top');
  if (topSel) {
    const cur = topSel.value;
    topSel.innerHTML = '<option value="">👤 All assignees</option>' +
      '<option value="unassigned">— Unassigned —</option>' +
      users.map(u => `<option value="${u.id}">${escapeHtml(u.full_name)}</option>`).join('');
    topSel.value = cur;
  }
}

async function refreshUsers() {
  await loadUsers();
  const list = document.getElementById('admin-users');
  list.innerHTML = users.map(u => `
    <div class="user-row">
      <div class="name"><b>${escapeHtml(u.full_name)}</b>
        <span style="color:#8b92a6"> · @${escapeHtml(u.username)}</span></div>
      <span class="role ${u.role}">${escapeHtml(u.role)}</span>
      ${u.id !== ME.id ? `
        <button class="btn secondary" onclick="resetPwd(${u.id})">Reset PW</button>
        <button class="btn danger" onclick="deactivateUser(${u.id})">Deactivate</button>
      ` : ''}
    </div>
  `).join('');
}

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
  if (!confirm('Deactivate this user?')) return;
  await fetch('/api/users/' + uid, { method: 'DELETE' });
  refreshUsers();
}
window.resetPwd = resetPwd;
window.deactivateUser = deactivateUser;

document.getElementById('btn-new-user').onclick = async () => {
  const username = prompt('Username (no spaces):'); if (!username) return;
  const full_name = prompt('Full name:'); if (!full_name) return;
  const password = prompt('Password (min 6 chars):'); if (!password) return;
  const role = confirm('OK = admin, Cancel = sales') ? 'admin' : 'sales';
  const r = await fetch('/api/users', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ username, full_name, password, role }),
  });
  if (r.ok) { refreshUsers(); notify('User created'); }
  else { const d = await r.json(); alert(d.error || 'Failed'); }
};

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
    if (data.type === 'leads_synced') {
      notify(`${data.count} new leads imported`);
      refreshLeads();
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

// Init
loadUsers();
refreshLeads();
refreshDailyCounter();
setInterval(refreshDailyCounter, 30000);
</script>
</body>
</html>"""
