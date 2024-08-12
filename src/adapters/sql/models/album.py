from datetime import datetime

from sqlalchemy import DateTime, orm

from adapters.sql.models.base import BaseModel
from adapters.sql.models.mixins import CoverUrlMixin, TitleMixin
from adapters.sql.models.track import TrackModel


class AlbumModel(TitleMixin, CoverUrlMixin, BaseModel):
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
    tracks: orm.Mapped[list["TrackModel"]] = orm.relationship(
        lazy="raise",
        order_by=TrackModel.title,
        back_populates="album",
    )
