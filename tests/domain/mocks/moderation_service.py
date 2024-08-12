from io import BytesIO
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.utils.moderation import ModerationServiceAdapter


@pytest.fixture(scope="package")
def moderation_service_mock(audio_mock: BytesIO) -> ModerationServiceAdapter:
    mocked_moderation_service = MagicMock(spec=ModerationServiceAdapter)
    mocked_moderation_service.download_approved_audio = AsyncMock(
        return_value=audio_mock
    )

    return mocked_moderation_service
