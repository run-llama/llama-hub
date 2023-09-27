.PHONY: format lint

format:
	black .
lint:
	ruff check .
	black --check .
test:
	pytest tests