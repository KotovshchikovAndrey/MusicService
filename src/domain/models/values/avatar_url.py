from domain.models.values.base import Url


class AvatarUrl(Url):
    def get_pattern(self) -> str:
        return r"\/[a-zA-Z\d\-_]+\.(png|jpeg|jpg)"
