import strawberry


@strawberry.type
class InvalidLimitParamException:
    message: str = "Invalid limit param. Expected limit > 0"


@strawberry.type
class InvalidPageParamException:
    message: str = "Invalid page param. Expected page > 0"
