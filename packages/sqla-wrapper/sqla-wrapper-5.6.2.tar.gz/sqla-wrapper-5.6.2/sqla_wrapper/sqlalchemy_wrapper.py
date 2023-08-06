from typing import Any, Dict, Optional

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .base_model import BaseModel
from .session import PatchedScopedSession, Session


__all__ = ("SQLAlchemy", "TestTransaction", "DeclarativeMeta")


class SQLAlchemy:
    """Create a SQLAlchemy connection

    This class creates an engine, a base class for your models, and a scoped session.

    The string form of the URL is
    `dialect[+driver]://user:password@host/dbname[?key=value..]`,
    where dialect is a database name such as mysql, postgresql, etc., and driver the
    name of a DBAPI, such as psycopg2, pyodbc, etc.

    Instead of the connection URL you can also specify dialect (plus optional driver),
    user, password, host, port, and database name as separate arguments.

    Please review the
    [Database URLs](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
    section of the SQLAlchemy documentation, for general guidelines in composing
    URL strings. In particular, special characters, such as those often part of
    passwords, must be URL-encoded to be properly parsed.

    Example:

    ```python
    db = SQLAlchemy(database_uri)
    # or SQLAlchemy(dialect=, name= [, user=] [, password=] [, host=] [, port=])

    class Base(db.Model):
        pass

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        login = Column(String(80), unique=True)
        deleted = Column(DateTime)

    ```

    """

    def __init__(
        self,
        url: Optional[str] = None,
        *,
        dialect: str = "sqlite",
        name: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        engine_options: Optional[Dict[str, Any]] = None,
        session_options: Optional[Dict[str, Any]] = None,
        base_model_class: Any = BaseModel,
        base_model_metaclass: Any = DeclarativeMeta,
    ) -> None:
        self.url = url or self._make_url(
            dialect=dialect,
            host=host,
            name=name,
            user=user,
            password=password,
            port=port,
        )
        engine_options = engine_options or {}
        engine_options.setdefault("future", True)
        self.engine = sqlalchemy.create_engine(self.url, **engine_options)

        self.registry = sqlalchemy.orm.registry()
        self.Model = self.registry.generate_base(
            cls=base_model_class,
            name="Model",
            metaclass=base_model_metaclass
        )

        session_options = session_options or {}
        session_options.setdefault("class_", Session)
        session_options.setdefault("bind", self.engine)
        session_options.setdefault("future", True)
        self.session_class = session_options["class_"]
        self.Session = sqlalchemy.orm.sessionmaker(**session_options)
        self.s = PatchedScopedSession(self.Session)

        self._include_sqlalchemy()

    def create_all(self, **kwargs) -> None:
        """Creates all the tables of the models registered so far.

        Only tables that do not already exist are created. Existing tables are
        not modified.
        """
        kwargs.setdefault("bind", self.engine)
        self.registry.metadata.create_all(**kwargs)

    def drop_all(self, **kwargs) -> None:
        """Drop all the database tables.

        Note that this is a destructive operation; data stored in the
        database will be deleted when this method is called.
        """
        kwargs.setdefault("bind", self.engine)
        self.registry.metadata.drop_all(**kwargs)

    def test_transaction(self, savepoint: bool = False) -> "TestTransaction":
        return TestTransaction(self, savepoint=savepoint)

    def _include_sqlalchemy(self):
        skip = (
            "create_engine",
            "create_session",
            "declarative_base",
            "scoped_session",
            "sessionmaker",
        )
        for module in sqlalchemy, sqlalchemy.orm:
            for key in module.__all__:
                if key in skip or hasattr(self, key):
                    continue
                setattr(self, key, getattr(module, key))
        self.event = sqlalchemy.event

    def _make_url(
        self,
        dialect: str,
        *,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        name: Optional[str] = None,
    ) -> str:
        url_parts = [f"{dialect}://"]
        if user:
            url_parts.append(user)
            if password:
                url_parts.append(f":{password}")
            url_parts.append("@")

        if not host and not dialect.startswith("sqlite"):
            host = "127.0.0.1"

        if host:
            url_parts.append(f"{host}")
            if port:
                url_parts.append(f":{port}")

        if name:
            url_parts.append(f"/{name}")
        return "".join(url_parts)

    def __repr__(self) -> str:
        return f"<SQLAlchemy('{self.url}')>"


class TestTransaction:
    """Helper for building sessions that rollback everyting at the end.

    See ["Joining a Session into an External Transaction"](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#session-external-transaction)
    in the SQLAlchemy documentation.
    """
    def __init__(self, db: SQLAlchemy, savepoint: bool = False) -> None:
        self.connection = db.engine.connect()
        self.trans = self.connection.begin()
        self.session = db.Session(bind=self.connection)
        db.s.registry.set(self.session)

        if savepoint:  # pragma: no branch
            # if the database supports SAVEPOINT (SQLite needs a
            # special config for this to work), starting a savepoint
            # will allow tests to also use rollback within tests
            self.nested = self.connection.begin_nested()

            @sqlalchemy.event.listens_for(self.session, "after_transaction_end")
            def end_savepoint(session, transaction):
                if not self.nested.is_active:
                    self.nested = self.connection.begin_nested()

    def close(self) -> None:
        self.session.close()
        self.trans.rollback()
        self.connection.close()

    def __enter__(self):  # pragma: no cover
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # pragma: no cover
        self.close()
