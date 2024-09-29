from datetime import datetime

from sqlalchemy import DateTime, String, orm


class TitleMixin:
    title: orm.Mapped[str] = orm.mapped_column(
        String(255),
        nullable=False,
    )


class CoverUrlMixin:
    cover_url: orm.Mapped[str] = orm.mapped_column(
        String(255),
        nullable=False,
    )


class CreatedAtMixin:
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
