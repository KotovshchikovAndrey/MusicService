import hashlib
import pathlib

type BlobUrl = str


class FileManagerMixin:
    async def _transfer_file_to_blob_storage(self, download_url: str) -> BlobUrl:
        file = await self._file_downloader.download_by_url(url=download_url)
        file_hash = hashlib.sha256(file.getvalue()).hexdigest()
        file_ext = pathlib.Path(download_url).suffix

        blob_url = f"/{file_hash}{file_ext}"
        await self._blob_storage.put(blob_url=blob_url, blob=file)
        return blob_url
