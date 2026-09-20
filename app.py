from models import EmbeddedFaultRecord


valid_fault = EmbeddedFaultRecord(
    extraction_status="extracted",
    device_id="ESP32-001",
    firmware_version="1.4.2",
    error_code="E104",
    affected_module="temperature_sensor",
    severity="high",
    summary="Temperature sensor did not respond before timeout.",
)

print(valid_fault.model_dump_json(indent=2))
try:
    invalid_fault = EmbeddedFaultRecord(
        extraction_status="extracted",
        summary="A problem occurred.",
    )
except ValueError as error:
    print("\nInvalid record rejected:")
    print(error)