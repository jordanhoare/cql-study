import logging

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.connection import log as cql_logger

from .config import get_settings


def set_logging() -> None:
    cql_logger.setLevel(logging.DEBUG)
    _formatter = logging.Formatter("%(message)s")
    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)
    cql_logger.addHandler(_handler)


def sync_db() -> None:
    settings = get_settings()
    auth = PlainTextAuthProvider(username=settings.CASSANDRA_USER, password=settings.CASSANDRA_PWD)
    cluster = Cluster(
        contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth
    )
    session = cluster.connect()

    rows = session.execute("SELECT * FROM system_schema.keyspaces")
    if settings.CASSANDRA_KEYSPACE in [row[0] for row in rows]:
        cql_logger.info("Dropping existing keyspace...")
        session.execute(f"DROP KEYSPACE {settings.CASSANDRA_KEYSPACE}")

    session.execute(
        "CREATE KEYSPACE %s WITH replication = "
        "{'class': 'SimpleStrategy', 'replication_factor': '1'} "
        "AND durable_writes = true;" % settings.CASSANDRA_KEYSPACE
    )

    session.set_keyspace(settings.CASSANDRA_KEYSPACE)
    connection.set_session(session)


def main() -> None:
    set_logging()
    sync_db()


if __name__ == "__main__":
    main()
