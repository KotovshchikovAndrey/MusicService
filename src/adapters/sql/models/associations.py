from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from adapters.sql import consts
from adapters.sql.models.base import BaseModel

track_artist = Table(
    "track_artist",
    BaseModel.metadata,
    Column("artist_id", ForeignKey("artist.id", ondelete="CASCADE")),
    Column("track_id", ForeignKey("track.id", ondelete="CASCADE")),
    UniqueConstraint(
        "artist_id",
        "track_id",
        name=consts.TRACK_ARTIST_UNIQUE_CONSTRAINT,
    ),
)

track_in_playlist = Table(
    "track_in_playlist",
    BaseModel.metadata,
    Column("playlist_id", ForeignKey("playlist.id", ondelete="CASCADE")),
    Column("track_id", ForeignKey("track.id", ondelete="CASCADE")),
    UniqueConstraint(
        "playlist_id",
        "track_id",
        name=consts.TRACK_ARTIST_UNIQUE_CONSTRAINT,
    ),
)
