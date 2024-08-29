import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from adapters.driven.sql.models.track import TrackModel
from adapters.driven.sql.repositories.track import TrackSqlRepository
from domain.builders.track import TrackBuilder
from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track


class TestTrackSqlRepository:
    async def test_get_by_id(self, session: AsyncSession, track_mock: Track) -> None:
        repository = TrackSqlRepository(session=session)
        track = await repository.get_by_id(track_mock.id)

        assert track is not None
        assert track.id == track_mock.id
        assert track.title == track_mock.title
        assert track.album_id == track_mock.album_id
        assert track.audio_url == track_mock.audio_url
        assert track.duration == track_mock.duration
        assert track.listens == track_mock.listens

    async def test_update(self, session: AsyncSession, track_mock: Track) -> None:
        repository = TrackSqlRepository(session=session)
        track = await repository.get_by_id(track_mock.id)
        assert track is not None

        old_title = track.title
        new_title = "New title"
        track.change_title(new_title)
        await repository.save(track)

        updated_track = await repository.get_by_id(track_mock.id)
        assert updated_track is not None
        assert updated_track.title != old_title

        assert updated_track.id == track_mock.id
        assert updated_track.title.value == new_title
        assert updated_track.album_id == track_mock.album_id
        assert updated_track.audio_url == track_mock.audio_url
        assert updated_track.duration == track_mock.duration
        assert updated_track.listens == track_mock.listens

    async def test_create(self, session: AsyncSession, album_mock: Album) -> None:
        new_track = (
            TrackBuilder()
            .set_title(title="In The End")
            .set_audio(audio_url="/track_url.mp3")
            .set_duration(duration=2.5 * 60)
            .set_album(album_id=album_mock.id)
            .build()
        )

        repository = TrackSqlRepository(session=session)
        track = await repository.get_by_id(new_track.id)
        assert track is None

        await repository.save(new_track)
        track = await repository.get_by_id(new_track.id)

        assert track is not None
        assert track.id == new_track.id
        assert track.title == new_track.title
        assert track.album_id == new_track.album_id
        assert track.audio_url == new_track.audio_url
        assert track.duration == new_track.duration
        assert track.listens == new_track.listens

    async def test_create_all(self, session: AsyncSession, album_mock: Album) -> None:
        track_builder = (
            TrackBuilder()
            .set_title(title="In The End")
            .set_duration(duration=2.5 * 60)
            .set_album(album_id=album_mock.id)
        )

        new_track_1 = track_builder.set_audio(audio_url="/track_url_0.mp3").build()
        new_track_2 = track_builder.set_audio(audio_url="/track_url_1.mp3").build()
        new_track_3 = track_builder.set_audio(audio_url="/track_url_2.mp3").build()

        repository = TrackSqlRepository(session=session)
        track_1 = await repository.get_by_id(track_id=new_track_1.id)
        track_2 = await repository.get_by_id(track_id=new_track_2.id)
        track_3 = await repository.get_by_id(track_id=new_track_3.id)

        assert not any([track_1, track_2, track_3])
        await repository.save_all([new_track_1, new_track_2, new_track_3])

        track_1 = await repository.get_by_id(track_id=new_track_1.id)
        track_2 = await repository.get_by_id(track_id=new_track_2.id)
        track_3 = await repository.get_by_id(track_id=new_track_3.id)

        assert track_1 == new_track_1
        assert track_2 == new_track_2
        assert track_3 == new_track_3

    async def test_set_artists(
        self, session: AsyncSession, track_mock: Track, artist_mock: Artist
    ) -> None:
        stmt = (
            select(TrackModel)
            .options(joinedload(TrackModel.artists))
            .where(TrackModel.id == track_mock.id)
        )

        track_model = await session.scalar(stmt)
        assert track_model is not None
        artist_count_before_update = len(track_model.artists)

        repository = TrackSqlRepository(session=session)
        artist_ids = (artist_mock.id,)
        await repository.set_artists(track_id=track_mock.id, artist_ids=artist_ids)
        await session.refresh(track_model)

        updated_track_model = await session.scalar(stmt)
        assert len(track_model.artists) == artist_count_before_update + 1
        assert all(
            artist_id in [artist.id for artist in updated_track_model.artists]
            for artist_id in artist_ids
        )

    async def test_increment_listens(
        self, session: AsyncSession, track_mock: Track
    ) -> None:
        repository = TrackSqlRepository(session=session)
        track_before_increment = await repository.get_by_id(track_mock.id)
        assert track_before_increment is not None

        await repository.increment_listens(track_mock.id)
        track_after_increment = await repository.get_by_id(track_mock.id)
        assert (
            track_after_increment.listens.value
            == track_before_increment.listens.value + 1
        )
