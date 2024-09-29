from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.sql.mappers.user import map_to_insert_user_values, map_to_user
from adapters.driven.sql.models import User as UserModel
from domain.models.entities.user import User
from domain.ports.driven.database.user_repository import UserRepository


class UserSQLRepository(UserRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_user(model)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_user(model)

    async def save(self, user: User) -> None:
        values = map_to_insert_user_values(user)
        stmt = insert(UserModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[UserModel.id],
            set_=dict(email=stmt.excluded.email, is_active=stmt.excluded.is_active),
        )

        await self._session.execute(stmt)
