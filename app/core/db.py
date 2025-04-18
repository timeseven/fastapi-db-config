from sqlalchemy import MetaData
from databases import Database, DatabaseURL

from app.core.config import settings

metadata = MetaData()


class DbConfig:
    def __init__(
        self,
        url: DatabaseURL | str,
        min_size: int,
        max_size: int,
        timeout: float,
        max_inactive_connection_lifetime: float,
    ):
        """
        Initialize the database parameters

        Args:
            - url (str): Database connection string
            The keyword arguments below are used for postgresql.
            Available keyword arguments may differ for other databases.
            - min_size (int): Minimum number of connections
            - max_size (int): Maximum number of connections
            - timeout (float): Connection timeout in seconds
            - max_inactive_connection_lifetime (float): Maximum inactive connection lifetime in seconds
        """
        self.db_pool = Database(
            url,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        )

    async def connect(self):
        """
        Connect to the database
        """
        await self.db_pool.connect()

    async def disconnect(self):
        """
        Disconnect from the database
        """
        await self.db_pool.disconnect()


db_conf = DbConfig(
    url=settings.ASYNC_DATABASE_URL,
    min_size=settings.DATABASE_MIN_CONNECTIONS,
    max_size=settings.DATABASE_MAX_CONNECTIONS,
    timeout=settings.DATABASE_TIMEOUT,
    max_inactive_connection_lifetime=settings.DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME,
)
