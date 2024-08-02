from sqlalchemy import Text, orm
from adapters.sql.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from adapters.sql.models.mixins import CoverUrlMixin, TitleMixin
from adapters.sql.models.track import TrackModel
from adapters.sql.models.associations import track_in_playlist


class PlaylistModel(TitleMixin, CoverUrlMixin, BaseModel):
    user_oid: orm.Mapped[str] = orm.mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
        name="user_id",
    )
    description: orm.Mapped[str | None] = orm.mapped_column(Text(), nullable=True)
    tracks: orm.Mapped[list["TrackModel"]] = orm.relationship(
        lazy="noload",
        uselist=True,
        secondary=track_in_playlist,
    )
