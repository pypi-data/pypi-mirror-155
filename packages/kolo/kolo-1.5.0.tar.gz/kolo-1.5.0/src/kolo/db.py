import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, MutableMapping, Optional

import toolz

from .config import create_kolo_directory


@contextmanager
def db_cursor(db_path, wal_mode=True):
    """
    Wrap sqlite's cursor for use as a context manager

    Commits all changes if no exception is raised.
    Always closes the cursor/connection after the context manager exits.
    """
    if wal_mode:
        connection = sqlite3.connect(str(db_path), isolation_level=None)
        connection.execute("pragma journal_mode=wal")
    else:
        connection = sqlite3.connect(str(db_path))  # pragma: no cover
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_db_path() -> Path:
    return create_kolo_directory() / "db.sqlite3"


def create_invocations_table(cursor) -> None:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS invocations (
        id text PRIMARY KEY NOT NULL,
        created_at TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')) NOT NULL,
        data text NOT NULL
    );
    """
    create_timestamp_index_query = """
        CREATE INDEX IF NOT EXISTS
        idx_invocations_created_at
        ON invocations (created_at);
        """

    cursor.execute(create_table_query)
    cursor.execute(create_timestamp_index_query)


def create_config_table(cursor) -> None:
    create_config_query = """
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        source text NOT NULL UNIQUE,
        last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        data text NOT NULL
    );
    """
    cursor.execute(create_config_query)


def save_config_to_db(cursor, config) -> None:
    save_config_query = "INSERT OR REPLACE INTO config(source, data) VALUES(?,?);"
    cursor.execute(save_config_query, ("python", json.dumps(config)))


def merge_or_last(args):
    if all(isinstance(arg, dict) for arg in args):
        return toolz.merge(*args)
    return args[-1]


def load_config_from_db(
    db_path: Path, toml_config: Optional[MutableMapping[str, Any]] = None
) -> MutableMapping[str, Any]:
    """
    Load the kolo config from sqlite

    We return the config defined by VSCode, if available, and fallback
    to the config we saved to the db from `.kolo/conf.toml`.
    """
    if toml_config is None:
        toml_config = {}

    wal_mode = toml_config.get("wal_mode", True)

    load_config_query = "SELECT source, data from config;"
    try:
        with db_cursor(db_path, wal_mode) as cursor:
            cursor.execute(load_config_query)
            rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        if e.args[0] != "no such table: config":
            raise  # pragma: no cover
        setup_db(toml_config)
        return toml_config

    data = {key: json.loads(value) for key, value in rows}
    python_config = data["python"]
    vscode_config = data.get("vscode", {})
    return toolz.merge_with(merge_or_last, python_config, vscode_config)


def setup_db(config: Optional[MutableMapping[str, Any]] = None) -> Path:
    if config is None:
        config = {}
    db_path = get_db_path()

    wal_mode = config.get("wal_mode", True)

    with db_cursor(db_path, wal_mode) as cursor:
        create_invocations_table(cursor)
        create_config_table(cursor)
        save_config_to_db(cursor, config)

    return db_path


def save_invocation_in_sqlite(
    db_path: Path, invocation_id: str, json_string: str, wal_mode: bool = True
) -> None:
    insert_sql = """
        INSERT OR IGNORE INTO invocations(id, data)
        VALUES(?,?)
        """

    # We can't reuse a connection
    # because we're in a new thread
    with db_cursor(db_path, wal_mode) as cursor:
        cursor.execute(insert_sql, (invocation_id, json_string))
