import logging
from uuid import UUID

from domain.events.event_notifier import EventNotifier
from domain.events.events import UserSignedIn
from domain.models.builders.user import UserBuilder
from domain.models.entities.otp_code import OTPCodePurpose
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.sign_in_process import SignInDTO, SignInUseCase


class SignInUseCaseImpl(SignInUseCase):
    _uow: UnitOfWork
    _notifier: EventNotifier

    def __init__(self, uow: UnitOfWork, notifier: EventNotifier) -> None:
        self._uow = uow
        self._notifier = notifier

    async def execute(self, data: SignInDTO) -> UUID:
        async with self._uow as uow:
            user = await uow.users.get_by_email(data.email)
            if user is None:
                user = UserBuilder().set_email(email=data.email).build()
                await uow.users.save(user)

                otp_code = user.request_new_otp_code(OTPCodePurpose.VERIFY)
                await uow.otp_codes.save(otp_code)
                await uow.commit()
                logging.info("User(id=%s) created", user.id)

            else:
                otp_code = await uow.otp_codes.get_by_owner_and_purpose(
                    owner_id=user.id,
                    purpose=OTPCodePurpose.VERIFY,
                )

                if (otp_code is None) or (otp_code.is_expired):
                    otp_code = user.request_new_otp_code(OTPCodePurpose.VERIFY)
                    await uow.otp_codes.save(otp_code)
                    await uow.commit()

        await self._notifier.notify(UserSignedIn(user, otp_code))
        logging.info("User(id=%s) signed in", user.id)
        return user.id
