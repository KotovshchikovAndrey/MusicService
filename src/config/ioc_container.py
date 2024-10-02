from punq import Container

from adapters.driven.aiosmtp.smtp_client import AioSmtpClient
from adapters.driven.elasticsearch.track import TrackElasticSearch
from adapters.driven.s3.blob_storage import S3BlobStorage
from adapters.driven.sql.connection import SQLDatabaseConnection
from adapters.driven.sql.unit_of_work import SQLUnitOfWork
from config.settings import settings
from domain.events.event_notifier import EventNotifier
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driven.search_engine import SearchEngine
from domain.ports.driven.smtp_client import SmtpClient
from domain.ports.driving.albums_getting import GetAlbumsUseCase
from domain.ports.driving.album_uploading import UploadAlbumUseCase
from domain.ports.driving.artists_getting import GetArtistsUseCase
from domain.ports.driving.artist_registration import RegisterArtistUseCase
from domain.ports.driving.chart_getting import GetChartUseCase
from domain.ports.driving.jwt_pair_refreshing import RefreshJwtPairUseCase
from domain.ports.driving.sign_in_process import SignInUseCase
from domain.ports.driving.track_listening import ListenTrackUseCase
from domain.ports.driving.user_authentication import AuthenticateUserUseCase
from domain.ports.driving.user_verification import VerifyUserUseCase
from domain.usecases.authenticate_user import AuthenticateUseUseCaseImpl
from domain.usecases.get_albums import GetAlbumsUseCaseImpl
from domain.usecases.get_artists import GetArtistsUseCaseImpl
from domain.usecases.get_chart import GetChartUseCaseImpl
from domain.usecases.listen_track import ListenTrackUseCaseImpl
from domain.usecases.refresh_jwt_pair import RefreshJwtPairUseCaseImpl
from domain.usecases.register_artist import RegisterArtistUseCaseImpl
from domain.usecases.sign_in import SignInUseCaseImpl
from domain.usecases.upload_album import UploadAlbumUseCaseImpl
from domain.usecases.verify_user import VerifyUserUseCaseImpl


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
        self._prepare_events()
        self._prepare_usecases()
        self._is_inited = True

    def resolve[T](self, dependency_type: type[T]) -> T:
        return self._container.resolve(dependency_type)

    def _prepare_driven_adapters(self) -> None:
        database = SQLDatabaseConnection(
            connection_url=settings.database.get_connection_url(),
            echo=settings.is_debug,
        )

        self._container.register(SQLDatabaseConnection, instance=database)

        self._container.register(UnitOfWork, SQLUnitOfWork)

        blob_storage = S3BlobStorage(
            address=settings.blob_storage.address,
            access_key_id=settings.blob_storage.access_key_id,
            secret_key=settings.blob_storage.secret_key,
            bucket_name=settings.blob_storage.bucket_name,
            use_ssl=settings.blob_storage.use_ssl,
        )

        self._container.register(BlobStorage, instance=blob_storage)

        self._container.register(
            FileDownloader,
            type("FileDownloaderImpl", (), {}),
        )

        track_search_engine = TrackElasticSearch(
            address=settings.search_engine.address,
            index=settings.search_engine.track_index,
        )

        self._container.register(SearchEngine, instance=track_search_engine)

        smtp_client = AioSmtpClient(
            host=settings.smtp.host,
            port=settings.smtp.port,
            username=settings.smtp.username,
            password=settings.smtp.password,
            use_tls=settings.smtp.use_tls,
        )

        self._container.register(SmtpClient, instance=smtp_client)

        # broker = RabbitMQMessageBroker(...)

        # self._container.register(MessageBroker, instance=broker)

    def _prepare_events(self) -> None:
        event_notifier = EventNotifier()
        # broker = self._container.resolve(MessageBroker)

        # event_notifier.subscribe(
        #     event=events.UserSignedIn,
        #     handler=SendOTPCodeByEmailHandler(
        #         broker=broker,
        #         email_verification_queue="",
        #     ),
        # )

        self._container.register(EventNotifier, instance=event_notifier)

    def _prepare_usecases(self) -> None:
        self._container.register(GetChartUseCase, GetChartUseCaseImpl)

        self._container.register(GetAlbumsUseCase, GetAlbumsUseCaseImpl)

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

        # self._container.register(SearchTrackUseCase, SearchTrackUseCaseImpl)

        # self._container.register(
        #     SendOTPCodeByEmailUseCase,
        #     SendOTPCodeByEmailUseCaseImpl,
        # )

        self._container.register(SignInUseCase, SignInUseCaseImpl)

        self._container.register(
            VerifyUserUseCase,
            VerifyUserUseCaseImpl,
            access_token_secret=settings.auth.access_token_secret,
            refresh_token_secret=settings.auth.refresh_token_secret,
        )

        self._container.register(
            RefreshJwtPairUseCase,
            RefreshJwtPairUseCaseImpl,
            access_token_secret=settings.auth.access_token_secret,
            refresh_token_secret=settings.auth.refresh_token_secret,
        )

        self._container.register(
            AuthenticateUserUseCase,
            AuthenticateUseUseCaseImpl,
            access_token_secret=settings.auth.access_token_secret,
        )


container = IoCContainer()
