import subprocess
from typing import Optional


def get_current_commit_sha() -> Optional[str]:
    try:
        git_process = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        return None

    if git_process.stderr:
        return None  # pragma: no cover
    return git_process.stdout.decode("utf-8").strip()


COMMIT_SHA = get_current_commit_sha()
