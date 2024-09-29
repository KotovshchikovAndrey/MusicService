from dataclasses import dataclass
from typing import Self

from domain.models.builders.base import BaseBuilder
from domain.models.entities.user import User
from domain.models.values.email import Email


@dataclass(eq=False, init=False, slots=True)
class UserBuilder(BaseBuilder[User]):
    _email: Email

    def set_email(self, email: str) -> Self:
        self._email = Email(email)
        return self

    def build(self) -> User:
        return User(email=self._email)
