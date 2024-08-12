import strawberry
from strawberry.fastapi import GraphQLRouter

from config.settings import settings

from .context import get_context
from .queries import Query

router = GraphQLRouter(
    strawberry.Schema(Query),
    prefix="/graphql",
    context_getter=get_context,
    graphiql=settings.is_debug,
)
