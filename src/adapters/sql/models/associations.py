from sqlalchemy import Column, DateTime, ForeignKey, Table, UniqueConstraint, text

from adapters.sql import consts
from adapters.sql.models.base import BaseModel

track_artist = Table(
    "track_artist",
    BaseModel.metadata,
    Column(
        "artist_id",
        ForeignKey("artist.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "track_id",
        ForeignKey("track.id", ondelete="CASCADE"),
        nullable=False,
    ),
    UniqueConstraint(
        "artist_id",
        "track_id",
        name=consts.TRACK_ARTIST_UNIQUE_CONSTRAINT,
    ),
)

track_in_playlist = Table(
    "track_in_playlist",
    BaseModel.metadata,
    Column(
        "playlist_id",
        ForeignKey("playlist.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "track_id",
        ForeignKey("track.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "added_at",
        DateTime(timezone=False),
        nullable=False,
        server_default=text("TIMEZONE('UTC', NOW())"),
    ),
    UniqueConstraint(
        "playlist_id",
        "track_id",
        name=consts.TRACK_IN_PLAYLIST_UNIQUE_CONSTRAINT,
    ),
)
