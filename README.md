# LLM-Powered Embedded-System Log and Fault Extraction Pipeline

A Python project that converts unstructured embedded-system logs into validated fault records using an LLM.

## Problem

Embedded logs are often difficult to search and analyse manually. This pipeline extracts useful fault information—such as device ID, firmware version, error code, affected module, and severity—from raw log text.

## Features

- Pydantic typed schema for fault records
- LLM-based structured extraction using OpenAI
- Rule-based baseline for comparison
- Retry once when LLM extraction fails
- `needs_review` failure route after repeated failure
- Dataset of 50 labelled embedded-system logs
- Automated evaluation and saved detailed results
- API key excluded from GitHub with `.gitignore`

## Results

| Method | Status accuracy | Field accuracy |
|---|---:|---:|
| Rule-based baseline | 86.0% | 67.7% |
| LLM pipeline | 100.0% | 83.1% |

See [Report.md](Report.md) for the evaluation details.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt