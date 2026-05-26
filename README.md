# AI Safe Shopping URL Classifier

A machine-learning pipeline that classifies shopping URLs as **safe** vs **suspicious** and assesses whether a domain is a *legitimate retailer* vs a likely scam — designed to help users avoid phishing and fraudulent e-commerce sites.

## Two-stage classifier

1. **`shopping_classifier.py`** — decides whether a URL is a shopping page at all.
2. **`trust_classifier.py`** — for shopping pages, predicts whether the seller is trustworthy.

`main.py` and `main_commented.py` wire the two stages together into a single end-to-end script.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

`main_commented.py` is an annotated walkthrough of the same flow — useful if you want to read the pipeline step by step.

## Inputs / outputs

- **Input:** a URL or a list of URLs
- **Output:** classification labels (shopping / not shopping; safe / risky) and supporting features

`search_results.json` ships a sample of crawled search-engine results used during evaluation.

## Project context

- Final report: `Final Report.docx` — full write-up of methodology, dataset construction, feature engineering, and evaluation results.
- Built as part of an AI / ML coursework + portfolio project.

## Files

```
AI_Safe_Shopping_URL_Classifier/
├── main.py                 # End-to-end entry point
├── main_commented.py       # Annotated walkthrough
├── shopping_classifier.py  # Stage 1: shopping vs not
├── trust_classifier.py     # Stage 2: safe vs risky
├── search_results.json     # Sample data
├── Final Report.docx       # Methodology + results
└── requirements.txt
```

## License

Shared for portfolio / educational review. Not a substitute for a hardened phishing-detection service.
