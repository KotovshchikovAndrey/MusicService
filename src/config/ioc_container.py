from typing import Type
from punq import Container

from adapters.driven.http.distribution_service import DistributionServiceHttpAdapter
from adapters.driven.s3.blob_storage import S3BlobStorage
from adapters.driven.sql.connection import SqlDatabaseConnection
from adapters.driven.sql.unit_of_work import SqlUnitOfWork
from config.settings import settings
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.distribution_service import DistributionServiceAdapter
from domain.ports.driving.getting_artists import GetArtistsUseCase
from domain.ports.driving.getting_chart import GetChartUseCase
from domain.ports.driving.getting_new_albums import GetNewAlbumsUseCase
from domain.ports.driving.listening_tracks import ListenTrackUseCase
from domain.ports.driving.registering_artists import RegisterArtistUseCase
from domain.ports.driving.uploading_albums import UploadAlbumUseCase
from domain.usecases.get_artists import GetArtistsUseCaseImpl
from domain.usecases.get_chart import GetChartUseCaseImpl
from domain.usecases.get_new_albums import GetNewAlbumsUseCaseImpl
from domain.usecases.listen_track import ListenTrackUseCaseImpl
from domain.usecases.register_artist import RegisterArtistUseCaseImpl
from domain.usecases.upload_album import UploadAlbumUseCaseImpl


class IoCContainer:
    _container: Container
    _is_inited: bool = False

    def __init__(self) -> None:
        self._container = Container()

    def init(self) -> None:
        if self._is_inited and settings.is_debug:
            return

        if self._is_inited and not settings.is_debug:
            raise Exception("Dependencies are already initialized")

        self._prepare_driven_adapters()
        self._prepare_usecases()
        self._is_inited = True

    def resolve[T](self, dependency_type: Type[T]) -> T:
        return self._container.resolve(dependency_type)

    def _prepare_driven_adapters(self) -> None:
        database = SqlDatabaseConnection(
            connection_url=settings.database.get_connection_url(),
            echo=settings.is_debug,
        )

        self._container.register(SqlDatabaseConnection, instance=database)

        self._container.register(UnitOfWork, SqlUnitOfWork)

        blob_storage = S3BlobStorage(
            address=settings.blob_storage.address,
            access_key_id=settings.blob_storage.access_key_id,
            secret_key=settings.blob_storage.secret_key,
            bucket_name=settings.blob_storage.bucket_name,
            use_ssl=settings.blob_storage.use_ssl,
        )

        self._container.register(BlobStorage, instance=blob_storage)

        self._container.register(
            DistributionServiceAdapter,
            DistributionServiceHttpAdapter,
        )

    def _prepare_usecases(self) -> None:
        self._container.register(GetChartUseCase, GetChartUseCaseImpl)

        self._container.register(GetNewAlbumsUseCase, GetNewAlbumsUseCaseImpl)

        self._container.register(
            GetArtistsUseCase,
            GetArtistsUseCaseImpl,
            limit=20,
        )

        self._container.register(
            ListenTrackUseCase,
            ListenTrackUseCaseImpl,
            chunk_size=settings.blob_storage.chunk_size,
        )

        self._container.register(RegisterArtistUseCase, RegisterArtistUseCaseImpl)

        self._container.register(UploadAlbumUseCase, UploadAlbumUseCaseImpl)


container = IoCContainer()
