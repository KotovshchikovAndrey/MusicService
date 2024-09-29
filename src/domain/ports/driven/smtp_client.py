from email.mime.text import MIMEText
from typing import Iterable, Protocol


class SmtpClient(Protocol):
    async def send_mail(
        self, to: Iterable[str], subject: str, body: MIMEText
    ) -> None: ...
