from dataclasses import dataclass
from datetime import datetime

from src.clients.sns_client import SNSClient
from src.repositories.user_repository import UserRepository
from src.services.datetime_service import DateTimeService
from src.services.generate_code import GenerateCodeService


@dataclass
class CodeMetaData:
    """Class that holds data that needs to be processed for sending code."""

    code: str
    message: str
    otp_expiration: datetime


@dataclass
class SendCodeUseCase:
    """Usecase for sending verification code."""

    client: SNSClient
    code_service: GenerateCodeService
    datetime_service: DateTimeService
    repository: UserRepository

    async def process_send_code(self, phone: str):
        """Usecase entrypoint for generating code, message
        and sending to user."""

        code_data = await self._get_message()
        await self._set_otp_for_user(phone, code_data)
        await self.client.send_message(phone, code_data.message)

    async def _get_message(self):
        code = await self.code_service.generate_code()
        message = await self.code_service.get_message_with_generated_code(code)

        otp_expiration = await self.datetime_service.get_otp_expiration()

        return CodeMetaData(
            code=code,
            message=message,
            otp_expiration=otp_expiration
        )

    async def _set_otp_for_user(self, phone, code_data: CodeMetaData) -> None:
        user = await self.repository.get_user_by_phone(phone)

        if not user:
            await self.repository.create_user_with_otp_code(
                phone=phone,
                code=code_data.code,
                otp_expiration=code_data.otp_expiration
            )
            return

        await self.repository.update_user_otp(
            phone=phone,
            code=code_data.code,
            otp_expiration=code_data.otp_expiration
        )
