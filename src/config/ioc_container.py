from punq import Container

from adapters.driven.http.distribution_service import DistributionServiceHttpAdapter
from adapters.driven.s3.blob_storage import S3BlobStorage
from adapters.driven.sql.connection import SqlDatabaseConnection
from adapters.driven.sql.uow import SqlUnitOfWork
from config.settings import settings
from domain.usecases.get_artists import GetArtistsUseCase
from domain.usecases.get_chart import GetChartUseCase
from domain.usecases.get_new_releases import GetNewReleasesUseCase
from domain.usecases.listen_track import ListenTrackUseCase
from domain.usecases.register_created_artist import RegisterCreatedArtistUseCase
from domain.usecases.upload_reviewed_album import UploadReviewedAlbumUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.distribution_service import DistributionServiceAdapter
from domain.utils.uow import UnitOfWork

container = Container()


# Adapters

database = SqlDatabaseConnection(
    connection_url=settings.database.get_connection_url(),
    echo=settings.is_debug,
)

container.register(SqlDatabaseConnection, instance=database)

container.register(UnitOfWork, SqlUnitOfWork)

blob_storage = S3BlobStorage(
    address=settings.blob_storage.address,
    access_key_id=settings.blob_storage.access_key_id,
    secret_key=settings.blob_storage.secret_key,
    bucket_name=settings.blob_storage.bucket_name,
    use_ssl=settings.blob_storage.use_ssl,
)

container.register(BlobStorage, instance=blob_storage)

container.register(DistributionServiceAdapter, DistributionServiceHttpAdapter)


# UseCases

container.register(GetChartUseCase, GetChartUseCase)

container.register(GetNewReleasesUseCase, GetNewReleasesUseCase)

container.register(
    GetArtistsUseCase,
    GetArtistsUseCase,
    limit=20,
)

container.register(
    ListenTrackUseCase,
    ListenTrackUseCase,
    chunk_size=settings.blob_storage.chunk_size,
)

container.register(RegisterCreatedArtistUseCase, RegisterCreatedArtistUseCase)

container.register(UploadReviewedAlbumUseCase, UploadReviewedAlbumUseCase)
