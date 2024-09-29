from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable

import aiosmtplib

from domain.ports.driven.smtp_client import SmtpClient


class AioSmtpClient(SmtpClient):
    _host: str
    _port: int
    _username: str
    _password: str
    _use_tls: bool

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = False,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_tls = use_tls

    async def send_mail(self, to: Iterable[str], subject: str, body: MIMEText) -> None:
        message = MIMEMultipart()
        message["From"] = self._username
        message["To"] = ", ".join(to)
        message["Subject"] = subject
        message.attach(body)

        async with aiosmtplib.SMTP(
            hostname=self._host,
            port=self._port,
            start_tls=self._use_tls,
        ) as smtp:
            await smtp.login(self._username, self._password)
            await smtp.send_message(message, recipients=to, sender=self._username)
