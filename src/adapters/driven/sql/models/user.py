from sqlalchemy import String, orm

from adapters.driven.sql.models.base import Base
from adapters.driven.sql.models.mixins import CreatedAtMixin
from domain.models.entities.otp_code import OTPCode


class User(CreatedAtMixin, Base):
    email: orm.Mapped[str] = orm.mapped_column(
        String(70),
        nullable=False,
        unique=True,
    )

    is_active: orm.Mapped[bool] = orm.mapped_column(nullable=False)

    otp_codes: orm.Mapped[list["OTPCode"]] = orm.relationship(
        lazy="selectin",
        uselist=True,
    )
