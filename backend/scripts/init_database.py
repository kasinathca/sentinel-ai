from __future__ import annotations

from pathlib import Path
import subprocess
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.seed import seed_frozen_violence_model
from app.db.session import (
    ensure_database_parent,
    get_database_url,
    get_session_factory,
)


def main() -> int:
    database_url = get_database_url()
    ensure_database_parent(database_url)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            str(BACKEND_ROOT / "alembic.ini"),
            "upgrade",
            "head",
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )

    seed_frozen_violence_model(get_session_factory())

    print("Sentinel database schema is at Alembic head.")
    print("Frozen violence model/version/global policy seed is present.")
    print(f"Database URL: {database_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
