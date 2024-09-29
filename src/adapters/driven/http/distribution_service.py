from http import HTTPStatus
from io import BytesIO

import httpx

from domain.ports.driven.file_downloader import FileDownloader
from utils.files import add_url_for_downloaded_file


class DistributionServiceHttpAdapter(FileDownloader):
    _api_url: str

    def __init__(self, api_url: str) -> None:
        self._api_url = api_url

    @add_url_for_downloaded_file
    async def download_file(self, download_url: str) -> BytesIO:
        async with httpx.AsyncClient(base_url=self._api_url) as client:
            response = await client.get(url=download_url)
            if response.status_code != HTTPStatus.OK:
                raise ...

            return BytesIO(response.content)
