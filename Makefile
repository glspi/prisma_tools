lint:
	python -m isort .
	python -m black .
	python -m pylama .
	python -m pydocstyle .
	python -m mypy --strict --no-warn-return-any prisma_tools/

test:
	python -m pytest tests/