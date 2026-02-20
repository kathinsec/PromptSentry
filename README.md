# PromptSentry

PromptSentry is a lightweight heuristic detector for identifying potential prompt injection patterns in LLM interaction logs.

## Features

- Heuristic prompt-injection detection
- Regex-driven rule engine
- Additive severity scoring
- Risk categories: LOW / MEDIUM / HIGH
- JSONL and CSV input support
- CSV findings export

## Installation

git clone https://github.com/kathinsec/PromptSentry.git
cd PromptSentry
python3 -m pip install -e .

## Demo

promptsentry sample_data/sample.jsonl --field content --min-score 8

## CSV Export

promptsentry sample_data/sample.csv --field content --min-score 8 --out findings.csv

## Disclaimer

Educational project. Not a production security system.