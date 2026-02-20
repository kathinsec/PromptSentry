# PromptSentry

PromptSentry is a lightweight heuristic detection tool that identifies potential prompt injection patterns in LLM interaction logs.

It demonstrates practical defensive techniques used in AI-integrated systems, including deterministic rule evaluation, additive risk scoring, and explainable findings.

---

## Key Capabilities

• Heuristic prompt-injection detection  
• Regex-based rule engine  
• Additive severity scoring model  
• Risk classification (LOW / MEDIUM / HIGH)  
• Evidence reporting (matched substrings)  
• Multi-format ingestion (JSONL, CSV)  
• Structured findings export (CSV)  

---

## Installation

Clone the repository and install in editable mode:

git clone https://github.com/kathinsec/PromptSentry.git
cd PromptSentry
python3 -m pip install -e .

---

## Quick Demo

Run PromptSentry on the included sample dataset:

promptsentry sample_data/sample.jsonl --field content --min-score 8

The tool evaluates each record, assigns a risk score, and prints triggered detection rules along with supporting evidence.

---

## CSV Analysis Example

promptsentry sample_data/sample.csv --field content --min-score 8

---

## Exporting Findings

promptsentry sample_data/sample.csv --field content --min-score 8 --out findings.csv

---

## Detection Model

PromptSentry uses deterministic heuristics rather than machine learning.

Each rule:

• Encodes a suspicious linguistic pattern  
• Carries a severity weight  
• Contributes to an aggregate score  

Multiple weak signals combine into stronger alerts via additive scoring.

---

## Educational Objective

This project is intentionally minimal and designed to illustrate:

• Prompt injection attack patterns  
• Defensive heuristic strategies  
• Explainable security tool design  
• Practical Python CLI architecture  

---

## Disclaimer

PromptSentry is an educational project and not a production security system.