from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Agent Action Approval - Public Demo")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Agent Action Approval | Public Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f0ff;
                color: #48346d;
                max-width: 850px;
                margin: 50px auto;
                padding: 20px;
            }
            h1 { color: #7653c6; }
            .card {
                background: white;
                border-radius: 16px;
                padding: 22px;
                margin: 18px 0;
                box-shadow: 0 5px 18px #7653c61c;
            }
            .stats {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }
            .stats .card {
                flex: 1;
                min-width: 120px;
                text-align: center;
            }
            strong { color: #7653c6; }
            .note { color: #755f92; }
        </style>
    </head>
    <body>
        <h1>Agent Action Approval</h1>
        <p>Human-in-the-Loop AI Agent | Public Portfolio Demo</p>

        <div class="card">
            <h2>Meet Pixel 🐱</h2>
            <p>AI proposes. Policy checks. Humans approve.</p>
            <p class="note">Read-only demonstration with sample data.</p>
        </div>

        <div class="stats">
            <div class="card"><strong>8</strong><p>Total</p></div>
            <div class="card"><strong>4</strong><p>Executed</p></div>
            <div class="card"><strong>1</strong><p>Pending</p></div>
            <div class="card"><strong>3</strong><p>Rejected</p></div>
        </div>

        <div class="card">
            <h2>Approval policy</h2>
            <p><strong>ALLOW:</strong> Internal recipients (@firma.ro).</p>
            <p><strong>HOLD:</strong> External recipients require human review.</p>
            <p><strong>REJECT:</strong> Only a human can reject a pending action.</p>
        </div>

        <div class="card">
            <h2>Example pending action</h2>
            <p>To: demo@example.com</p>
            <p>Subject: Portfolio demonstration</p>
            <p><strong>Status: PENDING_APPROVAL</strong></p>
            <p class="note">Approval controls are disabled in the public demo.</p>
        </div>

        <p class="note">All email actions are simulated. No real emails are sent.</p>
    </body>
    </html>
    """
