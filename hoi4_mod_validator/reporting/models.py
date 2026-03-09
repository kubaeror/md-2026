"""Data models for validation issues and reports."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import datetime


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"

    @property
    def github_level(self) -> str:
        """Map to GitHub Actions annotation level."""
        return {
            Severity.ERROR: "error",
            Severity.WARNING: "warning",
            Severity.INFO: "notice",
            Severity.HINT: "notice",
        }[self]

    @property
    def emoji(self) -> str:
        return {
            Severity.ERROR: "❌",
            Severity.WARNING: "⚠️",
            Severity.INFO: "ℹ️",
            Severity.HINT: "💡",
        }[self]


@dataclass
class Issue:
    """A single validation issue."""
    severity: Severity
    file: str
    line: int
    code: str           # e.g. "REF001", "SYN002"
    message: str
    column: int = 0
    context: Optional[str] = None    # surrounding code snippet
    suggestion: Optional[str] = None # fix suggestion

    @property
    def location(self) -> str:
        if self.column:
            return f"{self.file}:{self.line}:{self.column}"
        return f"{self.file}:{self.line}"

    def to_github_annotation(self) -> str:
        """Format as GitHub Actions workflow command."""
        level = self.severity.github_level
        parts = [f"file={self.file}", f"line={self.line}"]
        if self.column:
            parts.append(f"col={self.column}")
        parts.append(f"title={self.code}")
        props = ",".join(parts)
        return f"::{level} {props}::{self.message}"


@dataclass
class ValidationReport:
    """Complete validation report."""
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    submod_path: str = ""
    md_path: str = ""
    vanilla_path: str = ""
    issues: list[Issue] = field(default_factory=list)
    files_scanned: int = 0
    parse_errors: list[str] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity in (Severity.INFO, Severity.HINT))

    @property
    def passed(self) -> bool:
        return self.error_count == 0

    def issues_by_file(self) -> dict[str, list[Issue]]:
        result: dict[str, list[Issue]] = {}
        for issue in sorted(self.issues, key=lambda i: (i.file, i.line)):
            result.setdefault(issue.file, []).append(issue)
        return result

    def issues_by_code(self) -> dict[str, list[Issue]]:
        result: dict[str, list[Issue]] = {}
        for issue in self.issues:
            result.setdefault(issue.code, []).append(issue)
        return result
