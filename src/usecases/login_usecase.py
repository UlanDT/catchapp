from dataclasses import dataclass
from datetime import datetime

import pytz

from src.db import UserDB
from src.exceptions.login_exceptions import OtpVerificationException
from src.exceptions.user_exceptions import UserNotFoundException
from src.repositories.user_repository import UserRepository
from src.services.datetime_service import DateTimeService
from src.services.token_service import AuthTokenService


@dataclass
class LogInUsecase:
    """Usecase that implements login logic."""

    repository: UserRepository
    datetime_service: DateTimeService
    token_service: AuthTokenService

    async def process_login(self, phone: str, code: str):
        user = await self.repository.get_user_otp_by_phone(phone)

        if not user:
            raise UserNotFoundException(message=f'User with phone {phone} not found')
        if not await self._user_otp_passed(code, user.otp_code, user.otp_expiration):
            await self.repository.update_user_status(
                phone, UserDB.StatusChoices.code_incorrect)
            raise OtpVerificationException(message='Code incorrect or inactive')

        await self.repository.update_user_status(phone, UserDB.StatusChoices.code_correct)
        return await self._generate_tokens(user.id)

    async def _generate_tokens(self, user_id: int):
        return self.token_service.get_tokens(user_id)

    async def _user_otp_passed(
            self,
            code: str,
            user_otp_code: str,
            otp_expiration: datetime
    ) -> bool:
        otp_is_active = await self.datetime_service.otp_active(
            datetime.now(tz=pytz.utc), otp_expiration
        )

        if user_otp_code == code and otp_is_active:
            return True

        return False
