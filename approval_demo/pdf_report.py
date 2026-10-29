from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether
)

PURPLE = colors.HexColor("#7651CC")
LAVENDER = colors.HexColor("#F4F0FC")
DARK = colors.HexColor("#29233D")
GREEN = colors.HexColor("#25856F")
RED = colors.HexColor("#C85770")
GOLD = colors.HexColor("#B47A22")


def create_report(actions):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=38,
        leftMargin=38,
        topMargin=42,
        bottomMargin=42,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=24,
        textColor=PURPLE,
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="ReportHeading",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=17,
        textColor=PURPLE,
        spaceBefore=17,
        spaceAfter=9,
    ))
    styles.add(ParagraphStyle(
        name="ReportBody",
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=DARK,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="ReportCell",
        fontName="Helvetica",
        fontSize=7.5,
        leading=11,
        textColor=DARK,
    ))

    story = []

    story.append(Paragraph(
        "Agent Action Approval<br/>Action &amp; Policy Report",
        styles["ReportTitle"]
    ))
    story.append(Paragraph(
        "PIXEL - YOUR POLICY BUDDY  |  HUMAN-IN-THE-LOOP DEMO",
        styles["ReportBody"]
    ))
    story.append(Paragraph(
        "Generated: " + datetime.now().strftime("%d %B %Y, %H:%M"),
        styles["ReportBody"]
    ))

    story.append(Paragraph("Executive Summary", styles["ReportHeading"]))
    story.append(Paragraph(
        "This report presents the results of a simulated AI agent action "
        "approval workflow. The system applies a trusted-domain policy and "
        "requires human authorization for actions outside the approved domain. "
        "Its purpose is to demonstrate accountability, oversight and controlled "
        "execution of agent-initiated requests.",
        styles["ReportBody"]
    ))

    executed = sum(a["status"] == "EXECUTED" for a in actions)
    pending = sum(a["status"] == "PENDING_APPROVAL" for a in actions)
    rejected = sum(a["status"] == "REJECTED" for a in actions)

    story.append(Paragraph("Action Overview", styles["ReportHeading"]))

    metrics = Table([
        ["TOTAL ACTIONS", "EXECUTED", "PENDING REVIEW", "REJECTED"],
        [str(len(actions)), str(executed), str(pending), str(rejected)],
    ], colWidths=[125, 125, 125, 125])

    metrics.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LAVENDER),
        ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 1), (-1, 1), PURPLE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, 1), 19),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(metrics)

    story.append(Paragraph("Action &amp; Decision Log", styles["ReportHeading"]))

    def decision_reason(action):
        if action.get("decision_reason"):
            return action["decision_reason"]

        status = action["status"]
        recipient = action.get("recipient", "")

        if status == "PENDING_APPROVAL":
            return "External recipient; human approval required."

        if status == "EXECUTED" and recipient.lower().endswith("@firma.ro"):
            return "Trusted internal domain; automatically permitted."

        if status == "EXECUTED":
            return "Authorized in simulation; approval history not recorded."

        if status == "REJECTED":
            return "Rejected in simulation; detailed reason not recorded."

        return "Decision information unavailable."

    rows = [["Recipient", "Subject", "Status", "Decision reason"]]

    for action in actions:
        rows.append([
            Paragraph(str(action.get("recipient", "")), styles["ReportCell"]),
            Paragraph(str(action.get("subject", "")), styles["ReportCell"]),
            Paragraph(str(action.get("status", "")), styles["ReportCell"]),
            Paragraph(decision_reason(action), styles["ReportCell"]),
        ])

    table = Table(
        rows,
        colWidths=[113, 112, 94, 181],
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white, LAVENDER
        ]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, PURPLE),
    ]))
    story.append(table)

    story.append(Paragraph("Policy &amp; Human Oversight", styles["ReportHeading"]))

    story.append(Paragraph(
        "<b>Executed:</b> The action was permitted under the trusted-domain "
        "policy or approved by a human reviewer. Execution refers exclusively "
        "to the simulated workflow.",
        styles["ReportBody"]
    ))
    story.append(Paragraph(
        "<b>Pending approval:</b> The action is held because the recipient "
        "falls outside the trusted domain. No simulated execution occurs "
        "until a reviewer approves it.",
        styles["ReportBody"]
    ))
    story.append(Paragraph(
        "<b>Rejected:</b> A human reviewer declined the action. The workflow "
        "blocks its simulated execution.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("Conclusion", styles["ReportHeading"]))
    story.append(Paragraph(
        "The demonstrated workflow illustrates how automated policy checks "
        "and human oversight can work together to reduce unauthorized agent "
        "actions. Requests outside the trusted domain are held for review, "
        "while reviewer decisions remain visible in the action log. "
        "This report documents a demonstration environment, not a production "
        "security audit.",
        styles["ReportBody"]
    ))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>SIMULATION ONLY - NO REAL EMAILS WERE SENT.</b>",
        styles["ReportBody"]
    ))


    def draw_pixel(pdf, document):
        from reportlab.graphics import renderPDF
        from reportlab.graphics.shapes import Drawing
        from svglib.svglib import svg2rlg
        from io import BytesIO

        svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <path d="M18 43 L15 12 L38 29 Q50 24 62 29 L85 12 L82 43 Q91 72 69 82 Q50 94 31 82 Q9 72 18 43Z" fill="#c6b4f5" stroke="#7653c6" stroke-width="2.5" stroke-linejoin="round"/>
        <ellipse cx="36" cy="54" rx="4" ry="6" fill="#29223c"/>
        <ellipse cx="64" cy="54" rx="4" ry="6" fill="#29223c"/>
        <path d="M47 65 Q50 69 53 65" fill="none" stroke="#29223c" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="27" cy="64" rx="8" ry="4" fill="#eca8ca" opacity="0.65"/>
        <ellipse cx="73" cy="64" rx="8" ry="4" fill="#eca8ca" opacity="0.65"/>
        </svg>'''

        drawing = svg2rlg(BytesIO(svg.encode("utf-8")))
        renderPDF.draw(drawing, pdf, A4[0] - 115, A4[1] - 75)
        return

    def draw_pixel_old(pdf, document):
        pdf.saveState()
        x = A4[0] - 75
        y = A4[1] - 65

        # Cat ears
        pdf.setFillColor(PURPLE)
        ears = pdf.beginPath()
        ears.moveTo(x - 22, y + 12)
        ears.lineTo(x - 17, y + 38)
        ears.lineTo(x - 5, y + 23)
        ears.lineTo(x + 5, y + 23)
        ears.lineTo(x + 17, y + 38)
        ears.lineTo(x + 22, y + 12)
        ears.close()
        pdf.drawPath(ears, fill=1, stroke=0)

        # Cat face
        pdf.setFillColor(LAVENDER)
        pdf.setStrokeColor(PURPLE)
        pdf.setLineWidth(2)
        pdf.circle(x, y + 10, 23, fill=1, stroke=1)

        # Eyes
        pdf.setFillColor(DARK)
        pdf.circle(x - 9, y + 13, 2.5, fill=1, stroke=0)
        pdf.circle(x + 9, y + 13, 2.5, fill=1, stroke=0)

        # Nose
        pdf.setFillColor(RED)
        pdf.circle(x, y + 5, 2.5, fill=1, stroke=0)

        # Whiskers
        pdf.setStrokeColor(PURPLE)
        pdf.setLineWidth(1)
        for side in (-1, 1):
            pdf.line(x + side * 8, y + 4, x + side * 29, y + 8)
            pdf.line(x + side * 8, y, x + side * 29, y - 3)

        pdf.restoreState()

    def footer(canvas, document):
        draw_pixel(canvas, document)

        canvas.saveState()
        canvas.setStrokeColor(PURPLE)
        canvas.line(38, 31, A4[0] - 38, 31)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(DARK)
        canvas.drawString(38, 19, "Agent Action Approval | Demo Report")
        canvas.drawRightString(
            A4[0] - 38, 19, f"Page {document.page}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer

