.PHONY: format lint

format:
	black .
	isort .

test:
	pytest tests