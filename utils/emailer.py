import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.quiz import get_quiz


def build_html(topic, video_info, wiki_info):
    image_html = (
        f'<img src="{wiki_info["image_url"]}" style="max-width:100%;border-radius:8px;" />'
        if wiki_info and wiki_info.get("image_url")
        else ""
    )
    summary_html = (
        f'<p style="font-size:15px;line-height:1.5;">{wiki_info["summary"]}</p>'
        if wiki_info and wiki_info.get("summary")
        else "<p>No summary available today -- check the links below.</p>"
    )
    wiki_link_html = (
        f'<p><a href="{wiki_info["wiki_url"]}">Read more on Wikipedia &rarr;</a></p>'
        if wiki_info and wiki_info.get("wiki_url")
        else ""
    )
    video_html = (
        f'<p>🎥 <a href="{video_info["url"]}"><b>{video_info["title"]}</b></a></p>'
        if video_info
        else ""
    )
    quiz = get_quiz(topic)
    options_html = "".join(
        f'<li><b>{letter}.</b> {escape(option)}</li>'
        for letter, option in zip("ABCD", quiz["options"])
    )
    quiz_html = f"""
        <div style="margin-top:20px;padding:15px;background:#f5f7fa;border-left:4px solid #667eea;">
          <h3>🧠 Quick MCQ</h3>
          <p><b>{escape(quiz["question"])}</b></p>
          <ol style="line-height:1.8;">{options_html}</ol>
          <p style="margin-bottom:0;"><b>Answer:</b> {quiz["answer"]} - {escape(quiz["explanation"])}</p>
        </div>
    """

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width:600px; margin:auto;">
        <h2 style="color:#1a1a1a;">🩺 Today's topic: {topic['name']}</h2>
        <p style="color:#888; margin-top:-10px;">{topic['category']}</p>
        {image_html}
        {summary_html}
        {video_html}
        {quiz_html}
        {wiki_link_html}
        <hr>
        <p style="font-size:12px;color:#aaa;">Sent by your daily disease-a-day app.</p>
      </body>
    </html>
    """


def send_email(smtp_host, smtp_port, smtp_user, smtp_pass, to_email, topic, video_info, wiki_info):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🩺 Today's disease: {topic['name']}"
    msg["From"] = smtp_user
    msg["To"] = to_email

    html = build_html(topic, video_info, wiki_info)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
