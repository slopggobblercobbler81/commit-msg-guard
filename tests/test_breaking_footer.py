"""Tests for BREAKING CHANGE footers and co-author trailers."""

import pytest
from commit_msg_guard.parser import CommitParser
from commit_msg_guard.validator import validate_message


def test_breaking_change_footer_parsing():
    parser = CommitParser()
    raw = (
        "feat(api): update user endpoint\n\n"
        "BREAKING CHANGE: v1 endpoints have been removed.\n"
        "Co-authored-by: octocat <octocat@github.com>"
    )
    commit = parser.parse(raw)
    assert commit.is_breaking is True
    assert any(token == "BREAKING CHANGE" for token, _ in commit.footers)
    assert any(token == "Co-authored-by" for token, _ in commit.footers)


def test_breaking_change_footer_validation():
    msg = (
        "feat(api)!: remove deprecated v1 API\n\n"
        "BREAKING CHANGE: API v1 is no longer supported.\n\n"
        "Co-authored-by: octocat <octocat@github.com>"
    )
    res = validate_message(msg)
    assert res.is_valid
    assert res.commit.is_breaking is True
