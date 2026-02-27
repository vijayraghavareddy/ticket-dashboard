import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app


def main() -> None:
    output_path = PROJECT_ROOT / "openapi.json"
    schema = app.openapi()
    output_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OpenAPI schema exported to {output_path}")


if __name__ == "__main__":
    main()
