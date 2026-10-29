# Agent Action Approval

A simple Human-in-the-Loop (HITL) demonstration built with Google Agent Development Kit (ADK), Python, FastAPI, and SQLite.

## Overview

This project demonstrates how an AI agent can request an action while a separate approval engine determines whether the action can proceed automatically or requires human intervention.

The example action is preparing an email. **No real emails are sent.** All executions are simulated.

## How it works

1. A user asks the Google ADK agent to prepare an email.
2. The agent calls the `request_email_action` tool.
3. The approval engine evaluates the recipient:
   - **ALLOW:** recipients in the trusted `firma.ro` domain are marked `EXECUTED` (simulated).
   - **HOLD:** external recipients are marked `PENDING_APPROVAL`.
4. Pending requests are displayed in a separate FastAPI web interface.
5. A human can approve or reject a pending request.
6. The action status is stored in SQLite.

The agent cannot approve or reject its own requests.

## Architecture

```text
User
  |
  v
Google ADK Agent
  |
  v
request_email_action
  |
  v
Approval Engine
  |
  +-- ALLOW --> EXECUTED (simulated)
  |
  +-- HOLD --> PENDING_APPROVAL
                    |
                    v
              Human Review UI
                    |
              +-----+-----+
              |           |
           Approve      Reject
              |           |
              v           v
           EXECUTED     REJECTED
          (simulated)
```

## Technologies

- Python 3.12
- Google ADK 2.13.0
- Gemini
- FastAPI
- SQLite
- pytest

## Run locally

From the project root, activate the Python virtual environment.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
python -m pip install -r requirements.txt
```

Start the Google ADK development interface:

```powershell
adk web
```

Open:

http://127.0.0.1:8000

In a second terminal, start the human approval interface:

```powershell
python -m uvicorn approval_demo.web_app:app --host 127.0.0.1 --port 8080
```

Open:

http://127.0.0.1:8080

A valid Gemini API configuration is required to use the ADK agent.

## Example scenarios

### Internal recipient

Recipient: `coleg@firma.ro`

Expected result: `ALLOW` and `EXECUTED` (simulated).

### External recipient

Recipient: `client@exemplu.ro`

Expected result: `HOLD` and `PENDING_APPROVAL`.

A human can then select **Approve** or **Reject** in the approval interface.

## Automated tests

Run:

```powershell
python -m pytest test_approval.py -v
```

The project includes six automated tests covering allowed actions, held requests, approvals, rejections, and invalid repeated decisions.

## Important limitations

- Email execution is simulated; there is no email delivery integration.
- The approval web interface does not currently implement authentication or authorization.
- SQLite is used for local demonstration.
- The project is intended for local educational use, not public production deployment.
- Gemini API requests may occasionally fail with temporary service errors such as HTTP 503.

## Project goal

Demonstrate a clear separation between an AI agent proposing an action, a deterministic approval engine applying rules, and a human making the final decision when required.

## Approval Policy and Human Oversight

The project uses a deterministic approval policy implemented in Python, independently of the language model.

| Condition                       | Decision  | Result                                   |
| ------------------------------- | --------- | ---------------------------------------- |
| Recipient belongs to `firma.ro` | `ALLOW`   | Action marked `EXECUTED` (simulated)     |
| Recipient is outside `firma.ro` | `HOLD`    | Action marked `PENDING_APPROVAL`         |
| Human approves a pending action | `APPROVE` | Status changes to `EXECUTED` (simulated) |
| Human rejects a pending action  | `REJECT`  | Status changes to `REJECTED`             |

The agent can request an action but cannot approve or reject it. Human decisions are made through a separate FastAPI interface.

The interface displays pending, executed, and rejected actions. SQLite stores their current status.

**Security limitations:** The approval interface does not implement user authentication or authorization. It is intended for local educational demonstration only and must not be exposed publicly without additional security controls.

No real emails are sent.

## Action & Policy Report

The Google ADK agent provides a `generate_action_report` tool that reads recorded actions from SQLite and returns an Action & Policy Report.

The report includes:
- Total number of recorded actions.
- Counts of simulated executed, pending approval, and rejected actions.
- A list of recorded actions with recipient, subject, and status.
- A reminder that no real emails are sent.

The agent can call `request_email_action` and `generate_action_report` within the same conversation. A report generated immediately after an external email request includes the new action as `PENDING_APPROVAL`.

Reports are generated on demand, not automatically on a daily or weekly schedule.

## Lavender Tech Dashboard

The local FastAPI review interface uses a Lavender Tech visual theme.

It includes:
- Live statistics calculated from SQLite.
- A donut chart showing action status distribution.
- Pixel, an animated purple cat mascot that reacts to pending approvals.
- Human Approve and Reject controls.
- Lists of pending, executed, and rejected actions.

The dashboard reflects the current database state whenever the page is loaded or refreshed.

