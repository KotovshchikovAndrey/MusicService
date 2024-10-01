from domain.errors.otp_code import InvalidOTPCodeError
from domain.errors.user import UserNotFoundError
from domain.models.entities.otp_code import OTPCodePurpose
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.user_verification import (
    JwtPair,
    VerifyUserDTO,
    VerifyUserUseCase,
)
from domain.usecases.mixins.jwt_encoder import JwtEncoderMixin


class VerifyUserUseCaseImpl(JwtEncoderMixin, VerifyUserUseCase):
    _uow: UnitOfWork
    _access_token_secret: str
    _refresh_token_secret: str

    def __init__(
        self,
        uow: UnitOfWork,
        access_token_secret: str,
        refresh_token_secret: str,
    ) -> None:
        self._uow = uow
        self._access_token_secret = access_token_secret
        self._refresh_token_secret = refresh_token_secret

    async def execute(self, data: VerifyUserDTO) -> JwtPair:
        async with self._uow as uow:
            user = await uow.users.get_by_email(data.email)
            if user is None:
                raise UserNotFoundError()

            requested_otp_code = await uow.otp_codes.get_by_owner_and_purpose(
                owner_id=user.id,
                purpose=OTPCodePurpose.VERIFY,
            )

            if requested_otp_code is None:
                raise InvalidOTPCodeError()

            requested_otp_code.check(data.otp_code)
            await uow.otp_codes.remove_by_id(requested_otp_code.id)

            if not user.is_active:
                user.is_active = True
                await uow.users.save(user)

            access_token, refresh_token = user.issue_token_pair(data.device_id)
            await uow.tokens.save(refresh_token)
            await uow.commit()

        return self._encode_jwt_pair(access_token, refresh_token)
