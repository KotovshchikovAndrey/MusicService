import strawberry

from domain.ports.driving.track_search import SearchTrackDTO


@strawberry.input
class SearchTrackInput:
    limit: int
    query: str

    def to_dto(self) -> SearchTrackDTO:
        return SearchTrackDTO(limit=self.limit, query=self.query)
