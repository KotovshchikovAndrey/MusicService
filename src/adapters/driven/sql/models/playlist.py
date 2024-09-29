from sqlalchemy import ForeignKey, Text, orm
from sqlalchemy.dialects.postgresql import UUID

from adapters.driven.sql.models.associations import track_in_playlist
from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CoverUrlMixin, TitleMixin
from adapters.driven.sql.models.track import Track


class Playlist(TitleMixin, CoverUrlMixin, Base):
    user_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    description: orm.Mapped[str | None] = orm.mapped_column(
        Text(),
        nullable=True,
    )

    tracks: orm.Mapped[list["Track"]] = orm.relationship(
        lazy="raise",
        secondary=track_in_playlist,
    )
