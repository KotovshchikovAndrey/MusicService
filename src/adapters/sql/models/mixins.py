from sqlalchemy import String, orm


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
