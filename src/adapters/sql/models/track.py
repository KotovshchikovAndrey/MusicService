from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    orm,
)

from adapters.sql import consts
from adapters.sql.models.artist import ArtistModel
from adapters.sql.models.associations import track_artist
from adapters.sql.models.base import BaseModel
from adapters.sql.models.mixins import TitleMixin

if TYPE_CHECKING:
    from adapters.sql.models.album import AlbumModel


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
    duration: orm.Mapped[int] = orm.mapped_column(
        Numeric(3, 0),
        nullable=False,
    )
    listens: orm.Mapped[int] = orm.mapped_column(
        BigInteger(),
        nullable=False,
        server_default="0",
    )
    listens_per_day: orm.Mapped[int] = orm.mapped_column(
        Integer(),
        nullable=False,
        server_default="0",
    )
    album_oid: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("album.id", ondelete="CASCADE"),
        nullable=False,
        name="album_id",
    )
    album: orm.Mapped["AlbumModel"] = orm.relationship(lazy="raise")
    artists: orm.Mapped[list["ArtistModel"]] = orm.relationship(
        lazy="raise",
        secondary=track_artist,
    )
