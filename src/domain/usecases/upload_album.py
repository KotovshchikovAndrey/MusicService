import asyncio
from typing import Iterable
from uuid import UUID

from domain.exceptions.album import InvalidAlbumUploadingData
from domain.models.builders.album import AlbumBuilder
from domain.models.builders.track import TrackBuilder
from domain.models.entities.album import Album
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.distribution_service import DistributionServiceAdapter
from domain.ports.driving.uploading_albums import (
    AlbumMetaData,
    TrackMetaData,
    UploadAlbumDto,
    UploadAlbumUseCase,
)


class UploadAlbumUseCaseImpl(UploadAlbumUseCase):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _distribution_service: DistributionServiceAdapter

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        distribution_service: DistributionServiceAdapter,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._distribution_service = distribution_service

    async def execute(self, data: UploadAlbumDto) -> None:
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

    async def _check_all_artists_exists(self, artist_ids: set[UUID]) -> None:
        async with self._uow as uow:
            artists = await uow.artists.filter_by_ids(artist_ids)
            if len(artist_ids) != len(artists):
                raise InvalidAlbumUploadingData(
                    reason="One or more of the 'artist_ids' not found"
                )

    async def _prepare_album_to_save(self, data: AlbumMetaData) -> Album:
        cover = await self._distribution_service.download_file(data.cover_download_url)
        album = (
            AlbumBuilder()
            .set_title(title=data.title)
            .set_cover(cover_url=cover.url)
            .build()
        )

        await self._blob_storage.put(blob_url=album.cover_url.value, blob=cover)
        return album

    async def _prepare_tracks_to_save(
        self, album: Album, data: Iterable[TrackMetaData]
    ) -> list[Track]:
        tasks = []
        async with asyncio.TaskGroup() as group:
            for track_data in data:
                coro = self._prepare_track_to_save(album=album, data=track_data)
                task = group.create_task(coro)
                tasks.append(task)

        return [task.result() for task in tasks]

    async def _prepare_track_to_save(self, album: Album, data: TrackMetaData) -> Track:
        audio = await self._distribution_service.download_file(data.audio_download_url)
        track = (
            TrackBuilder()
            .set_album(album_id=album.id)
            .set_title(title=data.title)
            .set_duration(duration=data.duration)
            .set_audio(audio_url=audio.url)
            .build()
        )

        await self._blob_storage.put(blob_url=track.audio_url.value, blob=audio)
        return track
