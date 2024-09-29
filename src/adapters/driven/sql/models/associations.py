from sqlalchemy import Column, DateTime, ForeignKey, Table, UniqueConstraint, func

from adapters.driven.sql import constraints
from adapters.driven.sql.models.base import Base

track_artist = Table(
    "track_artist",
    Base.metadata,
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
        name=constraints.TRACK_ARTIST_UNIQUE_CONSTRAINT,
    ),
)

track_in_playlist = Table(
    "track_in_playlist",
    Base.metadata,
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
        server_default=func.now(),
    ),
    UniqueConstraint(
        "playlist_id",
        "track_id",
        name=constraints.TRACK_IN_PLAYLIST_UNIQUE_CONSTRAINT,
    ),
)

listener = Table(
    "listener",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "track_id",
        ForeignKey("track.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "last_listened_at",
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint(
        "user_id",
        "track_id",
        name=constraints.LISTENER_UNIQUE_CONSTRAINT,
    ),
)
