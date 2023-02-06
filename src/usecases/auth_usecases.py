from dataclasses import dataclass
from datetime import datetime, timedelta

from src.clients.sns_client import SNSClient
from src.repositories.user_repository import UserRepository
from src.services.datetime_service import DateTimeService
from src.services.generate_code import GenerateCodeService


@dataclass
class SendCodeUseCase:
    """Usecase for sending verification code."""

    client: SNSClient
    code_service: GenerateCodeService
    datetime_service: DateTimeService
    repository: UserRepository

    async def send_code(self, phone: str):
        code = await self.code_service.generate_code()
        otp_expiration = await self.datetime_service.get_otp_expiration()

        user = await self.repository.get_user_by_phone(phone)
        if not user:
            user = await self.repository.create_user_with_otp_code(
                phone=phone,
                code=code,
                otp_expiration=otp_expiration
            )

        message = await self.code_service.get_message_with_generated_code(code)
        await self.client.send_message(phone, message)
