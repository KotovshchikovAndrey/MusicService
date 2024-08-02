from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(orm.DeclarativeBase):
    oid: orm.Mapped[str] = orm.mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        name="id",
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()

    def get_sql_values(self) -> dict:
        values = dict()
        for column in self.__table__.columns:
            value = getattr(self, column.name.replace("id", "oid"), None)
            values[column.name] = value

        return values
