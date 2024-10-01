from unittest.mock import call, patch
from uuid import uuid4

import pytest

from domain.errors.album import InvalidAlbumError
from domain.models.entities.album import Album
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
    @pytest.mark.parametrize(
        "data",
        (
            UploadAlbumDTO(
                album=AlbumMetaData(
                    title="Some album title",
                    cover_url="https://example.com/cover.png",
                ),
                tracks=[
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                ],
            ),
        ),
    )
    async def test_execute_successfully(
        self,
        data: UploadAlbumDTO,
        mock_uow: UnitOfWork,
        mock_blob_storage: BlobStorage,
        mock_file_downloader: FileDownloader,
        mock_track: Track,
        mock_album: Album,
    ) -> None:
        usecase = UploadAlbumUseCaseImpl(
            uow=mock_uow,
            blob_storage=mock_blob_storage,
            file_downloader=mock_file_downloader,
        )

        with (
            patch(
                "domain.models.builders.track.TrackBuilder.build"
            ) as mock_track_builder,
            patch(
                "domain.models.builders.album.AlbumBuilder.build"
            ) as mock_album_builder,
        ):
            mock_track_builder.return_value = mock_track
            mock_album_builder.return_value = mock_album

            album_id = await usecase.execute(data)
            assert mock_album.id == album_id

            mock_uow.albums.save.assert_called_once_with(mock_album)
            mock_uow.tracks.save_all.assert_called_once_with(
                [mock_track] * len(data.tracks)
            )

            mock_uow.commit.assert_called_once()

    @pytest.mark.parametrize(
        "data",
        (
            UploadAlbumDTO(
                album=AlbumMetaData(
                    title="Some album title",
                    cover_url="https://example.com/cover.png",
                ),
                tracks=[
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                ],
            ),
        ),
    )
    async def test_specify_artists_call_count(
        self,
        data: UploadAlbumDTO,
        mock_uow: UnitOfWork,
        mock_blob_storage: BlobStorage,
        mock_file_downloader: FileDownloader,
        mock_track: Track,
    ) -> None:
        mock_uow.artists.exists_all.return_value = True
        usecase = UploadAlbumUseCaseImpl(
            uow=mock_uow,
            blob_storage=mock_blob_storage,
            file_downloader=mock_file_downloader,
        )

        with patch(
            "domain.models.builders.track.TrackBuilder.build"
        ) as mock_track_builder:
            mock_track_builder.return_value = mock_track
            await usecase.execute(data)

            assert mock_uow.tracks.specify_artists.call_count == len(data.tracks)
            expected_calls = [
                call(track_id=mock_track.id, artist_ids=data.tracks[0].artist_ids),
                call(track_id=mock_track.id, artist_ids=data.tracks[1].artist_ids),
                call(track_id=mock_track.id, artist_ids=data.tracks[2].artist_ids),
            ]

            mock_uow.tracks.specify_artists.assert_has_calls(expected_calls)

    @pytest.mark.parametrize(
        "data",
        (
            UploadAlbumDTO(
                album=AlbumMetaData(
                    title="Some album title",
                    cover_url="https://example.com/cover.png",
                ),
                tracks=[
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                    TrackMetaData(
                        title="Some track title",
                        duration=60 * 3,
                        audio_url="https://example.com/audio.mp3",
                        artist_ids={uuid4()},
                    ),
                ],
            ),
        ),
    )
    async def test_execute_when_one_or_more_artist_not_exists(
        self,
        data: UploadAlbumDTO,
        mock_uow: UnitOfWork,
        mock_blob_storage: BlobStorage,
        mock_file_downloader: FileDownloader,
    ) -> None:
        mock_uow.artists.exists_all.return_value = False
        usecase = UploadAlbumUseCaseImpl(
            uow=mock_uow,
            blob_storage=mock_blob_storage,
            file_downloader=mock_file_downloader,
        )

        with pytest.raises(InvalidAlbumError):
            await usecase.execute(data)
