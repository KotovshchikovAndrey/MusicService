from email.mime.text import MIMEText

from domain.ports.driven.smtp_client import SmtpClient
from domain.ports.driving.otp_code_sending import (
    SendOTPCodeByEmailDTO,
    SendOTPCodeByEmailUseCase,
)


class SendOTPCodeByEmailUseCaseImpl(SendOTPCodeByEmailUseCase):
    _smtp_client: SmtpClient

    def __init__(self, smtp_client: SmtpClient) -> None:
        self._smtp_client = smtp_client

    async def execute(self, data: SendOTPCodeByEmailDTO) -> None:
        body = "<html><body>"
        body += f"<p><b>{data.code}</b> - Ваш код для авторизации на _____</p>"
        body += "</html></body>"

        await self._smtp_client.send_mail(
            to=[data.email],
            subject="Код подтверждения",
            body=MIMEText(body, "html", "utf-8"),
        )
