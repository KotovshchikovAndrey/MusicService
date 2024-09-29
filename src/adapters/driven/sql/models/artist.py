from sqlalchemy import ForeignKeyConstraint, String, orm

from adapters.driven.sql.models.base import Base


class Artist(Base):
    __table_args__ = (
        ForeignKeyConstraint(
            ["id"],
            ["user.id"],
            ondelete="CASCADE",
        ),
    )

    nickname: orm.Mapped[str] = orm.mapped_column(
        String(50),
        nullable=False,
    )

    avatar_url: orm.Mapped[str] = orm.mapped_column(
        String(255),
        nullable=False,
    )
