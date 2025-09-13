from unittest import mock
import pytest

from domain.events.event_notifier import EventNotifier
from domain.models.builders.user import UserBuilder
from domain.ports.driven.database.otp_code_repository import OTPCodeRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.database.user_repository import UserRepository
from domain.ports.driving.sign_in_process import SignInDTO
from domain.usecases.sign_in import SignInUseCaseImpl


@pytest.fixture
def mock_uow() -> UnitOfWork:
    mock_uow = mock.MagicMock(spec=UnitOfWork)
    mock_uow.__aenter__.return_value = mock_uow

    mock_uow.otp_codes = mock.MagicMock(spec=OTPCodeRepository)
    mock_uow.users = mock.MagicMock(spec=UserRepository)

    return mock_uow


async def test_sign_in_save_user_when_not_exists(mock_uow: UnitOfWork):
    # Arrange
    mock_uow.users.get_by_email.return_value = None
    mock_notifier = mock.MagicMock(spec=EventNotifier)
    usecase = SignInUseCaseImpl(uow=mock_uow, notifier=mock_notifier)
    dto = SignInDTO(email="example@gmail.com")

    # Act
    await usecase.execute(dto)

    # Assert
    mock_uow.users.save.assert_called_once()
    mock_uow.commit.assert_called_once()
    mock_notifier.notify.assert_called_once()


async def test_sign_in_not_save_user_when_exists(mock_uow: UnitOfWork):
    # Arrange
    occupied_email = "example@gmail.com"
    exists_user = UserBuilder().set_email(email=occupied_email).build()
    mock_uow.users.get_by_email.return_value = exists_user

    mock_notifier = mock.MagicMock(spec=EventNotifier)
    usecase = SignInUseCaseImpl(uow=mock_uow, notifier=mock_notifier)
    dto = SignInDTO(email=occupied_email)

    # Act
    await usecase.execute(dto)

    # Assert
    mock_uow.users.save.assert_not_called()
    mock_notifier.notify.assert_called_once()
