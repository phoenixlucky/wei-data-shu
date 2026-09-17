"""Mail reporting utilities."""

from __future__ import annotations

import datetime
import logging
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Sequence

logger = logging.getLogger(__name__)


class MailError(RuntimeError):
    """Raised when an email operation fails."""


class DailyEmailReport:
    """SMTP/SSL email reporter with plain-text / HTML body and attachments."""

    def __init__(
        self,
        email_host: str,
        email_port: int,
        email_username: str,
        email_password: str,
    ) -> None:
        self.email_host = email_host
        self.email_port = email_port
        self.email_username = email_username
        self.email_password = email_password
        self.receivers: list[str] = []
        self.msg = MIMEMultipart()

    def add_receiver(self, receiver_email: str) -> None:
        self.receivers.append(receiver_email)

    def set_email_content(
        self,
        subject: str,
        body: str,
        file_paths: Sequence[str | Path] | None = None,
        file_names: Sequence[str] | None = None,
        is_html: bool = False,
    ) -> None:
        """Compose the message body and optional attachments."""
        if body is None:
            raise ValueError("邮件正文不能为空")
        self.msg["From"] = self.email_username
        self.msg["To"] = ", ".join(self.receivers)
        self.msg["Subject"] = subject

        if is_html:
            self.msg.attach(MIMEText(body, "html", "utf-8"))
        else:
            self.msg.attach(MIMEText(body, "plain", "utf-8"))

        if file_paths and file_names:
            if len(file_paths) != len(file_names):
                raise ValueError("file_paths 与 file_names 长度必须一致")
            for file_path, file_name in zip(file_paths, file_names):
                path = Path(file_path) / file_name
                if not path.is_file():
                    raise FileNotFoundError(f"附件不存在: {path}")
                with path.open("rb") as handle:
                    attachment = MIMEApplication(handle.read())
                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=("utf-8", "", file_name),
                )
                self.msg.attach(attachment)

    def send_email(self) -> None:
        """Send the composed message. Raises :class:`MailError` on failure."""
        if not self.receivers:
            raise MailError("没有收件人，请先调用 add_receiver()")
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(self.email_host, self.email_port, context=context) as server:
                server.login(self.email_username, self.email_password)
                server.sendmail(self.email_username, self.receivers, self.msg.as_string())
        except (smtplib.SMTPException, OSError) as err:
            raise MailError(f"邮件发送失败: {err}") from err
        logger.info("邮件发送成功（收件人: %s）", ", ".join(self.receivers))

    def send_daily_report(
        self,
        title: str,
        text: str | None = None,
        is_html: bool = False,
        html_content: str | None = None,
    ) -> None:
        """Send a daily report with today's date in the subject line."""
        subject = f"{title} - {datetime.date.today()}"
        body: str
        if html_content is not None:
            body = html_content
            is_html = True
        elif text is not None:
            body = text
        else:
            raise ValueError("send_daily_report 需要 text 或 html_content 之一")
        self.set_email_content(subject, body, is_html=is_html)
        self.send_email()


__all__ = ["DailyEmailReport", "MailError"]
