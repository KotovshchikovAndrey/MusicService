from uuid import UUID

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class Base(orm.DeclarativeBase):
    id: orm.Mapped[UUID] = orm.mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
