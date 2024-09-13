from datetime import datetime

from sqlalchemy import DateTime, orm

from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CoverUrlMixin, TitleMixin
from adapters.driven.sql.models.track import Track


class Album(TitleMixin, CoverUrlMixin, Base):
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )

    tracks: orm.Mapped[list["Track"]] = orm.relationship(
        lazy="raise",
        order_by=Track.title,
        back_populates="album",
    )
