format:
	python -m black . --exclude="docs"
	python -m isort . --skip "docs"

lint:
	python -m black --check --diff . --exclude="docs"
	python -m isort --check --diff . --skip "docs"

test:
	pytest

build:
	rm -f ./dist/*.whl
	flit build --format wheel

.PHONY: lint format test

publish:
	./dist/publish.sh
