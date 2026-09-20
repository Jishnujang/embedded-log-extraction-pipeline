


from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


class EmbeddedFaultRecord(BaseModel):
    """Validated information extracted from one embedded-system log."""

    extraction_status: Literal[
        "extracted",
        "no_relevant_fields",
        "needs_review",
    ] = Field(
        description="Whether a useful fault record was found."
    )

    device_id: Optional[str] = None
    firmware_version: Optional[str] = None
    timestamp: Optional[str] = None
    error_code: Optional[str] = None
    affected_module: Optional[str] = None
    severity: Optional[Literal["low", "medium", "high", "critical"]] = None
    summary: Optional[str] = None

    @model_validator(mode="after")
    def validate_extracted_record(self):
        if self.extraction_status == "extracted" and not (
            self.device_id or self.error_code or self.affected_module
        ):
            raise ValueError(
                "An extracted record needs a device ID, error code, "
                "or affected module."
            )
        return self