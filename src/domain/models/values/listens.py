from domain.models.values.base import BaseValue


class Listens(BaseValue[int]):
    def validate(self) -> None:
        if self.value < 0:
            raise ValueError("Listens cannot be a negative number")
