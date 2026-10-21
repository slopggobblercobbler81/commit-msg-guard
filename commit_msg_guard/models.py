"""Data models for conventional commit representation and validation results."""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any


@dataclass
class ConventionalCommit:
    """Represents a parsed git commit message adhering to Conventional Commits specification."""
    raw_message: str
    clean_message: str
    header: str
    type: Optional[str] = None
    scope: Optional[str] = None
    is_breaking: bool = False
    description: Optional[str] = None
    body: Optional[str] = None
    footers: List[Tuple[str, str]] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)
    is_merge_commit: bool = False
    is_revert_commit: bool = False

    @property
    def co_authors(self) -> List[str]:
        """Extract list of co-authors from Co-authored-by footers."""
        return [f[1] for f in self.footers if f[0].lower() in ("co-authored-by", "coauthored-by")]

    def to_dict(self) -> Dict[str, Any]:
        """Convert commit representation to dictionary."""
        return {
            "header": self.header,
            "type": self.type,
            "scope": self.scope,
            "is_breaking": self.is_breaking,
            "description": self.description,
            "body": self.body,
            "footers": [{"token": f[0], "value": f[1]} for f in self.footers],
            "co_authors": self.co_authors,
            "is_merge_commit": self.is_merge_commit,
            "is_revert_commit": self.is_revert_commit,
        }


@dataclass
class ValidationError:
    """Represents a specific lint or validation error/warning."""
    code: str
    message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    suggestion: Optional[str] = None
    severity: str = "error"  # 'error' or 'warning'

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation error to dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "line_number": self.line_number,
            "column_number": self.column_number,
            "suggestion": self.suggestion,
            "severity": self.severity,
        }


@dataclass
class ValidationResult:
    """Aggregated result of commit message validation."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    commit: Optional[ConventionalCommit] = None
    ignored: bool = False
    ignore_reason: Optional[str] = None

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert full validation result to dictionary."""
        return {
            "is_valid": self.is_valid,
            "ignored": self.ignored,
            "ignore_reason": self.ignore_reason,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "commit": self.commit.to_dict() if self.commit else None,
        }
