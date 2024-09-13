from uuid import UUID

from sqlalchemy import inspect, orm
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class Base(orm.DeclarativeBase):
    id: orm.Mapped[UUID] = orm.mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()

    def to_dict_values(self) -> dict:
        values = dict()
        for column in inspect(self).mapper.column_attrs:
            value = getattr(self, column.key)
            if value is None:
                default_param = column.columns[0].default
                if default_param is not None:
                    value = default_param.arg

            values[column.key] = value

        return values
