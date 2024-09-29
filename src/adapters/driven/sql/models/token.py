from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, orm

from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CreatedAtMixin
from domain.models.entities.token import TokenType


class Token(CreatedAtMixin, Base):
    __table_args__ = (CheckConstraint("expired_at > created_at"),)

    token_type: orm.Mapped[TokenType] = orm.mapped_column(
        nullable=False,
        name="type",
    )

    expired_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )

    device_id: orm.Mapped[str] = orm.mapped_column(
        String(255),
        nullable=False,
    )

    is_revoked: orm.Mapped[bool] = orm.mapped_column(nullable=False)

    owner_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
