from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_PATH = BACKEND_ROOT / "runtime" / "sentinel.db"
DEFAULT_DATABASE_URL = "sqlite+pysqlite:///" + DEFAULT_SQLITE_PATH.as_posix()


def get_database_url() -> str:
    return os.environ.get("SENTINEL_DATABASE_URL", DEFAULT_DATABASE_URL)


def ensure_database_parent(database_url: str) -> None:
    """Create the parent directory for file-backed SQLite URLs."""
    prefix = "sqlite+pysqlite:///"

    if not database_url.startswith(prefix):
        return

    raw = database_url[len(prefix):]

    if raw in ("", ":memory:"):
        return

    path = Path(raw)

    if not path.is_absolute():
        path = Path.cwd() / path

    path.parent.mkdir(parents=True, exist_ok=True)


def build_engine(database_url: str | None = None) -> Engine:
    url = database_url or get_database_url()
    ensure_database_parent(url)

    kwargs: dict = {
        "pool_pre_ping": True,
        "future": True,
    }

    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}

    return create_engine(url, **kwargs)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return build_engine()


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    return build_session_factory(get_engine())
