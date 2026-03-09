"""
Entry point for the HoI4 Mod Validator.
Invoked as:  python -m hoi4_mod_validator.main [options]
"""
from __future__ import annotations
import argparse
import fnmatch
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import Config
from .index.builder import IndexBuilder
from .reporting.models import ValidationReport, Issue, Severity
from .reporting.formatter_json import write_json, format_json
from .reporting.formatter_markdown import write_markdown, format_markdown
from .reporting.formatter_html import write_html


log = logging.getLogger("hoi4_mod_validator")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )


def _apply_suppression(issues: list[Issue], cfg: Config) -> list[Issue]:
    """Remove issues that match suppression rules."""
    if not cfg.suppress:
        return issues
    result = []
    for issue in issues:
        suppressed = False
        for rule in cfg.suppress:
            if rule.code and rule.code != issue.code:
                continue
            if rule.path_glob and not fnmatch.fnmatch(issue.file, rule.path_glob):
                continue
            suppressed = True
            break
        if not suppressed:
            result.append(issue)
    return result


def _emit_annotations(issues: list[Issue]) -> None:
    """Print GitHub Actions workflow commands for each issue."""
    for issue in issues:
        print(issue.to_github_annotation(), flush=True)


def run_validation(cfg: Config) -> ValidationReport:
    """Run the full validation pipeline and return a report."""
    report = ValidationReport(
        submod_path=cfg.submod_path,
        md_path=cfg.md_path or "",
        vanilla_path=cfg.vanilla_path or "",
    )

    # ── Build index ────────────────────────────────────────────────────────
    log.info("Building definition index…")
    builder = IndexBuilder(
        vanilla_path=cfg.vanilla_path,
        md_path=cfg.md_path,
        submod_path=cfg.submod_path,
        cache_dir=cfg.cache_dir,
    )
    registry = builder.build()

    # Count scanned files in submod
    submod_dir = Path(cfg.submod_path)
    report.files_scanned = sum(
        1 for _ in submod_dir.rglob("*.txt")
        if not any(p in str(_) for p in ("vanilla", "millennium_dawn", ".validator_cache"))
    )

    all_issues: list[Issue] = []

    # ── Layer 1: Syntax ────────────────────────────────────────────────────
    if cfg.validate_syntax:
        log.info("Running syntax validation…")
        from .validators.syntax import SyntaxValidator
        issues = SyntaxValidator(cfg.submod_path).validate()
        log.info("  Syntax: %d issue(s)", len(issues))
        all_issues.extend(issues)

    # ── Layer 2: References ────────────────────────────────────────────────
    if cfg.validate_references:
        log.info("Running reference validation…")
        from .validators.references import ReferenceValidator
        issues = ReferenceValidator(cfg.submod_path, registry).validate()
        log.info("  References: %d issue(s)", len(issues))
        all_issues.extend(issues)

    # ── Layer 3: Logic ─────────────────────────────────────────────────────
    if cfg.validate_logic:
        log.info("Running logic validation…")
        from .validators.logic import LogicValidator
        issues = LogicValidator(cfg.submod_path).validate()
        log.info("  Logic: %d issue(s)", len(issues))
        all_issues.extend(issues)

    # ── Layer 4: Localization ──────────────────────────────────────────────
    if cfg.validate_localization:
        log.info("Running localization validation…")
        from .validators.localization import LocalizationValidator
        issues = LocalizationValidator(cfg.submod_path, registry).validate()
        log.info("  Localization: %d issue(s)", len(issues))
        all_issues.extend(issues)

    # ── Layer 5: Assets ────────────────────────────────────────────────────
    if cfg.validate_assets:
        log.info("Running asset validation…")
        from .validators.assets import AssetValidator
        issues = AssetValidator(
            cfg.submod_path, registry,
            md_path=cfg.md_path,
            vanilla_path=cfg.vanilla_path,
        ).validate()
        log.info("  Assets: %d issue(s)", len(issues))
        all_issues.extend(issues)

    # ── Apply suppression ──────────────────────────────────────────────────
    all_issues = _apply_suppression(all_issues, cfg)

    # Truncate if needed
    if len(all_issues) > cfg.max_issues:
        log.warning("Too many issues (%d), truncating to %d", len(all_issues), cfg.max_issues)
        all_issues = all_issues[:cfg.max_issues]

    report.issues = sorted(all_issues, key=lambda i: (i.file, i.line))
    return report


def write_reports(report: ValidationReport, cfg: Config) -> None:
    """Write report(s) in the configured format(s)."""
    fmt = cfg.output_format.lower()

    if fmt in ("json", "all"):
        out = cfg.output_file or "validation-report.json"
        if fmt == "all":
            out = "validation-report.json"
        write_json(report, out)
        log.info("JSON report written to %s", out)

    if fmt in ("markdown", "all"):
        out = cfg.output_file or "validation-report.md"
        if fmt == "all":
            out = "validation-summary.md"
        write_markdown(report, out)
        log.info("Markdown report written to %s", out)

    if fmt in ("html", "all"):
        out = cfg.output_file or "validation-report.html"
        if fmt == "all":
            out = "validation-report.html"
        write_html(report, out)
        log.info("HTML report written to %s", out)

    # GitHub Step Summary
    if cfg.summary_output:
        md_content = format_markdown(report)
        Path(cfg.summary_output).write_text(md_content, encoding="utf-8")
        log.info("Summary written to %s", cfg.summary_output)

    # Also write summary.md for PR comment (always)
    if fmt == "json":
        write_markdown(report, "validation-summary.md")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hoi4_mod_validator",
        description="Static validator for HoI4 / Millennium Dawn submods",
    )
    parser.add_argument("--config", "-c", default="validator.yml",
                        help="Path to validator.yml config file")
    parser.add_argument("--format", "-f", choices=["json", "markdown", "html", "all"],
                        help="Output format")
    parser.add_argument("--output", "-o",
                        help="Output file path")
    parser.add_argument("--summary-output",
                        help="Write Markdown summary to this path (for GITHUB_STEP_SUMMARY)")
    parser.add_argument("--annotations", action="store_true",
                        help="Emit GitHub Actions annotations")
    parser.add_argument("--submod-path",
                        help="Path to submod directory (overrides config)")
    parser.add_argument("--md-path",
                        help="Path to Millennium Dawn directory (overrides config)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose logging")
    args = parser.parse_args(argv)

    _setup_logging(args.verbose)
    cfg = Config.from_args(args)

    log.info("Starting HoI4 Mod Validator")
    log.info("  Submod: %s", cfg.submod_path)
    log.info("  Millennium Dawn: %s", cfg.md_path or "not provided")
    log.info("  Vanilla: %s", cfg.vanilla_path or "not provided")

    try:
        report = run_validation(cfg)
    except Exception as exc:
        log.exception("Validation failed with an unexpected error: %s", exc)
        return 2

    write_reports(report, cfg)

    if cfg.emit_annotations:
        _emit_annotations(report.issues)

    # Print summary to stderr
    status = "PASSED" if report.passed else "FAILED"
    print(
        f"\nValidation {status}: "
        f"{report.error_count} error(s), "
        f"{report.warning_count} warning(s), "
        f"{report.info_count} info/hint(s) "
        f"in {report.files_scanned} file(s)",
        file=sys.stderr,
    )

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
