import strawberry


@strawberry.type(name="Pagination")
class PaginationSchema:
    count: int
    total_count: int
    total_pages: int
    current_page: int
    next_page: int | None = None
    prev_page: int | None = None


@strawberry.type(name="JwtPair")
class JwtPairSchema:
    access_token: str
    refresh_token: str
