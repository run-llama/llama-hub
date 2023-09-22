.PHONY: format lint

format:
	black .
	isort .

lint:
	mypy .
	black --check .
test:
	pytest tests