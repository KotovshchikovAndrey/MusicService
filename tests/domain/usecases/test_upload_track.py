from io import BytesIO
from unittest.mock import patch
from uuid import uuid4

import pytest

from domain.common.exceptions import BadRequestException
from domain.dtos.inputs import UploadTrackDto
from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.repositories.album import AlbumRepository
from domain.repositories.artist import ArtistRepository
from domain.usecases.upload_track import UploadTrackUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork


class TestUploadTrackUseCase:
    @pytest.fixture(scope="class")
    def usecase(
        self,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        moderation_service_mock: ModerationServiceAdapter,
    ) -> UploadTrackUseCase:
        return UploadTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            moderation_service=moderation_service_mock,
        )

    @pytest.fixture(scope="class")
    def input_dict(self, artist_mock: Artist, album_mock: Album) -> dict:
        return dict(
            title="Mr.Kitty - After Dark",
            audio_filename="/audio.mp3",
            duration=100,
            album_id=album_mock.id,
            artist_ids={artist_mock.id},
        )

    async def test_upload_track_success(
        self,
        usecase: UploadTrackUseCase,
        input_dict: dict,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        track_mock: Track,
        artist_mock: Artist,
        audio_mock: BytesIO,
    ) -> None:
        data = UploadTrackDto(**input_dict)
        with patch("domain.factories.track.TrackFactory.create") as mocker:
            mocker.return_value = track_mock
            track_id = await usecase.execute(data=data)

            assert track_id == track_mock.id
            uow_mock.tracks.upsert.assert_called_with(track_mock)
            blob_storage_mock.put.assert_called_with(
                blob_url=track_mock.audio_url.value,
                blob=audio_mock,
            )

            uow_mock.tracks.set_artists.assert_called_with(
                track_id=track_mock.id,
                artist_ids=(artist_mock.id,),
            )

    async def test_upload_track_when_invalid_artist_ids(
        self,
        input_dict: dict,
        usecase: UploadTrackUseCase,
        artist_mock: Artist,
        artist_repository_mock: ArtistRepository,
    ) -> None:
        artist_repository_mock.filter_by_ids.return_value = []
        with pytest.raises(BadRequestException):
            input_dict["artist_ids"] = set()
            UploadTrackDto(**input_dict)

        artist_repository_mock.filter_by_ids.return_value = []
        with pytest.raises(BadRequestException):
            input_dict["artist_ids"] = (uuid4(),)
            data = UploadTrackDto(**input_dict)
            await usecase.execute(data=data)

        artist_repository_mock.filter_by_ids.return_value = [artist_mock]
        with pytest.raises(BadRequestException):
            input_dict["artist_ids"] = {artist_mock.id, uuid4()}
            data = UploadTrackDto(**input_dict)
            await usecase.execute(data=data)

    async def test_upload_track_when_album_not_found(
        self,
        input_dict: dict,
        usecase: UploadTrackUseCase,
        album_repository_mock: AlbumRepository,
    ) -> None:
        album_repository_mock.get_by_id.return_value = None
        with pytest.raises(BadRequestException):
            input_dict["album_id"] = uuid4()
            data = UploadTrackDto(**input_dict)
            await usecase.execute(data)
