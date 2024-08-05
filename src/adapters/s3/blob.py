import typing as tp
from io import BytesIO

import aioboto3

from domain.utils.blob import BlobStorage


class S3BlobStorage(BlobStorage):
    _endpoint_url: str
    _access_key_id: str
    _secret_key: str
    _bucket_name: str
    _use_ssl: bool

    def __init__(
        self,
        address: str,
        access_key_id: str,
        secret_key: str,
        bucket_name: str,
        use_ssl: bool = False,
    ) -> None:
        self._access_key_id = access_key_id
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._use_ssl = use_ssl
        self._endpoint_url = (
            f"http://{address}" if not use_ssl else f"https://{address}"
        )

    async def read(
        self,
        blob_url: str,
        chunk_size: int,
        start_byte: int = 0,
        end_byte: int | None = None,
    ) -> tp.AsyncGenerator[bytes, None]:
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_key,
            use_ssl=self._use_ssl,
        ) as s3_client:
            if end_byte is None:
                end_byte = self.get_byte_size(blob_url)

            for offset in range(start_byte, end_byte, chunk_size):
                end = min(offset + chunk_size - 1, end_byte - 1)
                blob = await s3_client.get_object(
                    Bucket=self._bucket_name,
                    Key=self._get_key_from_url(blob_url),
                    Range=f"bytes={offset}-{end}",
                )

                async with blob["Body"] as io:
                    yield await io.read()

    async def put(self, blob_url: str, blob: BytesIO) -> None:
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_key,
            use_ssl=self._use_ssl,
        ) as s3_client:
            await s3_client.put_object(
                Bucket=self._bucket_name,
                Key=self._get_key_from_url(blob_url),
                Body=blob,
                ContentType="audio/mpeg",
                ContentLength=len(blob.getvalue()),
            )

    async def get_byte_size(self, blob_url: str) -> int:
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_key,
            use_ssl=self._use_ssl,
        ) as s3_client:
            blob_head = await s3_client.head_object(
                Bucket=self._bucket_name,
                Key=self._get_key_from_url(blob_url),
            )

            return blob_head["ContentLength"]

    def _get_key_from_url(self, blob_url: str) -> str:
        return blob_url.replace("/", "")
