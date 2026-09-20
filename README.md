# LLM-Powered Embedded-System Log and Fault Extraction Pipeline

A Python project that converts unstructured embedded-system logs into validated fault records.

## Current features

- Typed fault-record schema using Pydantic
- Validation and explicit failure handling
- Dataset of embedded logs with expected answers
- Rule-based baseline extractor
- Evaluation script for status and field accuracy

## Project structure

- `models.py` — defines the validated fault schema
- `baseline_extractor.py` — extracts fault fields using rules
- `evaluate_baseline.py` — measures baseline accuracy
- `data/logs.json` — labelled embedded-log dataset

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pydantic python-dotenv openai