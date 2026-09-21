# Evaluation Report

## Project

LLM-Powered Embedded-System Log and Fault Extraction Pipeline

## Goal

Convert unstructured embedded-system logs into validated structured fault records.

## Dataset

The evaluation uses 50 synthetic embedded-system logs:

- fault logs with device IDs, firmware versions, error codes, modules, and severity;
- normal logs with no fault information;
- ambiguous reports routed to human review.

Synthetic data was used because no proprietary production device logs were available.

## Pipeline

1. Raw embedded log enters the system.
2. An LLM extracts a structured `EmbeddedFaultRecord`.
3. Pydantic validates the output schema.
4. If extraction fails, the system retries once.
5. If it still fails, the record is marked `needs_review`.
6. Results are compared with labelled expected answers.

## Results

| Method | Status accuracy | Field accuracy |
|---|---:|---:|
| Rule-based baseline | 86.0% | 67.7% |
| LLM pipeline | 100.0% | 83.1% |

The LLM improved field accuracy by 15.4 percentage points.

## Interpretation

The rule-based baseline handled known patterns well but struggled with new device types, modules, and ambiguous reports. The LLM handled all 50 status decisions correctly and improved field extraction accuracy.

The remaining field mismatches show that LLM output should still be validated and reviewed for real production use.

## Safety and Reliability

- API key is stored locally in `.env` and excluded from Git.
- Output is validated with Pydantic.
- Failed LLM requests are retried once.
- Repeated failures are routed to `needs_review`.
- Detailed per-log results are saved in `results/llm_results.json`.