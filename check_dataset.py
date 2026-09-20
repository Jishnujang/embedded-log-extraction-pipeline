import json
from pathlib import Path

from pydantic import ValidationError

from models import EmbeddedFaultRecord


DATASET_PATH = Path("data/logs.json")


def load_and_validate_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    valid_records = 0
    invalid_records = 0

    for log in logs:
        try:
            record = EmbeddedFaultRecord(**log["expected"])
            valid_records += 1
            print(f"PASS  {log['log_id']} -> {record.extraction_status}")

        except ValidationError as error:
            invalid_records += 1
            print(f"FAIL  {log['log_id']}")
            print(error)

    print("\nDataset validation summary")
    print(f"Total logs: {len(logs)}")
    print(f"Valid expected records: {valid_records}")
    print(f"Invalid expected records: {invalid_records}")


if __name__ == "__main__":
    load_and_validate_dataset()