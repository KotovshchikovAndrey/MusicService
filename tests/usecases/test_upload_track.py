from io import BytesIO

import pytest

from domain.dtos.track import UploadTrackDto
from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.exceptions.bad_request import BadRequestException
from domain.usecases.upload_track import UploadTrackUseCase
from domain.utils.blob import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork


class TestUploadTrackUseCase:
    @pytest.fixture
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

    @pytest.fixture
    def input_dict(self, artist_mock: Artist, album_mock: Album) -> dict:
        return dict(
            title="Mr.Kitty - After Dark",
            audio_filename="/audio.mp3",
            duration=100,
            album_oid=album_mock.oid.value,
            artist_oids=(artist_mock.oid.value,),
        )

    async def test_upload_track_success(
        self,
        audio_mock: BytesIO,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        usecase: UploadTrackUseCase,
        input_dict: dict,
    ) -> None:
        data = UploadTrackDto(**input_dict)
        track_oid = await usecase.execute(data=data)
        track = await uow_mock.tracks.get_by_oid(track_oid)

        assert track is not None
        assert track.oid.value == track_oid
        assert track.title.value == data.title
        assert track.album_oid.value == data.album_oid
        assert track.duration.value == data.duration
        assert data.artist_oids == tuple(artist.oid.value for artist in track.artists)

        audio = blob_storage_mock.read(blob_url=track.audio_url.value, chunk_size=1024)
        buffer = BytesIO()
        async for byte in audio:
            buffer.write(byte)

        assert buffer.getvalue() == audio_mock.getvalue()

    async def test_upload_track_when_invalid_artist_oids(
        self,
        artist_mock: Artist,
        random_oid_mock: str,
        input_dict: dict,
        usecase: UploadTrackUseCase,
    ) -> None:
        with pytest.raises(BadRequestException):
            input_dict["artist_oids"] = ()
            UploadTrackDto(**input_dict)

        with pytest.raises(BadRequestException):
            input_dict["artist_oids"] = (random_oid_mock,)
            data = UploadTrackDto(**input_dict)
            await usecase.execute(data=data)

        with pytest.raises(BadRequestException):
            input_dict["artist_oids"] = (
                artist_mock.oid.value,
                random_oid_mock,
            )

            data = UploadTrackDto(**input_dict)
            await usecase.execute(data=data)

    async def test_upload_track_when_album_not_found(
        self,
        random_oid_mock: str,
        input_dict: dict,
        usecase: UploadTrackUseCase,
    ) -> None:
        with pytest.raises(BadRequestException):
            input_dict["album_oid"] = random_oid_mock
            data = UploadTrackDto(**input_dict)
            await usecase.execute(data)
