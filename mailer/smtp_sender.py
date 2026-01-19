import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config.email_config import (
    SMTP_SERVER, SMTP_PORT,
    EMAIL_ADDRESS, EMAIL_PASSWORD, FROM_NAME
)

def send_email(to_emails, subject, html_content, inline_images: list = None):
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    msg = MIMEMultipart("related")
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    msg["From"] = f"{FROM_NAME} <{EMAIL_ADDRESS}>"
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    msg_alternative.attach(MIMEText(html_content, "html"))

    inline_images = inline_images or []
    for img_path in inline_images:
        if not img_path or not os.path.exists(img_path):
            continue
        with open(img_path, "rb") as f:
            img_data = f.read()
        mime_img = MIMEImage(img_data)
        cid = os.path.splitext(os.path.basename(img_path))[0]
        mime_img.add_header("Content-ID", f"<{cid}>")
        mime_img.add_header("Content-Disposition", "inline", filename=os.path.basename(img_path))
        msg.attach(mime_img)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)