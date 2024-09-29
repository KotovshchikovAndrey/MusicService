import strawberry

from adapters.driving.graphql.controller import GraphQLController
from config.settings import settings

from .resolvers.mutations import Mutation
from .resolvers.queries import Query

router = GraphQLController(
    strawberry.Schema(Query, Mutation),
    prefix="/graphql",
    graphiql=settings.is_debug,
)
