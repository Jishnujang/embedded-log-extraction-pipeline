import os
import re
import time

from dotenv import load_dotenv
from openai import OpenAI

from models import EmbeddedFaultRecord


load_dotenv()

MODEL_NAME = "gpt-5.6-luna"

SYSTEM_PROMPT = """
You extract embedded-system fault information from raw log text.

Rules:
- Extract only information supported by the log.
- Use "extracted" when a real fault is identified.
- Use "no_relevant_fields" for normal or successful status logs.
- Use "needs_review" when a possible fault is described but key details
  are missing or unclear.
- Write affected_module in lower_snake_case, for example
  temperature_sensor or can_bus.
- Infer severity as low, medium, high, or critical from the likely impact:
  low = minor UI/configuration issue;
  medium = recoverable communication or sensor issue;
  high = important device function affected;
  critical = power, watchdog, or safety-related failure.
- Never invent device IDs, error codes, firmware versions, or timestamps.
- Keep summary short and factual.
"""


def normalise_record(record: EmbeddedFaultRecord) -> EmbeddedFaultRecord:
    """Make module names consistent for evaluation."""

    data = record.model_dump()

    if data["affected_module"]:
        module = data["affected_module"].lower()
        module = re.sub(r"[^a-z0-9]+", "_", module).strip("_")
        data["affected_module"] = module

    return EmbeddedFaultRecord(**data)


def extract_with_llm(
    raw_log: str,
    max_attempts: int = 2,
) -> EmbeddedFaultRecord:
    """Extract a validated record, retrying once before requesting review."""

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to the .env file."
        )

    client = OpenAI()
    last_error = None

    for attempt in range(max_attempts):
        try:
            response = client.responses.parse(
                model=MODEL_NAME,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": raw_log},
                ],
                text_format=EmbeddedFaultRecord,
            )

            if response.output_parsed is None:
                raise RuntimeError(
                    "The model did not return a structured response."
                )

            return normalise_record(response.output_parsed)

        except Exception as error:
            last_error = error

            if attempt < max_attempts - 1:
                time.sleep(1)

    return EmbeddedFaultRecord(
        extraction_status="needs_review",
        summary=(
            "Automatic review required because LLM extraction failed: "
            f"{type(last_error).__name__}"
        ),
    )