# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

__version__ = "3.0.0"

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool
from .json_encoder import _json_encoder
from minty import Base
from minty.cqrs import MiddlewareBase, QueryMiddleware


def DatabaseTransactionMiddleware(infrastructure_name):
    class _DatabaseTransactionMiddleware(MiddlewareBase):
        def __call__(self, func):
            session = self.infrastructure_factory.get_infrastructure(
                context=self.context, infrastructure_name=infrastructure_name
            )
            try:
                func()
                session.commit()
            except Exception as e:
                self.logger.error(
                    f"Exception during database transaction; rolling back: {e}",
                    exc_info=True,
                )
                session.rollback()
                raise e

    return _DatabaseTransactionMiddleware


def DatabaseTransactionQueryMiddleware(infrastructure_name):
    """Database transaction middleware factory for queries.

    Query middleware is slightly different from command middleware, because
    queries don't have events, and need to return a value."""

    class _DatabaseTransactionQueryMiddleware(QueryMiddleware):
        def __call__(self, func):
            session = self.infrastructure_factory.get_infrastructure(
                context=self.context, infrastructure_name=infrastructure_name
            )
            try:
                return_value = func()
            except Exception as e:
                self.logger.error(
                    f"Exception during database query transaction; rolling back: {e}"
                )
                raise e
            finally:
                # Queries shouldn't write to the database
                session.rollback()

            return return_value

    return _DatabaseTransactionQueryMiddleware


class DatabaseSessionInfrastructure(Base):
    """Infrastructure for handling SQLAlchemy sessions"""

    def __init__(self, prefix: str):
        """Initialize a new database session infrastructure factory

        :param prefix: Prefix to use for sqlalchemy.engine_from_config, which
            uses it to retrieve a specific configuration from a configuration.
        :type prefix: str
        """

        self.prefix = prefix

    def __call__(self, config: dict):
        """Create a database session from the specified configuration

        Uses `sqlalchemy.engine_from_config` and the prefix configured in
        `__init__` to create a `sqlalchemy.Session`.

        :param config: Configuration
        :type config: dict
        :return: A SQLAlchemy session, bound to an engine that's been set up
            according to `config`
        :rtype: sqlalchemy.Session
        """

        engine = sqlalchemy.engine_from_config(
            configuration=config,
            prefix=self.prefix,
            poolclass=sqlalchemy.pool.NullPool,
            json_serializer=_json_encoder,
        )

        timer = self.statsd.get_timer("database_connect_duration")
        with timer.time():
            connection = engine.connect()

        self.statsd.get_counter("database_connect_number").increment()

        session = sqlalchemy.orm.Session(bind=connection)
        return session

    def clean_up(self, session):
        """Close the SQLAlchemy Session"""

        session.close()
