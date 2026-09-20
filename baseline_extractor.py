import re

from models import EmbeddedFaultRecord


ERROR_SEVERITY = {
    "E104": "high",
    "E210": "medium",
    "E305": "high",
    "E401": "medium",
    "E502": "high",
}

MODULE_PATTERNS = {
    "temperature_sensor": r"temperature sensor",
    "uart": r"uart",
    "pressure_sensor": r"pressure sensor",
    "gps_module": r"gps module",
    "battery": r"battery",
    "i2c": r"i2c",
}


def extract_fault_record(raw_log: str) -> EmbeddedFaultRecord:
    """Extract embedded fault details from raw log text using simple rules."""

    device_match = re.search(r"\b[A-Z0-9]+(?:-[A-Z0-9]+)+\b", raw_log)
    firmware_match = re.search(
        r"(?:FW:|firmware\s)([0-9]+\.[0-9]+\.[0-9]+)",
        raw_log,
        re.IGNORECASE,
    )
    error_match = re.search(r"\bE\d{3}\b", raw_log)

    device_id = device_match.group(0) if device_match else None
    firmware_version = firmware_match.group(1) if firmware_match else None
    error_code = error_match.group(0) if error_match else None

    affected_module = None
    for module, pattern in MODULE_PATTERNS.items():
        if re.search(pattern, raw_log, re.IGNORECASE):
            affected_module = module
            break

    severity = ERROR_SEVERITY.get(error_code) if error_code else None

    if error_code or affected_module:
        status = "extracted"
    elif re.search(r"issue|problem|stops responding|error", raw_log, re.IGNORECASE):
        status = "needs_review"
    else:
        status = "no_relevant_fields"

    return EmbeddedFaultRecord(
        extraction_status=status,
        device_id=device_id,
        firmware_version=firmware_version,
        error_code=error_code,
        affected_module=affected_module,
        severity=severity,
        summary=raw_log,
    )