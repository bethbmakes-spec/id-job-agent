import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import date

from config import EMAIL_TO, EMAIL_SUBJECT_PREFIX


def rows_to_html(rows):
    if not rows:
        return "<p>No new qualifying postings found this run.</p>"
    html = ["<table border='1' cellpadding='6' cellspacing='0'>",
            "<tr><th>Score</th><th>Title</th><th>Source</th><th>Remote</th><th>Salary</th>"
            "<th>Bonus?</th><th>Reputation</th><th>Link</th></tr>"]
    for r in rows:
        sal = r.get("salary_range_detected")
        sal_str = f"${sal[0]:,}\u2013${sal[1]:,}" if sal else "Not stated (verify manually)"
        rep_flag = r.get("reputation_flag", False)
        rep_notes = r.get("reputation_notes", "not checked")
        rep_cell = (f"<span style='color:red;font-weight:bold'>\u26a0 FLAGGED</span><br><small>{rep_notes}</small>"
                    if rep_flag else f"<span style='color:green'>OK</span><br><small>{rep_notes}</small>")
        row_style = " style='background-color:#fff3f3'" if rep_flag else ""
        html.append(
            f"<tr{row_style}><td>{r['score']}</td><td>{r['title']}</td><td>{r['source']}</td>"
            f"<td>{'Yes' if r['remote'] else 'No'}</td><td>{sal_str}</td>"
            f"<td>{'Yes' if r['bonus_mentioned'] else 'Unclear'}</td>"
            f"<td>{rep_cell}</td>"
            f"<td><a href='{r['url']}'>Open</a></td></tr>"
        )
    html.append("</table>")
    html.append("<p style='font-size:12px;color:#666'>\u26a0 Reputation flag = red-flag language "
                "(toxic culture, high turnover, understaffed marketing/design teams, etc.) found in "
                "public review snippets. Always confirm on Glassdoor directly before ruling a company out.</p>")
    return "\n".join(html)


def send_digest(rows, csv_path):
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print("[warn] SMTP_USER / SMTP_PASS not set -- skipping email send.")
        return

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"{EMAIL_SUBJECT_PREFIX} {date.today().isoformat()} \u2014 {len(rows)} matches"
    msg["From"] = smtp_user
    msg["To"] = EMAIL_TO

    msg.attach(MIMEText(rows_to_html(rows), "html"))

    with open(csv_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(csv_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(csv_path)}"'
        msg.attach(part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print(f"Digest emailed to {EMAIL_TO}")
