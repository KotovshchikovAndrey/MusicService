from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.s3.blob import S3BlobStorage
from adapters.sql.connection import SqlDatabaseConnection
from adapters.sql.uow import SqlUnitOfWork
from config.settings import settings
from domain.usecases.get_artists import GetArtistsUseCase
from domain.usecases.get_chart import GetChartUseCase
from domain.usecases.get_new_releases import GetNewReleasesUseCase
from domain.usecases.listen_track import ListenTrackUseCase
from domain.utils.blob import BlobStorage
from domain.utils.search import TrackElasticSearch
from domain.utils.uow import UnitOfWork

database = SqlDatabaseConnection(
    connection_url=settings.database.get_connection_url(),
    echo=True,
)


async def unit_of_work(
    session: Annotated[AsyncSession, Depends(database.get_session)]
) -> UnitOfWork:
    return SqlUnitOfWork(session=session)


def blob_storage() -> BlobStorage:
    return S3BlobStorage(
        address=settings.blob_storage.address,
        access_key_id=settings.blob_storage.access_key_id,
        secret_key=settings.blob_storage.secret_key,
        bucket_name=settings.blob_storage.bucket_name,
        use_ssl=settings.blob_storage.use_ssl,
    )


def track_elastic_search() -> TrackElasticSearch:
    return TrackElasticSearch(
        index_url=f"http://{settings.search.host}:{settings.search.port}/{settings.search.track_index}"
    )


def get_listen_track_usecase(
    uow: Annotated[UnitOfWork, Depends(unit_of_work)],
    blob_storage: Annotated[BlobStorage, Depends(blob_storage)],
) -> ListenTrackUseCase:
    return ListenTrackUseCase(
        uow=uow,
        blob_storage=blob_storage,
        chunk_size=settings.blob_storage.chunk_size,
    )


def get_new_releases_usecase(
    uow: Annotated[UnitOfWork, Depends(unit_of_work)]
) -> GetNewReleasesUseCase:
    return GetNewReleasesUseCase(uow=uow)


def get_chart_usecase(
    uow: Annotated[UnitOfWork, Depends(unit_of_work)]
) -> GetChartUseCase:
    return GetChartUseCase(uow=uow)


def get_artists_usecase(
    uow: Annotated[UnitOfWork, Depends(unit_of_work)]
) -> GetArtistsUseCase:
    return GetArtistsUseCase(uow=uow, limit=20)


ListenTrackDependency = Annotated[
    ListenTrackUseCase,
    Depends(get_listen_track_usecase),
]

GetNewReleasesDependency = Annotated[
    GetNewReleasesUseCase,
    Depends(get_new_releases_usecase),
]

GetChartDependency = Annotated[
    GetChartUseCase,
    Depends(get_chart_usecase),
]

GetArtistsDependency = Annotated[
    GetArtistsUseCase,
    Depends(get_artists_usecase),
]
