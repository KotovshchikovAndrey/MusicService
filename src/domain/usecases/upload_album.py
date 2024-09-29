import asyncio
from uuid import UUID

from domain.exceptions.album import InvalidAlbumInput
from domain.models.builders.album import AlbumBuilder
from domain.models.builders.track import TrackBuilder
from domain.models.entities.album import Album
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driving.album_uploading import (
    AlbumMetaData,
    TrackMetaData,
    UploadAlbumDTO,
    UploadAlbumUseCase,
)
from domain.usecases.mixins.file_manager_mixin import FileManagerMixin


class UploadAlbumUseCaseImpl(FileManagerMixin, UploadAlbumUseCase):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _file_downloader: FileDownloader

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        file_downloader: FileDownloader,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._file_downloader = file_downloader

    async def execute(self, data: UploadAlbumDTO) -> None:
        artist_ids_for_check = set()
        for track_data in data.tracks:
            artist_ids_for_check.update(track_data.artist_ids)

        await self._check_all_artists_exists(artist_ids_for_check)
        album = await self._prepare_album_to_save(data=data.album)
        tracks = await self._prepare_tracks_to_save(album=album, data=data.tracks)

        track_artists = []
        for index, track in enumerate(tracks):
            artist_ids = data.tracks[index].artist_ids
            track_artists.append((track.id, artist_ids))

        async with self._uow as uow:
            await uow.albums.save(album)
            await uow.tracks.save_all(tracks)
            for track_id, artist_ids in track_artists:
                await uow.tracks.set_artists(track_id=track_id, artist_ids=artist_ids)

            await uow.commit()

        return album.id

    async def _check_all_artists_exists(self, artist_ids: set[UUID]) -> None:
        async with self._uow as uow:
            artists = await uow.artists.filter_by_ids(artist_ids)
            if len(artist_ids) != len(artists):
                raise InvalidAlbumInput(
                    detail="One or more of the 'artist_ids' not found"
                )

    async def _prepare_album_to_save(self, data: AlbumMetaData) -> Album:
        cover_url = await self._transfer_file_to_blob_storage(data.cover_download_url)
        album = (
            AlbumBuilder()
            .set_title(title=data.title)
            .set_cover(cover_url=cover_url)
            .build()
        )

        return album

    async def _prepare_tracks_to_save(
        self, album: Album, data: list[TrackMetaData]
    ) -> list[Track]:
        tasks = []
        async with asyncio.TaskGroup() as group:
            for track_data in data:
                coroutine = self._prepare_track_to_save(album=album, data=track_data)
                task = group.create_task(coroutine)
                tasks.append(task)

        return [task.result() for task in tasks]

    async def _prepare_track_to_save(self, album: Album, data: TrackMetaData) -> Track:
        audio_url = await self._transfer_file_to_blob_storage(data.audio_download_url)
        track = (
            TrackBuilder()
            .set_album(album_id=album.id)
            .set_title(title=data.title)
            .set_duration(duration=data.duration)
            .set_audio(audio_url=audio_url)
            .build()
        )

        return track
