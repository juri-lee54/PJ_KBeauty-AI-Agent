from newsletter.builder import build_newsletter
from mailer.smtp_sender import send_email
import os

if __name__ == "__main__":
    email_html, preview_path, logo_file = build_newsletter()

    recipients = os.getenv("REPORT_RECIPIENTS", "example@company.com")
    to_list = [e.strip() for e in recipients.split(",") if e.strip()]

    inline_imgs = [logo_file] if logo_file else []
    send_email(
        to_emails=to_list,
        subject="📬 주간 에이전트 분석 리포트",
        html_content=email_html,
        inline_images=inline_imgs
    )