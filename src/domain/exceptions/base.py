class DomainException(Exception):
    detail: str

    def __init__(self, detail: str) -> None:
        self.message = detail
