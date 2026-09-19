.PHONY: install test eval example

install:
	python -m pip install -e ".[dev]"

test:
	pytest

eval:
	python evals/run_offline_eval.py

example:
	cogc compile --input examples/repository-analysis.json --profile qwen-4b --format text --receipt
