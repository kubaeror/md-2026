"""HTML report formatter (for GitHub Actions artifact)."""
from __future__ import annotations
import html
from pathlib import Path
from .models import ValidationReport, Issue, Severity

_SEVERITY_COLOR = {
    Severity.ERROR:   "#dc3545",
    Severity.WARNING: "#fd7e14",
    Severity.INFO:    "#0d6efd",
    Severity.HINT:    "#6c757d",
}

_SEVERITY_BG = {
    Severity.ERROR:   "#fff5f5",
    Severity.WARNING: "#fffbf0",
    Severity.INFO:    "#f0f7ff",
    Severity.HINT:    "#f8f9fa",
}


def format_html(report: ValidationReport) -> str:
    status_color = "#198754" if report.passed else "#dc3545"
    status_text = "PASSED" if report.passed else "FAILED"

    issues_html = _render_issues(report)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HoI4 Mod Validator Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          margin: 0; padding: 20px; background: #f8f9fa; color: #212529; }}
  .header {{ background: #1a1a2e; color: white; padding: 20px 30px;
             border-radius: 8px; margin-bottom: 20px; }}
  .status {{ font-size: 1.8em; font-weight: bold; color: {status_color}; }}
  .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                   gap: 15px; margin-bottom: 20px; }}
  .metric {{ background: white; border-radius: 8px; padding: 15px; text-align: center;
             box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
  .metric .value {{ font-size: 2em; font-weight: bold; }}
  .metric .label {{ color: #6c757d; font-size: 0.85em; }}
  .issues-section {{ background: white; border-radius: 8px; padding: 20px;
                     box-shadow: 0 1px 3px rgba(0,0,0,.1); margin-bottom: 20px; }}
  .issue {{ border-left: 4px solid #dee2e6; padding: 8px 12px; margin: 6px 0;
            border-radius: 0 4px 4px 0; font-size: 0.9em; }}
  .issue .loc {{ font-family: monospace; color: #6c757d; font-size: 0.85em; }}
  .issue .code {{ font-family: monospace; font-weight: bold; }}
  .issue .msg {{ margin-top: 2px; }}
  .filter-bar {{ margin-bottom: 15px; }}
  .filter-bar input {{ padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px;
                        width: 300px; font-size: 0.9em; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ background: #f1f3f4; padding: 8px 12px; text-align: left;
        border-bottom: 2px solid #dee2e6; font-size: 0.85em; }}
  td {{ padding: 6px 12px; border-bottom: 1px solid #f1f3f4; font-size: 0.85em; }}
  tr:hover td {{ background: #f8f9fa; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px;
             font-size: 0.75em; font-weight: bold; color: white; }}
</style>
</head>
<body>
<div class="header">
  <div class="status">{html.escape(status_text)}</div>
  <div>HoI4 Mod Validator &mdash; {html.escape(report.timestamp)}</div>
  <div style="margin-top:8px;font-size:0.9em;opacity:0.8">
    Submod: <code>{html.escape(report.submod_path)}</code>
  </div>
</div>

<div class="summary-grid">
  <div class="metric">
    <div class="value" style="color:#6c757d">{report.files_scanned}</div>
    <div class="label">Files Scanned</div>
  </div>
  <div class="metric">
    <div class="value" style="color:#dc3545">{report.error_count}</div>
    <div class="label">Errors</div>
  </div>
  <div class="metric">
    <div class="value" style="color:#fd7e14">{report.warning_count}</div>
    <div class="label">Warnings</div>
  </div>
  <div class="metric">
    <div class="value" style="color:#0d6efd">{report.info_count}</div>
    <div class="label">Info / Hints</div>
  </div>
</div>

<div class="issues-section">
  <h2>Issues ({len(report.issues)} total)</h2>
  <div class="filter-bar">
    <input type="text" id="filter" placeholder="Filter by file, code, or message..." oninput="filterIssues()">
  </div>
  <table id="issues-table">
    <thead>
      <tr>
        <th>Severity</th>
        <th>File</th>
        <th>Line</th>
        <th>Code</th>
        <th>Message</th>
      </tr>
    </thead>
    <tbody>
      {issues_html}
    </tbody>
  </table>
</div>

<script>
function filterIssues() {{
  const q = document.getElementById('filter').value.toLowerCase();
  const rows = document.querySelectorAll('#issues-table tbody tr');
  rows.forEach(row => {{
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
</script>
</body>
</html>"""


def _render_issues(report: ValidationReport) -> str:
    if not report.issues:
        return '<tr><td colspan="5" style="text-align:center;color:#6c757d">No issues found 🎉</td></tr>'

    rows = []
    for issue in sorted(report.issues, key=lambda i: (i.severity.value, i.file, i.line)):
        color = _SEVERITY_COLOR[issue.severity]
        fname = html.escape(issue.file.split("/")[-1] if "/" in issue.file else issue.file)
        full_path = html.escape(issue.file)
        msg = html.escape(issue.message)
        code = html.escape(issue.code)
        sev = html.escape(issue.severity.value.upper())
        rows.append(
            f'<tr>'
            f'<td><span class="badge" style="background:{color}">{sev}</span></td>'
            f'<td title="{full_path}"><code>{fname}</code></td>'
            f'<td>{issue.line}</td>'
            f'<td><code>{code}</code></td>'
            f'<td>{msg}</td>'
            f'</tr>'
        )
    return "\n".join(rows)


def write_html(report: ValidationReport, output_path: str) -> None:
    Path(output_path).write_text(format_html(report), encoding="utf-8")
