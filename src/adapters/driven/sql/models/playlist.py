from sqlalchemy import Text, orm
from sqlalchemy.dialects.postgresql import UUID

from adapters.driven.sql.models.associations import track_in_playlist
from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CoverUrlMixin, TitleMixin
from adapters.driven.sql.models.track import Track


class Playlist(TitleMixin, CoverUrlMixin, Base):
    user_id: orm.Mapped[str] = orm.mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
        name="user_id",
    )

    description: orm.Mapped[str | None] = orm.mapped_column(
        Text(),
        nullable=True,
    )

    tracks: orm.Mapped[list["Track"]] = orm.relationship(
        lazy="raise",
        secondary=track_in_playlist,
        # order_by=track_in_playlist.columns.get("added_at"),
    )
