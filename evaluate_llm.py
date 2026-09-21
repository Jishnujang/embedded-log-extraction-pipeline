import json
from pathlib import Path

from llm_extractor import extract_with_llm


DATASET_PATH = Path("data/logs.json")
RESULTS_PATH = Path("results/llm_results.json")


def evaluate():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    RESULTS_PATH.parent.mkdir(exist_ok=True)

    correct_statuses = 0
    correct_fields = 0
    total_fields_checked = 0
    all_results = []

    for log in logs:
        expected = log["expected"]
        predicted = extract_with_llm(log["raw_log"]).model_dump()

        status_correct = (
            predicted["extraction_status"]
            == expected["extraction_status"]
        )

        if status_correct:
            correct_statuses += 1

        for field, expected_value in expected.items():
            if field == "extraction_status":
                continue

            total_fields_checked += 1

            if predicted[field] == expected_value:
                correct_fields += 1

        all_results.append(
            {
                "log_id": log["log_id"],
                "raw_log": log["raw_log"],
                "expected": expected,
                "predicted": predicted,
                "status_correct": status_correct,
            }
        )

        result_word = "PASS" if status_correct else "CHECK"
        print(f"{result_word}  {log['log_id']}")

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(all_results, file, indent=2)

    status_accuracy = correct_statuses / len(logs) * 100
    field_accuracy = correct_fields / total_fields_checked * 100

    print("\nLLM evaluation summary")
    print(f"Logs tested: {len(logs)}")
    print(f"Status accuracy: {status_accuracy:.1f}%")
    print(f"Field accuracy: {field_accuracy:.1f}%")
    print(f"Correct fields: {correct_fields}/{total_fields_checked}")
    print(f"Saved detailed results to: {RESULTS_PATH}")


if __name__ == "__main__":
    evaluate()