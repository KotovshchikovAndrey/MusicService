from sqlalchemy import String, orm
from adapters.sql.models.base import BaseModel


class ArtistModel(BaseModel):
    nickname: orm.Mapped[str] = orm.mapped_column(String(50), nullable=False)
    avatar_url: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
