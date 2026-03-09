"""JSON report formatter."""
from __future__ import annotations
import json
from pathlib import Path
from .models import ValidationReport, Issue, Severity


def _issue_to_dict(issue: Issue) -> dict:
    return {
        "severity": issue.severity.value,
        "file": issue.file,
        "line": issue.line,
        "column": issue.column,
        "code": issue.code,
        "message": issue.message,
        "context": issue.context,
        "suggestion": issue.suggestion,
    }


def format_json(report: ValidationReport, indent: int = 2) -> str:
    """Serialize the report to a JSON string."""
    data = {
        "timestamp": report.timestamp,
        "submod_path": report.submod_path,
        "md_path": report.md_path,
        "vanilla_path": report.vanilla_path,
        "summary": {
            "passed": report.passed,
            "files_scanned": report.files_scanned,
            "error_count": report.error_count,
            "warning_count": report.warning_count,
            "info_count": report.info_count,
            "total_issues": len(report.issues),
            "parse_errors": len(report.parse_errors),
        },
        "issues": [_issue_to_dict(i) for i in report.issues],
        "parse_errors": report.parse_errors,
    }
    return json.dumps(data, indent=indent, ensure_ascii=False)


def write_json(report: ValidationReport, output_path: str) -> None:
    Path(output_path).write_text(format_json(report), encoding="utf-8")
