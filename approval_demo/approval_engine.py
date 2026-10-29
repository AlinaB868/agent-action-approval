from uuid import uuid4

from approval_demo.database import get_connection, init_db


def check_recipient(recipient: str) -> str:
    recipient = recipient.strip().lower()
    return "ALLOW" if recipient.endswith("@firma.ro") else "HOLD"


def request_email(recipient: str, subject: str, body: str) -> dict:
    recipient = recipient.strip().lower()

    if not recipient or "@" not in recipient:
        return {"status": "ERROR", "message": "Invalid recipient."}

    init_db()

    action_id = str(uuid4())
    decision = check_recipient(recipient)
    status = "EXECUTED" if decision == "ALLOW" else "PENDING_APPROVAL"
    reason = (
    "Recipient belongs to the trusted internal domain firma.ro."
    if decision == "ALLOW"
    else "Recipient is outside the trusted internal domain firma.ro. "
         "Human approval is required."
)

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO actions (id, recipient, subject, body, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (action_id, recipient, subject, body, status),
        )

    return {
        "status": status,
        "action_id": action_id,
        "decision": decision,
        "reason": reason,
        "message": (
            "Email simulated successfully."
            if status == "EXECUTED"
            else "Action held. Human approval required."
        ),
    }


def approve_action(action_id: str) -> dict:
    init_db()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE actions
            SET status = 'EXECUTED'
            WHERE id = ? AND status = 'PENDING_APPROVAL'
            """,
            (action_id,),
        )

    if cursor.rowcount != 1:
        return {
            "status": "ERROR",
            "message": "Action not found or already processed.",
        }

    return {
        "status": "EXECUTED",
        "action_id": action_id,
        "message": "Approved by human. Email simulated.",
    }


def reject_action(action_id: str) -> dict:
    init_db()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE actions
            SET status = 'REJECTED'
            WHERE id = ? AND status = 'PENDING_APPROVAL'
            """,
            (action_id,),
        )

    if cursor.rowcount != 1:
        return {
            "status": "ERROR",
            "message": "Action not found or already processed.",
        }

    return {
        "status": "REJECTED",
        "action_id": action_id,
        "message": "Action rejected. Nothing executed.",
    }


def get_actions(status: str) -> list[dict]:
    init_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, recipient, subject, body, status
            FROM actions
            WHERE status = ?
            ORDER BY created_at DESC, rowid DESC
            """,
            (status,),
        ).fetchall()

    return [dict(row) for row in rows]

def generate_action_report() -> dict:
    """Generate a summary of all recorded simulated actions."""
    statuses = ("EXECUTED", "PENDING_APPROVAL", "REJECTED")

    actions = []
    counts = {}

    for status in statuses:
        items = get_actions(status)
        counts[status] = len(items)

        for item in items:
            actions.append({
                "recipient": item["recipient"],
                "subject": item["subject"],
                "status": item["status"],
            })

    return {
        "report_type": "Action & Policy Report",
        "scope": "All recorded actions",
        "total_actions": sum(counts.values()),
        "executed": counts["EXECUTED"],
        "pending_approval": counts["PENDING_APPROVAL"],
        "rejected": counts["REJECTED"],
        "actions": actions,
        "note": "All email executions are simulated. No real emails are sent.",
    }