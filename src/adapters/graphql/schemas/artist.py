import strawberry


@strawberry.type
class ArtistSchema:
    oid: strawberry.ID
    nickname: str
    avatar_url: str
