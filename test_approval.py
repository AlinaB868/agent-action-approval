
import sqlite3

import pytest

from approval_demo import database
from approval_demo.approval_engine import (
    request_email,
    approve_action,
    reject_action,
    get_actions,
)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    """Each test uses its own temporary SQLite database."""
    test_db = tmp_path / "test_approval.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)
    database.init_db()


def get_action(action_id):
    with database.get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM actions WHERE id = ?",
            (action_id,),
        ).fetchone()

    return dict(row) if row else None


def test_allow():
    result = request_email(
        "ana@firma.ro",
        "Salut",
        "Mesaj de test",
    )

    assert result["status"] == "EXECUTED"
    assert get_action(result["action_id"])["status"] == "EXECUTED"


def test_hold_and_approve():
    result = request_email(
        "extern@exemplu.ro",
        "Document",
        "Mesaj de test",
    )

    assert result["status"] == "PENDING_APPROVAL"

    action_id = result["action_id"]
    assert get_action(action_id)["status"] == "PENDING_APPROVAL"

    approved = approve_action(action_id)

    assert approved["status"] == "EXECUTED"
    assert get_action(action_id)["status"] == "EXECUTED"


def test_hold_and_reject():
    result = request_email(
        "extern2@exemplu.ro",
        "Test",
        "Mesaj de test",
    )

    action_id = result["action_id"]
    rejected = reject_action(action_id)

    assert rejected["status"] == "REJECTED"
    assert get_action(action_id)["status"] == "REJECTED"
    assert get_actions("EXECUTED") == []


def test_cannot_approve_twice():
    result = request_email(
        "extern@exemplu.ro",
        "Test double approval",
        "Mesaj simulat",
    )

    action_id = result["action_id"]

    first = approve_action(action_id)
    second = approve_action(action_id)

    assert first["status"] == "EXECUTED"
    assert second["status"] == "ERROR"

    with database.get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM actions WHERE id = ? AND status = 'EXECUTED'",
            (action_id,),
        ).fetchone()[0]

    assert count == 1


def test_cannot_approve_rejected_action():
    result = request_email(
        "extern@exemplu.ro",
        "Test rejected",
        "Mesaj simulat",
    )

    action_id = result["action_id"]

    rejected = reject_action(action_id)
    approved = approve_action(action_id)

    assert rejected["status"] == "REJECTED"
    assert approved["status"] == "ERROR"
    assert get_action(action_id)["status"] == "REJECTED"


def test_cannot_reject_executed_action():
    result = request_email(
        "ana@firma.ro",
        "Already executed",
        "Mesaj simulat",
    )

    action_id = result["action_id"]
    rejected = reject_action(action_id)

    assert rejected["status"] == "ERROR"
    assert get_action(action_id)["status"] == "EXECUTED"
