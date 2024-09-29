from fastapi import Request
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult

from domain.exceptions.base import BaseDomainException


class GraphQLController(GraphQLRouter):
    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {"data": result.data}
        if not result.errors:
            return data

        exc = result.errors[0].original_error
        if isinstance(exc, BaseDomainException):
            error = {"code": exc.exc_code, "detail": exc.detail}
            data["errors"] = [error]
            return data

        data["errors"] = [err.formatted for err in result.errors]
        return data
