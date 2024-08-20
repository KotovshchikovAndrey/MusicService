from uuid import UUID

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class BaseModel(orm.DeclarativeBase):
    id: orm.Mapped[UUID] = orm.mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()

    def get_values_to_upsert(self, exclude: set[str] | None = None) -> dict:
        values = dict()
        for column in self.__table__.columns:
            model_field_name = column.name
            if exclude is not None and model_field_name in exclude:
                continue

            value = getattr(self, model_field_name, None)
            values[column.name] = value

        return values
