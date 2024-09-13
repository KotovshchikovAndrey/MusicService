from sqlalchemy import String, orm

from adapters.driven.sql.models.base import Base


class Artist(Base):
    nickname: orm.Mapped[str] = orm.mapped_column(
        String(50),
        nullable=False,
    )

    avatar_url: orm.Mapped[str] = orm.mapped_column(
        String(255),
        nullable=False,
    )
