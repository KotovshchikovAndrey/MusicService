from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, UniqueConstraint, orm

from adapters.driven.sql import constraints
from adapters.driven.sql.models.base import Base
from domain.models.entities.otp_code import OTPCodePurpose


class OTPCode(Base):
    __table_args__ = (
        UniqueConstraint(
            "owner_id",
            "purpose",
            name=constraints.OTP_CODE_UNIQUE_CONSTRAINT,
        ),
    )

    code: orm.Mapped[int] = orm.mapped_column(
        Numeric(4, 0),
        nullable=False,
    )

    expired_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )

    purpose: orm.Mapped[OTPCodePurpose] = orm.mapped_column(nullable=False)

    owner_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
