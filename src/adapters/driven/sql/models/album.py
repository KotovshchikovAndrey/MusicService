from sqlalchemy import orm

from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CoverUrlMixin, CreatedAtMixin, TitleMixin
from adapters.driven.sql.models.track import Track


class Album(TitleMixin, CoverUrlMixin, CreatedAtMixin, Base):
    tracks: orm.Mapped[list["Track"]] = orm.relationship(
        lazy="raise",
        order_by=Track.title,
        back_populates="album",
    )
