from dataclasses import dataclass

from fastapi import Depends
from strawberry.fastapi import BaseContext

from config.dependencies import (
    GetArtistsDependency,
    GetChartDependency,
    GetNewReleasesDependency,
)


@dataclass
class GraphqlContext(BaseContext):
    get_chart: GetChartDependency
    get_new_releases: GetNewReleasesDependency
    get_artists: GetArtistsDependency


async def get_context(
    context: GraphqlContext = Depends(GraphqlContext),
):
    return context
