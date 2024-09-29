from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, and_, func, orm, select

from adapters.driven.sql.models.artist import Artist
from adapters.driven.sql.models.associations import listener, track_artist
from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import TitleMixin

if TYPE_CHECKING:
    from adapters.driven.sql.models.album import Album


class Track(TitleMixin, Base):
    audio_url: orm.Mapped[str] = orm.mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    duration: orm.Mapped[int] = orm.mapped_column(
        Numeric(3, 0),
        nullable=False,
    )

    album_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("album.id", ondelete="CASCADE"),
        nullable=False,
    )

    album: orm.Mapped["Album"] = orm.relationship(
        lazy="raise",
        back_populates="tracks",
    )

    artists: orm.Mapped[list["Artist"]] = orm.relationship(
        lazy="raise",
        secondary=track_artist,
    )


Track.listens = orm.column_property(
    select(func.count(listener.c.user_id))
    .where(listener.c.track_id == Track.id)
    .scalar_subquery()
)

Track.listens_per_day = orm.column_property(
    select(func.count(listener.c.user_id))
    .where(
        and_(
            listener.c.track_id == Track.id,
            listener.c.last_listened_at
            >= datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1),
        )
    )
    .scalar_subquery()
)
