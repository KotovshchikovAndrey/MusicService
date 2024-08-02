from sqlalchemy import CheckConstraint, ForeignKey, Integer, orm, String, Numeric
from adapters.sql import consts
from adapters.sql.models.artist import ArtistModel
from adapters.sql.models.base import BaseModel
from adapters.sql.models.associations import track_artist
from adapters.sql.models.mixins import TitleMixin


class TrackModel(TitleMixin, BaseModel):
    __table_args__ = (
        CheckConstraint(
            "listens >= 0",
            name=consts.LISTENS_CHECK_CONSTRAINT,
        ),
    )

    audio_url: orm.Mapped[str] = orm.mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    duration: orm.Mapped[int] = orm.mapped_column(Numeric(3, 0), nullable=False)
    listens: orm.Mapped[int] = orm.mapped_column(
        Integer(),
        nullable=False,
        server_default="0",
    )
    album_oid: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("album.id", ondelete="CASCADE"),
        nullable=False,
        name="album_id",
    )
    artists: orm.Mapped[list["ArtistModel"]] = orm.relationship(
        lazy="joined",
        innerjoin=True,
        uselist=True,
        secondary=track_artist,
    )
