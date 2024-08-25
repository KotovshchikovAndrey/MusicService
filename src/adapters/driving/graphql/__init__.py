import strawberry
from strawberry.fastapi import GraphQLRouter

from config.settings import settings

from .queries import Query

router = GraphQLRouter(
    strawberry.Schema(Query),
    prefix="/graphql",
    graphiql=settings.is_debug,
)
