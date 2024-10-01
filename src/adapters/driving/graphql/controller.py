from fastapi import Request
from pydantic import ValidationError
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult

from domain.errors.base import DomainError


class GraphQLController(GraphQLRouter):
    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {"data": result.data}
        if not result.errors:
            return data

        exc = result.errors[0].original_error
        if isinstance(exc, DomainError):
            error = {"error": exc.error, "message": exc.message}
            data["errors"] = [error]
            return data

        if isinstance(exc, ValueError):
            error = {
                "error": ValueError.__name__,
                "message": "invalid request data",
                "detail": (
                    exc.errors(include_url=False, include_context=False)
                    if isinstance(exc, ValidationError)
                    else str(exc)
                ),
            }

            data["errors"] = [error]
            return data

        data["errors"] = [err.formatted for err in result.errors]
        return data
