from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from .config import get_settings


def create_session():
    settings = get_settings()
    auth = PlainTextAuthProvider(username=settings.CASSANDRA_USER, password=settings.CASSANDRA_PWD)
    cluster = Cluster(
        contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth
    )
    return cluster.connect()
