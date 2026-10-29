from google.adk.agents import Agent

from approval_demo.approval_engine import request_email, generate_action_report


def request_email_action(
    recipient: str,
    subject: str,
    body: str,
) -> dict:
    """Request a simulated email action through the approval gateway.

    Args:
        recipient: Destination email address.
        subject: Email subject.
        body: Email message content.

    Returns:
        The execution or pending-approval status.
    """
    return request_email(
        recipient=recipient,
        subject=subject,
        body=body,
    )


root_agent = Agent(
    name="approval_demo",
    model="gemini-3.8-flash",
    description="AI agent demonstrating human approval for sensitive actions.",
    instruction=(
        "You are an assistant for a simulated email workflow. "
        "When the user asks to prepare or send an email, "
        "call request_email_action with the recipient, subject and body. "
        "If the subject or body is missing, use short demo placeholders. "
        "Never claim that a real email was sent. "
        "When the user asks for an action report, summary, or policy report, "
        "call generate_action_report and present the actual database results. "
        "Explain that EXECUTED means simulated execution, not a real email. "
        "Do not invent counts or actions. "
        "If the tool returns PENDING_APPROVAL, explain that the action "
        "is paused until a human approves it. "
        "If the tool returns a decision and reason, "
        "explain both clearly to the user. "
        "You cannot approve or reject actions yourself. "
        "Do not claim that a pending action was executed."
    ),
    tools=[request_email_action, generate_action_report],
)