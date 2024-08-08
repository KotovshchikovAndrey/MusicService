import strawberry
from strawberry.fastapi import GraphQLRouter
from .queries import Query
from .context import get_context


router = GraphQLRouter(
    strawberry.Schema(Query),
    prefix="/graphql",
    context_getter=get_context,
)
