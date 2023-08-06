import logging
import os
from pathlib import Path
from typing import Any, MutableMapping

import toml
from cerberus import Validator


logger = logging.getLogger("kolo")


schema = {
    "filters": {
        "type": "dict",
        "schema": {
            "include_frames": {"type": "list"},
            "ignore_frames": {"type": "list"},
            "ignore_request_paths": {"type": "list"},
        },
    },
    "use_frame_boundaries": {"type": "boolean"},
    "wal_mode": {"type": "boolean"},
}
validator = Validator(schema, allow_unknown=False)


def clear_errors(config: MutableMapping[str, Any], errors) -> None:
    for error in errors:
        key = error.document_path[-1]
        if error.info:
            for info in error.info:
                clear_errors(config[key], info)
        else:
            del config[key]


def load_config_from_toml(path: Path) -> MutableMapping[str, Any]:
    try:
        with open(path) as conf:
            config = toml.load(conf)
    except FileNotFoundError:
        return {}
    if not validator.validate(config):
        logger.warning("Kolo config file has errors: %s", validator.errors)
        clear_errors(config, validator._errors)
    return config


def create_kolo_directory() -> Path:
    """
    Create the kolo directory and contents if they do not exist

    Returns the path to the .kolo directory for convenience.
    """
    kolo_directory = (Path(os.environ.get("KOLO_PATH", ".")) / ".kolo").resolve()
    kolo_directory.mkdir(parents=True, exist_ok=True)
    with open(kolo_directory / ".gitignore", "w") as gitignore:
        gitignore.write("db.sqlite3\n")
        gitignore.write("db.sqlite3-shm\n")
        gitignore.write("db.sqlite3-wal\n")
        gitignore.write(".gitignore\n")
    return kolo_directory
