import json
from pathlib import Path

def get(
    file_path: str | Path,
    key: str
) -> str | None:
    with Path(file_path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key)