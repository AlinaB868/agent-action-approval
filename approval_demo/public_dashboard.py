from html import escape

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse


DEMO_ACTIONS = [
    {"id": "demo-1", "recipient": "ana@firma.ro", "subject": "Internal project update", "status": "EXECUTED"},
    {"id": "demo-2", "recipient": "client@example.com", "subject": "External proposal", "status": "PENDING_APPROVAL"},
    {"id": "demo-3", "recipient": "team@firma.ro", "subject": "Weekly report", "status": "EXECUTED"},
    {"id": "demo-4", "recipient": "unknown@example.com", "subject": "Unapproved request", "status": "REJECTED"},
]

def get_actions(status):
    return [action for action in DEMO_ACTIONS if action["status"] == status]


app = FastAPI(title="Agent Action Approval Demo")


def render_page() -> str:
    pending_actions = get_actions("PENDING_APPROVAL")
    executed_actions = get_actions("EXECUTED")
    rejected_actions = get_actions("REJECTED")

    pending_count = len(pending_actions)
    executed_count = len(executed_actions)
    rejected_count = len(rejected_actions)
    total_count = pending_count + executed_count + rejected_count

    if total_count:
        executed_pct = executed_count / total_count * 100
        rejected_pct = rejected_count / total_count * 100
        pending_pct = pending_count / total_count * 100
    else:
        executed_pct = rejected_pct = pending_pct = 0

    pet_message = (
        "You have actions waiting for review!"
        if pending_count
        else "All clear! No actions are waiting for approval."
    )

    pending_html = ""

    for action in get_actions("PENDING_APPROVAL"):
        action_id = action["id"]
        recipient = escape(action["recipient"])
        subject = escape(action["subject"])
        safe_id = escape(action_id, quote=True)

        pending_html += f"""
        <div class="item">
            <strong>HOLD - Awaiting human approval</strong>
            <p>To: {recipient}</p>
            <p>Subject: {subject}</p>

            <form method="post" action="/demo/approve/{safe_id}">
                <button type="submit" class="approve">Approve</button>
            </form>

            <form method="post" action="/demo/reject/{safe_id}">
                <button type="submit" class="reject">Reject</button>
            </form>
        </div>
        """

    if not pending_html:
        pending_html = "<p>No pending actions.</p>"

    executed_html = "".join(
        f"<li>{escape(a['recipient'])} - {escape(a['subject'])}</li>"
        for a in get_actions("EXECUTED")
    )

    if not executed_html:
        executed_html = "<li>No executed actions.</li>"

    rejected_html = "".join(
        f"<li>{escape(a['recipient'])} - {escape(a['subject'])}</li>"
        for a in get_actions("REJECTED")
    )

    if not rejected_html:
        rejected_html = "<li>No rejected actions.</li>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Agent Action Approval Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 850px;
                margin: 40px auto;
                padding: 0 20px;
                background: #f5f7fb;
                color: #172033;
            }}
            h1 {{ color: #233876; }}
            .card {{
                background: white;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 2px 12px #00000010;
            }}
            input, textarea {{
                display: block;
                width: 100%;
                box-sizing: border-box;
                margin: 10px 0;
                padding: 12px;
            }}
            button {{
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                margin: 4px 0;
            }}
            .submit {{ background: #2846a0; color: white; }}
            .approve {{ background: #198754; color: white; }}
            .reject {{ background: #dc3545; color: white; }}
            .item {{
                border-left: 4px solid #e0a000;
                padding: 12px;
                margin: 12px 0;
                background: #fff9e8;
            }}

            .stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 24px 0;
}}

.stat-card {{
    background: #ffffff;
    border: 1px solid #e6dcf7;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 16px #7653c610;
}}

.stat-card span {{
    display: block;
    font-size: 13px;
    color: #756b87;
    margin-bottom: 10px;
}}

.stat-card strong {{
    display: block;
    font-size: 30px;
    color: #7653c6;
}}

@media (max-width: 700px) {{
    .stats {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}
.chart-card {{
    border: 1px solid #e6dcf7;
}}

.chart-description {{
    color: #756b87;
    font-size: 14px;
}}

.chart-layout {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 55px;
    flex-wrap: wrap;
    padding: 15px 0;
}}

.donut {{
    width: 180px;
    height: 180px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.donut-center {{
    width: 125px;
    height: 125px;
    border-radius: 50%;
    background: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.donut-center strong {{
    font-size: 38px;
    color: #7653c6;
}}

.donut-center span {{
    font-size: 13px;
    color: #756b87;
}}

.chart-legend p {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: #29223c;
}}

.legend-dot {{
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}

.executed-dot {{ background: #7653c6; }}
.rejected-dot {{ background: #e3a4a7; }}
.pending-dot {{ background: #e9c37a; }}

.pet-card {{
    display: flex;
    align-items: center;
    gap: 24px;
    border: 1px solid #e6dcf7;
    background: #fcfaff;
}}

.pet-avatar {{
    flex-shrink: 0;
    background: #f5f0ff;
    border-radius: 20px;
    padding: 10px;
}}

.pet-info h2 {{
    color: #7653c6;
    margin: 0 0 8px;
    font-size: 22px;
}}

.pet-info p {{
    color: #514760;
    margin: 0 0 12px;
}}

.pet-label {{
    color: #8b7aa9;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}

@media (max-width: 600px) {{
    .pet-card {{
        flex-direction: column;
        text-align: center;
    }}
}}

/* Lavender Tech â€” final visual refinements */

body {{
    background: #f7f5fc;
    color: #29223c;
    font-family: "Segoe UI", Arial, sans-serif;
}}

h1 {{
    color: #7653c6;
    font-size: 38px;
    letter-spacing: -0.8px;
}}

h2 {{
    color: #352a4b;
}}

.card {{
    border: 1px solid #e9e1f5;
    border-radius: 16px;
    box-shadow: 0 6px 22px #7653c60d;
}}

input, textarea {{
    border: 1px solid #dcd3eb;
    border-radius: 9px;
    font: inherit;
    background: #fff;
    color: #29223c;
}}

input:focus, textarea:focus {{
    outline: 2px solid #c6b4f5;
    border-color: #7653c6;
}}

button {{
    font: inherit;
    font-weight: 600;
    border-radius: 9px;
    transition: filter 0.2s ease;
}}

button:hover {{
    filter: brightness(0.92);
}}

.submit {{
    background: #7653c6;
    color: white;
}}

.approve {{
    background: #26846c;
    color: white;
}}

.reject {{
    background: #c65b70;
    color: white;
}}

.item {{
    background: #fcf9ff;
    border-left: 4px solid #b392e7;
    border-radius: 9px;
}}

label {{
    display: block;
    margin-top: 14px;
    font-weight: 600;
    color: #514760;
}}

.pet-avatar svg {{
    animation: pixel-breathe 3s ease-in-out infinite;
    transform-origin: center bottom;
}}

.pet-calm .pet-avatar svg {{
    animation: pixel-breathe 3s ease-in-out infinite;
}}

.pet-alert {{
    border-color: #e9c37a;
    background: #fffaf1;
}}

.pet-alert .pet-avatar {{
    background: #fff0d1;
}}

.pet-alert .pet-avatar svg {{
    animation: pixel-alert 0.7s ease-in-out infinite alternate;
}}

.pet-alert .pet-info h2 {{
    color: #a66b16;
}}

@keyframes pixel-breathe {{
    0%, 100% {{ transform: translateY(0) scale(1); }}
    50% {{ transform: translateY(-3px) scale(1.03); }}
}}

@keyframes pixel-alert {{
    from {{ transform: rotate(-6deg) translateY(0); }}
    to {{ transform: rotate(6deg) translateY(-5px); }}
}}

@media (prefers-reduced-motion: reduce) {{
    .pet-avatar svg,
    .pet-calm .pet-avatar svg,
    .pet-alert .pet-avatar svg {{
        animation: none;
    }}
}}

/* Lavender Tech â€” section headings */

h2 {{
    color: #7653c6;
    font-weight: 700;
}}

label {{
    color: #514760;
}}

/* Lavender Tech â€” clean electric violet */

.stat-card strong {{
    color: #6d35d4;
    font-size: 42px;
    font-weight: 800;
    -webkit-text-stroke: 0;
    text-shadow:
        0 0 2px #d9c7ff,
        0 0 6px #c6b4f580;
}}

.stat-card {{
    background: #ffffff;
    border: 1px solid #ded0fa;
}}

.stat-card:hover {{
    transform: translateY(-3px);
    border-color: #a78bfa;
    box-shadow: 0 6px 20px #7653c625;
    transition: all 0.25s ease;
}}
        
button:disabled {{
    opacity: 0.55;
    cursor: not-allowed;
}}
</style>
    </head>
    <body>
        <h1>Agent Action Approval Demo</h1>
        <p>Human-in-the-loop control for simulated agent actions.</p>

        <div class="stats">
    <div class="stat-card">
        <span>Total Actions</span>
        <strong>{total_count}</strong>
    </div>

    <div class="stat-card">
        <span>Executed</span>
        <strong>{executed_count}</strong>
    </div>

    <div class="stat-card">
        <span>Pending Review</span>
        <strong>{pending_count}</strong>
    </div>

    <div class="stat-card">
        <span>Rejected</span>
        <strong>{rejected_count}</strong>
    </div>
</div>
<div class="card chart-card">
    <h2>Action Status Distribution</h2>
    <p class="chart-description">
        Overview of all simulated agent actions.
    </p>

    <div class="chart-layout">
        <div class="donut"
             style="background: conic-gradient(
                 #7653c6 0% {executed_pct}%,
                 #e3a4a7 {executed_pct}% {executed_pct + rejected_pct}%,
                 #e9c37a {executed_pct + rejected_pct}% 100%
             );">
            <div class="donut-center">
                <strong>{total_count}</strong>
                <span>actions</span>
            </div>
        </div>

        <div class="chart-legend">
            <p><span class="legend-dot executed-dot"></span>
               Executed: {executed_count}</p>
            <p><span class="legend-dot rejected-dot"></span>
               Rejected: {rejected_count}</p>
            <p><span class="legend-dot pending-dot"></span>
               Pending: {pending_count}</p>
        </div>
    </div>
</div>
<div class="card pet-card {'pet-alert' if pending_count else 'pet-calm'}">
    <div class="pet-avatar">
        <svg viewBox="0 0 100 100" width="100" height="100"
             xmlns="http://www.w3.org/2000/svg"
             role="img" aria-label="Pixel the purple cat">
            <path d="M18 43 L15 12 L38 29 Q50 24 62 29
                     L85 12 L82 43 Q91 72 69 82
                     Q50 94 31 82 Q9 72 18 43Z"
                  fill="#c6b4f5" stroke="#7653c6"
                  stroke-width="2.5" stroke-linejoin="round"/>
            <ellipse cx="36" cy="54" rx="4" ry="6" fill="#29223c"/>
            <ellipse cx="64" cy="54" rx="4" ry="6" fill="#29223c"/>
            <path d="M47 65 Q50 69 53 65"
                  fill="none" stroke="#29223c"
                  stroke-width="2.5" stroke-linecap="round"/>
            <ellipse cx="27" cy="64" rx="8" ry="4"
                     fill="#eca8ca" opacity="0.65"/>
            <ellipse cx="73" cy="64" rx="8" ry="4"
                     fill="#eca8ca" opacity="0.65"/>
        </svg>
    </div>

    <div class="pet-info">
        <h2>Meet Pixel, your policy buddy!</h2>
        <p>{pet_message}</p>
        <span class="pet-label">AI APPROVAL ASSISTANT Â· DEMO MASCOT</span>
    </div>
</div>
        <div class="card">
            <h2>Request an action</h2>
            <form method="post" action="/request">
                <label>Recipient</label>
                <input name="recipient" required
                       placeholder="ana@firma.ro">

                <label>Subject</label>
                <input name="subject" required
                       placeholder="Test email">

                <label>Message</label>
                <textarea name="body" required></textarea>

                <button type="submit" class="submit">Request action</button>
            </form>
        </div>

        <div class="card">
            <h2>Pending approval</h2>
            {pending_html}
        </div>

        <div class="card">
            <h2>Executed simulated actions</h2>
            <ul>{executed_html}</ul>
        </div>
                <div class="card">
            <h2>Rejected actions</h2>
            <ul>{rejected_html}</ul>
        </div>
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    return render_page()




@app.post("/demo/approve/{action_id}")
def demo_approve(action_id: str):
    for action in DEMO_ACTIONS:
        if action["id"] == action_id and action["status"] == "PENDING_APPROVAL":
            action["status"] = "EXECUTED"
            break
    return RedirectResponse("/", status_code=303)


@app.post("/demo/reject/{action_id}")
def demo_reject(action_id: str):
    for action in DEMO_ACTIONS:
        if action["id"] == action_id and action["status"] == "PENDING_APPROVAL":
            action["status"] = "REJECTED"
            break
    return RedirectResponse("/", status_code=303)



@app.post("/request")
def request_action(
    recipient: str = Form(...),
    subject: str = Form(...),
    message: str = Form(""),
):
    recipient = recipient.strip()
    if not recipient:
        return RedirectResponse("/", status_code=303)

    status = "EXECUTED" if recipient.lower().endswith("@firma.ro") else "PENDING_APPROVAL"

    DEMO_ACTIONS.append({
        "id": f"demo-{len(DEMO_ACTIONS) + 1}",
        "recipient": recipient,
        "subject": subject,
        "status": status,
    })

    return RedirectResponse("/", status_code=303)
