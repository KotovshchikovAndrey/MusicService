import strawberry
from datetime import datetime


@strawberry.type
class AlbumSchema:
    oid: strawberry.ID
    title: str
    cover_url: str
    created_at: datetime
