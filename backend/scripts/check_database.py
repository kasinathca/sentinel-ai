from __future__ import annotations

import json
from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.readiness import inspect_database_readiness  # noqa: E402
from app.db.session import get_engine  # noqa: E402


def main() -> int:
    result = inspect_database_readiness(get_engine())
    print(json.dumps(result.to_public_dict(), indent=2))
    return 0 if result.ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
