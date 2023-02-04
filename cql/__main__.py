import logging

from cassandra.cqlengine import connection
from cassandra.cqlengine.connection import log as cql_logger

from .db import create_session


def set_logging() -> None:
    cql_logger.setLevel(logging.DEBUG)
    _formatter = logging.Formatter("%(message)s")
    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)
    cql_logger.addHandler(_handler)


def sync_db() -> None:
    """Initialise a session with Cassandra and set keyspaces to system defaults"""

    session = create_session()

    # Remove all keyspaces other than system defaults
    rows = session.execute("SELECT * FROM system_schema.keyspaces")
    system_keyspaces = [
        "system_auth",
        "system_schema",
        "system_distributed",
        "system",
        "system_traces",
    ]
    for row in rows:
        if row[0] not in system_keyspaces:
            session.execute(f"DROP KEYSPACE {row[0]}")
            cql_logger.info(f"Dropped existing keyspace {row[0]}...")

    connection.set_session(session)


def main() -> None:
    set_logging()
    sync_db()


if __name__ == "__main__":
    main()
