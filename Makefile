.PHONY: format lint

format:
	black .
	isort .

lint:
	ruff check .
	black --check .
test:
	pytest tests