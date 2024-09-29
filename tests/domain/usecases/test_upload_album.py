from unittest.mock import call, patch
from uuid import uuid4

import pytest

from domain.exceptions.album import InvalidAlbumInput
from domain.models.entities.album import Album
from domain.models.entities.artist import Artist
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driving.album_uploading import (
    AlbumMetaData,
    TrackMetaData,
    UploadAlbumDTO,
)
from domain.usecases.upload_album import UploadAlbumUseCaseImpl


class TestUploadAlbumUseCase:
    @pytest.fixture(scope="function")
    def album_valid_data(self, album_mock: Album) -> dict:
        return dict(
            title=album_mock.title.value,
            cover_download_url="/media" + album_mock.cover_url.value,
        )

    @pytest.fixture(scope="function")
    def track_valid_data(self, track_mock: Track, artist_mock: Artist) -> dict:
        return dict(
            title=track_mock.title.value,
            audio_download_url="/media" + track_mock.audio_url.value,
            duration=track_mock.duration.value,
            artist_ids={artist_mock.id},
        )

    async def test_execute_successfully(
        self,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        file_downloader_mock: FileDownloader,
        album_valid_data: dict,
        track_valid_data: dict,
        track_mock: Track,
        album_mock: Album,
    ) -> None:
        usecase = UploadAlbumUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            file_downloader=file_downloader_mock,
        )

        data = UploadAlbumDTO(
            album=AlbumMetaData(**album_valid_data),
            tracks=[TrackMetaData(**track_valid_data)],
        )

        with (
            patch(
                "domain.models.builders.track.TrackBuilder.build"
            ) as track_builder_mock,
            patch(
                "domain.models.builders.album.AlbumBuilder.build"
            ) as album_builder_mock,
        ):
            track_builder_mock.return_value = track_mock
            album_builder_mock.return_value = album_mock

            album_id = await usecase.execute(data)
            assert album_mock.id == album_id

            uow_mock.albums.save.assert_called_once_with(album_mock)
            uow_mock.tracks.save_all.assert_called_once_with([track_mock])
            uow_mock.tracks.set_artists.assert_called_with(
                track_id=track_mock.id,
                artist_ids=data.tracks[0].artist_ids,
            )

            uow_mock.commit.assert_called_once()

    @pytest.mark.parametrize(
        "tracks",
        (
            [
                TrackMetaData(
                    title="Track",
                    audio_download_url="/audio_0.mp3",
                    artist_ids={uuid4()},
                    duration=100,
                ),
                TrackMetaData(
                    title="Track",
                    audio_download_url="/audio_1.mp3",
                    artist_ids={uuid4(), uuid4()},
                    duration=100,
                ),
                TrackMetaData(
                    title="Track",
                    audio_download_url="/audio_2.mp3",
                    artist_ids={uuid4(), uuid4(), uuid4()},
                    duration=100,
                ),
            ],
        ),
    )
    async def test_set_artists_calls(
        self,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        file_downloader_mock: FileDownloader,
        album_valid_data: dict,
        tracks: list[TrackMetaData],
        track_mock: Track,
    ) -> None:
        usecase = UploadAlbumUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            file_downloader=file_downloader_mock,
        )

        data = UploadAlbumDTO(album=AlbumMetaData(**album_valid_data), tracks=tracks)
        with patch(
            "domain.models.builders.track.TrackBuilder.build"
        ) as track_builder_mock:
            track_builder_mock.return_value = track_mock
            uow_mock.artists.filter_by_ids.return_value = (
                tracks[0].artist_ids | tracks[1].artist_ids | tracks[2].artist_ids
            )

            await usecase.execute(data)
            assert uow_mock.tracks.set_artists.call_count == len(data.tracks)

            expected_calls = [
                call(track_id=track_mock.id, artist_ids=tracks[0].artist_ids),
                call(track_id=track_mock.id, artist_ids=tracks[1].artist_ids),
                call(track_id=track_mock.id, artist_ids=tracks[2].artist_ids),
            ]

            uow_mock.tracks.set_artists.assert_has_calls(expected_calls)

    async def test_execute_when_invalid_artist_ids(
        self,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        file_downloader_mock: FileDownloader,
        album_valid_data: dict,
        track_valid_data: dict,
    ) -> None:
        usecase = UploadAlbumUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            file_downloader=file_downloader_mock,
        )

        data = UploadAlbumDTO(
            album=AlbumMetaData(**album_valid_data),
            tracks=[TrackMetaData(**track_valid_data)],
        )

        with pytest.raises(InvalidAlbumInput):
            uow_mock.artists.filter_by_ids.return_value = []
            await usecase.execute(data)

        with pytest.raises(ValueError):
            track_valid_data["artist_ids"] = set()
            TrackMetaData(**track_valid_data)
