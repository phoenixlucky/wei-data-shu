"""Mail reporting utilities."""

from __future__ import annotations

import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class DailyEmailReport:
    def __init__(self, email_host, email_port, email_username, email_password):
        self.email_host = email_host
        self.email_port = email_port
        self.email_username = email_username
        self.email_password = email_password
        self.receivers = []
        self.msg = MIMEMultipart()

    def add_receiver(self, receiver_email):
        self.receivers.append(receiver_email)

    def set_email_content(self, subject, body, file_paths=None, file_names=None, is_html=False):
        self.msg["From"] = self.email_username
        self.msg["To"] = ", ".join(self.receivers)
        self.msg["Subject"] = subject

        if is_html:
            self.msg.attach(MIMEText(body, "html", "utf-8"))
        else:
            self.msg.attach(MIMEText(body, "plain"))

        if file_paths and file_names:
            for file_path, file_name in zip(file_paths, file_names):
                with open(file_path + file_name, "rb") as handle:
                    att1 = MIMEText(handle.read(), "base64", "utf-8")
                att1["Content-Type"] = "application/octet-stream"
                att1.add_header("Content-Disposition", "attachment", filename=("gbk", "", file_name))
                self.msg.attach(att1)

    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.email_host, self.email_port, context=context) as server:
            server.login(self.email_username, self.email_password)
            server.sendmail(self.email_username, self.receivers, self.msg.as_string())
            print("邮件发送成功！")

    def send_daily_report(self, title, text=None, is_html=False, html_content=None):
        subject = f"{title} - {datetime.date.today()}"
        if html_content is not None:
            body = html_content
            is_html = True
        else:
            body = text
        self.set_email_content(subject, body, is_html=is_html)
        self.send_email()


__all__ = ["DailyEmailReport"]
