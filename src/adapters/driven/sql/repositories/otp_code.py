from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.sql import constraints
from adapters.driven.sql.mappers.otp_code import (
    map_to_insert_otp_code_values,
    map_to_otp_code,
)
from adapters.driven.sql.models.otp_code import OTPCode as OTPCodeModel
from domain.models.entities.otp_code import OTPCode, OTPCodePurpose
from domain.ports.driven.database.otp_code_repository import OTPCodeRepository


class OTPCodeSQLRepository(OTPCodeRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_owner_and_purpose(
        self, owner_id: UUID, purpose: OTPCodePurpose
    ) -> OTPCode | None:
        stmt = select(OTPCodeModel).where(
            and_(
                OTPCodeModel.owner_id == owner_id,
                OTPCodeModel.purpose == purpose,
            )
        )

        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_otp_code(model)

    async def save(self, otp_code: OTPCode) -> None:
        values = map_to_insert_otp_code_values(otp_code)
        stmt = insert(OTPCodeModel).values(values)
        stmt = stmt.on_conflict_do_update(
            constraint=constraints.OTP_CODE_UNIQUE_CONSTRAINT,
            set_=dict(code=stmt.excluded.code, expired_at=stmt.excluded.expired_at),
        )

        await self._session.execute(stmt)

    async def remove_by_id(self, otp_code_id: UUID) -> None:
        stmt = delete(OTPCodeModel).where(OTPCodeModel.id == otp_code_id)
        await self._session.execute(stmt)
