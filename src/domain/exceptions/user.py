from domain.exceptions.base import NotFound


class UserNotFound(NotFound):
    def __init__(self) -> None:
        super().__init__(detail="User not found")
