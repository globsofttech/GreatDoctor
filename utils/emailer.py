import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def build_html(topic, video_info, wiki_info, nav_info=None, ipos=None):
    video_html = (
        f'<p>🎥 <a href="{video_info["url"]}"><b>{video_info["title"]}</b></a></p>'
        if video_info
        else ""
    )
    nav_html = (
        f"""
        <div style="margin-top:20px;padding:15px;background:#eef8f1;border-left:4px solid #1ab24f;">
          <h3 style="margin-top:0;">NIBL Sahabhagita Fund NAV</h3>
          <p style="margin:0 0 8px;"><b>NAV Value:</b> {escape(str(nav_info["value"]))}</p>
          <p style="margin:0 0 8px;"><b>Date:</b> {escape(str(nav_info["date"]))}</p>
          <p style="margin-bottom:0;"><a href="{escape(nav_info["source_url"])}">View latest NAV</a></p>
        </div>
        """
        if nav_info
        else ""
    )
    ipo_html = (
        """
        <div style="margin-top:20px;padding:15px;background:#f4f0ff;border-left:4px solid #7654c7;">
          <h3 style="margin-top:0;">Upcoming IPOs</h3>
          <ul style="padding-left:20px;line-height:1.6;">
        """
        + "".join(
            f'<li><b>{escape(str(ipo["company"]))}</b> - '
            f'{escape(str(ipo["countdown"]))} '
            f'(opens {escape(str(ipo["opening_date"]))}, '
            f'closes {escape(str(ipo["closing_date"]))})</li>'
            for ipo in ipos
        )
        + f"""
          </ul>
          <p style="margin-bottom:0;"><a href="{escape(ipos[0]["source_url"])}">View all IPO details</a></p>
        </div>
        """
        if ipos
        else ""
    )

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width:600px; margin:auto;">
        <h2 style="color:#1a1a1a;">🩺 Today's topic: {topic['name']}</h2>
        <p style="color:#888; margin-top:-10px;">{topic['category']}</p>
        {video_html}
        {nav_html}
        {ipo_html}
        <hr>
        <p style="font-size:12px;color:#aaa;">Sent by your daily disease-a-day app.</p>
      </body>
    </html>
    """


def send_email(
    smtp_host,
    smtp_port,
    smtp_user,
    smtp_pass,
    to_email,
    topic,
    video_info,
    wiki_info,
    nav_info=None,
    ipos=None,
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🩺 Today's disease: {topic['name']}"
    msg["From"] = smtp_user
    msg["To"] = to_email

    html = build_html(topic, video_info, wiki_info, nav_info, ipos)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
