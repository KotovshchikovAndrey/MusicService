from dataclasses import dataclass

from fastapi import Depends
from strawberry.fastapi import BaseContext

from config.dependencies import GetChartDependency, GetNewReleasesDependency


@dataclass
class GraphqlContext(BaseContext):
    get_chart_usecase: GetChartDependency
    get_new_releases: GetNewReleasesDependency


async def get_context(
    context: GraphqlContext = Depends(GraphqlContext),
):
    return context
