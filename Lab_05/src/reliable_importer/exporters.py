import json
from dataclasses import asdict
from pathlib import Path
from reliable_importer.models import BankingEntry


def export_entries_atomically(entries: list[BankingEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = output_path.with_suffix(".tmp")

    payload = [asdict(e) for e in entries]

    # Write first to a temporary file, then perform an atomic rename to prevent corrupting data mid-flight
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    temp_file.replace(output_path)
