import sys
from runpy import run_module, run_path

import click

from .config import create_kolo_directory, load_config_from_toml
from .db import load_config_from_db, setup_db
from .profiler import KoloProfiler


def get_profiler() -> KoloProfiler:
    kolo_directory = create_kolo_directory()
    config = load_config_from_toml(kolo_directory / "config.toml")
    db_path = setup_db(config)
    db_config = load_config_from_db(db_path)
    filter_config = db_config.get("filters", {})

    return KoloProfiler(
        db_path,
        include_frames=filter_config.get("include_frames", []),
        ignore_frames=filter_config.get("ignore_frames", []),
        config=db_config,
    )


def profile_module(profiler: KoloProfiler, module_name: str):
    with profiler:
        run_module(module_name, run_name="__main__", alter_sys=True)


def profile_path(profiler: KoloProfiler, path: str):
    with profiler:
        run_path(path, run_name="__main__")


@click.group()
def cli():
    """Base for all kolo command line commands"""

    # Ensure the current working directory is on the path.
    # Important when running the `kolo` script installed by setuptools.
    # Not really necessary when using `python -m kolo`, but doesn't hurt.
    # Note, we use 1, not 0: https://stackoverflow.com/q/10095037
    # This probably doesn't matter for our use case, but it doesn't hurt.
    sys.path.insert(1, ".")


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("path")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(path, args):
    """
    Profile python code using kolo.

    PATH is the path to the python file or module being profiled.
    """
    if path == "python":
        path, *args = args
        if path == "-m":
            path, *args = args
            module = True
        else:
            module = False
    elif path.endswith(".py"):
        module = False
    else:
        module = True

    # Monkeypatch sys.argv, so the profiled code doesn't get confused
    # Without this, the profiled code would see extra args it doesn't
    # know how to handle.
    sys.argv = [path, *args]

    profiler = get_profiler()
    try:
        if module:
            profile_module(profiler, path)
        else:
            profile_path(profiler, path)
    finally:
        profiler.save_request_in_db()


@cli.command()
def config():
    """Display kolo's configuration."""
    from pprint import pformat

    kolo_directory = create_kolo_directory()
    config_file = kolo_directory / "config.toml"
    config = load_config_from_toml(config_file)
    db_path = setup_db(config)
    db_config = load_config_from_db(db_path)

    click.echo("Kolo config from VSCode (takes precedence)")
    click.echo(pformat(db_config))
    click.echo(f"Kolo config from {config_file}")
    click.echo(pformat(config))


if __name__ == "__main__":
    cli()  # pragma: no cover
