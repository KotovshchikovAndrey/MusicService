import asyncio
from typing import Iterable
from uuid import UUID

from domain.builders.album import AlbumBuilder
from domain.builders.track import TrackBuilder
from domain.common.exceptions import BadRequestException
from domain.dtos.inputs import UploadAlbumDto, UploadReviewedAlbumDto, UploadTrackDto
from domain.entities.album import Album
from domain.entities.track import Track
from domain.usecases.base import BaseUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.distribution_service import DistributionServiceAdapter
from domain.utils.uow import UnitOfWork


class UploadReviewedAlbumUseCase(BaseUseCase[UploadReviewedAlbumDto, None]):
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

    async def execute(self, data: UploadReviewedAlbumDto) -> None:
        artist_ids_for_check = set()
        for track_data in data.tracks:
            artist_ids_for_check.update(track_data.artist_ids)

        await self._check_all_artists_exists(artist_ids_for_check)
        album = await self._upload_album(data=data.album)
        tracks = await self._upload_tracks(album=album, data=data.tracks)

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
                raise BadRequestException("One or more of the 'artist_ids' not found")

    async def _upload_album(self, data: UploadAlbumDto) -> Album:
        cover = await self._distribution_service.download_file(data.cover_download_url)
        album = (
            AlbumBuilder()
            .set_title(title=data.title)
            .set_cover(cover_url=cover.url)
            .build()
        )

        await self._blob_storage.put(blob_url=album.cover_url.value, blob=cover)
        return album

    async def _upload_tracks(
        self, album: Album, data: Iterable[UploadTrackDto]
    ) -> list[Track]:
        upload_tasks = []
        async with asyncio.TaskGroup() as group:
            for track_data in data:
                task = group.create_task(self._upload_track(album=album, data=track_data))
                upload_tasks.append(task)

        return [upload_task.result() for upload_task in upload_tasks]

    async def _upload_track(self, album: Album, data: UploadTrackDto) -> Track:
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
