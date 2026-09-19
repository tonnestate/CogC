.PHONY: install sync check-sync test eval example verify

install:
	python -m pip install -e ".[dev]"

sync:
	python tools/sync_skill.py

check-sync:
	python tools/sync_skill.py --check

test:
	pytest

eval:
	python evals/run_offline_eval.py

example:
	cogc compile --input examples/repository-analysis.json --profile qwen-4b --format text --receipt

verify: check-sync test eval
	cogc --version
	python skill/cogc/scripts/compile_context.py --input examples/repository-analysis.json --profile qwen-4b --format json > /dev/null
