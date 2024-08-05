from domain.values.base import BaseValue


class Listens(BaseValue[int]):
    def validate(self) -> None:
        if self.value < 0:
            raise ValueError("Listens must be positive number")
