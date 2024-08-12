import strawberry
from strawberry.fastapi import GraphQLRouter

from .context import get_context
from .queries import Query

router = GraphQLRouter(
    strawberry.Schema(Query),
    prefix="/graphql",
    context_getter=get_context,
)
