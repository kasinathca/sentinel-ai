from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.readiness import inspect_database_readiness  # noqa: E402
from app.db.seed import seed_frozen_violence_model  # noqa: E402
from app.db.session import (  # noqa: E402
    ensure_database_parent,
    get_database_url,
    get_engine,
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

    readiness = inspect_database_readiness(get_engine())
    if not readiness.ready:
        print(
            "Database initialization completed but readiness verification failed.",
            file=sys.stderr,
        )
        print(json.dumps(readiness.to_public_dict(), indent=2), file=sys.stderr)
        return 3

    print("Sentinel database schema is at the expected Alembic head.")
    print("Frozen violence model/version/global policy seed is present.")
    print("Database readiness verification: PASS")
    print(f"Database URL: {database_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
