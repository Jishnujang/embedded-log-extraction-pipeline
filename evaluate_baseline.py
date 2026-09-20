import json
from pathlib import Path

from baseline_extractor import extract_fault_record


DATASET_PATH = Path("data/logs.json")


def evaluate():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    correct_statuses = 0
    correct_fields = 0
    total_fields_checked = 0

    print("Baseline evaluation results\n")

    for log in logs:
        predicted = extract_fault_record(log["raw_log"]).model_dump()
        expected = log["expected"]

        status_correct = (
            predicted["extraction_status"]
            == expected["extraction_status"]
        )

        if status_correct:
            correct_statuses += 1

        print(f"{log['log_id']}:")
        print(f"  Expected status:  {expected['extraction_status']}")
        print(f"  Predicted status: {predicted['extraction_status']}")
        print(f"  Status correct:   {status_correct}")

        for field, expected_value in expected.items():
            if field == "extraction_status":
                continue

            total_fields_checked += 1
            field_correct = predicted[field] == expected_value

            if field_correct:
                correct_fields += 1

            print(f"  {field}: {field_correct}")

        print()

    status_accuracy = correct_statuses / len(logs) * 100

    if total_fields_checked > 0:
        field_accuracy = correct_fields / total_fields_checked * 100
    else:
        field_accuracy = 0

    print("Summary")
    print(f"Status accuracy: {status_accuracy:.1f}%")
    print(f"Field accuracy: {field_accuracy:.1f}%")
    print(f"Correct fields: {correct_fields}/{total_fields_checked}")


if __name__ == "__main__":
    evaluate()