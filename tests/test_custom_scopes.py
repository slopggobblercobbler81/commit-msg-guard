"""Tests for custom scope validation regex and whitespace trimming support."""

import pytest
from commit_msg_guard.config import Config
from commit_msg_guard.validator import validate_message


def test_custom_scope_regex_matching():
    # Test custom regex patterns for scope validation (e.g. ticket numbers or specific formats)
    cfg = Config(scope_pattern=r"^JIRA-\d+$")
    
    # Valid matches
    res_valid = validate_message("feat(JIRA-123): implement user dashboard", cfg)
    assert res_valid.is_valid, f"Expected valid, got errors: {[e.message for e in res_valid.errors]}"

    # Invalid matches
    res_invalid = validate_message("feat(jira-123): lowercase not allowed", cfg)
    assert not res_invalid.is_valid
    assert any(e.code == "INVALID_SCOPE_FORMAT" for e in res_invalid.errors)


def test_custom_scope_whitespace_trimming():
    # Test scopes with leading or trailing whitespace when custom pattern or allowed scopes are configured
    cfg = Config(allowed_scopes=["api", "core"])
    
    res = validate_message("fix(api): trim whitespace around scope", cfg)
    assert res.is_valid


def test_custom_scope_complex_regex():
    # Complex regex combining alphanumeric and hyphens with length constraints
    cfg = Config(scope_pattern=r"^[a-z]{2,}-\d{3}$")
    
    assert validate_message("refactor(fix-456): update dependency bounds", cfg).is_valid
    assert not validate_message("refactor(f-456): too short prefix", cfg).is_valid
    assert not validate_message("refactor(fix-45): too short digits", cfg).is_valid
