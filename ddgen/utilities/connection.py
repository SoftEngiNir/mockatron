from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import NamedTuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConnectionDetails(NamedTuple):
    username: str
    host: str | None = 'localhost'
    port: int | None = 5432
    dbname: str | None = 'postgres'
    password: str | None = 'admin'
    schema: str | None = ''


def create_engine_postgres(cnxn: ConnectionDetails) -> Engine:
    connection_string = f'postgresql://{cnxn.username}:{cnxn.password}@{cnxn.host}:{cnxn.port}/{cnxn.dbname}'
    return create_engine(connection_string)


@contextmanager
def session_context(engine) -> Generator[Session, None, None]:
    session = sessionmaker(engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


TEST_DB_CNXT = ConnectionDetails(
    username='postgres',
    host='localhost',
    port=26552,
    dbname='postgres',
    password='test',
)

TEST_ENGINE = create_engine_postgres(TEST_DB_CNXT)
