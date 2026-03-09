"""
Configuration loader for the HoI4 Mod Validator.
Reads validator.yml and exposes a Config dataclass.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


@dataclass
class SuppressRule:
    """A rule to suppress specific issue codes for specific files/patterns."""
    code: str
    path_glob: str = "*"
    reason: str = ""


@dataclass
class Config:
    # Paths
    submod_path: str = "."
    md_path: Optional[str] = None
    vanilla_path: Optional[str] = None
    cache_dir: str = ".validator_cache"

    # Validator toggles
    validate_syntax: bool = True
    validate_references: bool = True
    validate_logic: bool = True
    validate_localization: bool = True
    validate_assets: bool = True

    # Reporting
    output_format: str = "json"      # json | markdown | html | all
    output_file: Optional[str] = None
    summary_output: Optional[str] = None  # path to write markdown summary
    emit_annotations: bool = False    # GitHub Actions annotations
    max_issues: int = 1000

    # Suppression
    suppress: list[SuppressRule] = field(default_factory=list)

    # Millennium Dawn specific
    md_country_tags: list[str] = field(default_factory=list)
    md_ideologies: list[str] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Load configuration from a YAML file."""
        if not _YAML_AVAILABLE:
            raise RuntimeError(
                "PyYAML is required to load configuration files. "
                "Install it with: pip install pyyaml"
            )
        cfg = cls()
        if not Path(path).exists():
            return cfg

        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

        # Paths
        paths = data.get("paths", {})
        cfg.submod_path = paths.get("submod", cfg.submod_path)
        cfg.md_path = paths.get("millennium_dawn", cfg.md_path)
        cfg.vanilla_path = paths.get("vanilla", cfg.vanilla_path)
        cfg.cache_dir = paths.get("cache_dir", cfg.cache_dir)

        # Override from environment variables
        if os.environ.get("SUBMOD_PATH"):
            cfg.submod_path = os.environ["SUBMOD_PATH"]
        if os.environ.get("MD_PATH"):
            cfg.md_path = os.environ["MD_PATH"]
        if os.environ.get("VANILLA_PATH"):
            cfg.vanilla_path = os.environ["VANILLA_PATH"]

        # Validators
        validators = data.get("validators", {})
        cfg.validate_syntax = validators.get("syntax", cfg.validate_syntax)
        cfg.validate_references = validators.get("references", cfg.validate_references)
        cfg.validate_logic = validators.get("logic", cfg.validate_logic)
        cfg.validate_localization = validators.get("localization", cfg.validate_localization)
        cfg.validate_assets = validators.get("assets", cfg.validate_assets)

        # Reporting
        reporting = data.get("reporting", {})
        cfg.output_format = reporting.get("format", cfg.output_format)
        cfg.output_file = reporting.get("output_file", cfg.output_file)
        cfg.summary_output = reporting.get("summary_output", cfg.summary_output)
        cfg.emit_annotations = reporting.get("annotations", cfg.emit_annotations)
        cfg.max_issues = reporting.get("max_issues", cfg.max_issues)

        # Suppression rules
        for rule_data in (data.get("suppress") or []):
            if isinstance(rule_data, dict):
                cfg.suppress.append(SuppressRule(
                    code=rule_data.get("code", ""),
                    path_glob=rule_data.get("path", "*"),
                    reason=rule_data.get("reason", ""),
                ))

        # MD specific
        md_cfg = data.get("millennium_dawn", {})
        cfg.md_country_tags = md_cfg.get("extra_tags", [])
        cfg.md_ideologies = md_cfg.get("ideologies", [])

        return cfg

    @classmethod
    def from_args(cls, args) -> "Config":
        """Build Config from parsed CLI arguments, optionally overlaying a config file."""
        if hasattr(args, "config") and args.config:
            cfg = cls.from_file(args.config)
        else:
            cfg = cls()

        if hasattr(args, "format") and args.format:
            cfg.output_format = args.format
        if hasattr(args, "output") and args.output:
            cfg.output_file = args.output
        if hasattr(args, "summary_output") and args.summary_output:
            cfg.summary_output = args.summary_output
        if hasattr(args, "annotations") and args.annotations:
            cfg.emit_annotations = True
        if hasattr(args, "submod_path") and args.submod_path:
            cfg.submod_path = args.submod_path
        if hasattr(args, "md_path") and args.md_path:
            cfg.md_path = args.md_path

        return cfg
