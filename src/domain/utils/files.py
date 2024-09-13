import functools
import hashlib
import pathlib
from io import BytesIO
from typing import Protocol


class DownloadFileFunction(Protocol):
    async def __call__(self, download_url: str, *args, **kwargs) -> BytesIO: ...


def add_url_for_downloaded_file(function: DownloadFileFunction):
    """Get download_url from function args and
    add url attribute for BytesIO object. Output: file_io.url = "/unique_name.txt"
    """

    @functools.wraps(function)
    async def wrapper(download_url: str, *args, **kwargs) -> BytesIO:
        file_io = await function(download_url, *args, **kwargs)
        hashed_file = hashlib.sha256(file_io.getvalue()).hexdigest()

        file_ext = pathlib.Path(download_url).suffix
        file_url = f"/{hashed_file}{file_ext}"
        file_io.url = file_url

        return file_io

    return wrapper
