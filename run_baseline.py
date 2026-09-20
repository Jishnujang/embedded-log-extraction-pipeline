from baseline_extractor import extract_fault_record


sample_log = (
    "[10:42:18] ESP32-001 FW:1.4.2 "
    "ERROR E104: temperature sensor timeout."
)

result = extract_fault_record(sample_log)

print(result.model_dump_json(indent=2))