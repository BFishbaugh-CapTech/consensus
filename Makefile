.PHONY: help install upgrade freeze run test coverage format lint fix typecheck check clean

help:
	@echo "Consensus Commands"
	@echo ""
	@echo "make run        - Start FastAPI"
	@echo "make test       - Run tests"
	@echo "make format     - Format code"
	@echo "make lint       - Run Ruff"
	@echo "make fix        - Auto-fix Ruff"
	@echo "make check      - Run all quality checks"
	@echo "make freeze     - Update requirements.txt"

install:
	pip install -r requirements.txt

upgrade:
	python -m pip install --upgrade pip

freeze:
	pip freeze > requirements.txt

run:
	python -m uvicorn main:app --reload

test:
	pytest

coverage:
	pytest --cov=app

format:
	black .

lint:
	ruff check .

fix:
	ruff check . --fix

typecheck:
	mypy app

check:
	ruff check .
	black --check .
	mypy app
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete