import pytest
from commit_msg_guard.parser import CommitParser


def test_co_author_footer_extraction():
    msg = """feat(cli): add co-author parsing

Detailed commit description explaining changes.

Co-authored-by: Stephen Cork <stephencork81@gmail.com>
Co-authored-by: Dean <158058829+oneandonlydean@users.noreply.github.com>
"""
    parser = CommitParser()
    commit = parser.parse(msg)
    assert len(commit.co_authors) == 2
    assert "Stephen Cork <stephencork81@gmail.com>" in commit.co_authors
    assert "Dean <158058829+oneandonlydean@users.noreply.github.com>" in commit.co_authors
    assert commit.to_dict()["co_authors"] == commit.co_authors


def test_commit_without_co_authors():
    msg = "fix(auth): resolve oauth token refresh loop"
    parser = CommitParser()
    commit = parser.parse(msg)
    assert commit.co_authors == []
    assert commit.to_dict()["co_authors"] == []
