# ==========================================================
# Consensus Makefile
# ==========================================================

PYTHON := python3
PIP := pip3

BACKEND_DIR := .
FRONTEND_DIR := frontend

UVICORN := uvicorn app.main:app --reload


# ==========================================================
# Install
# ==========================================================

.PHONY: install

install:
	@echo "Installing Python dependencies..."
	@$(PIP) install -r requirements.txt

	@echo ""
	@echo "Installing Frontend dependencies..."
	@cd $(FRONTEND_DIR) && npm install


# ==========================================================
# Formatting
# ==========================================================

.PHONY: format

format:
	black .
	ruff check . --fix


# ==========================================================
# Linting
# ==========================================================

.PHONY: lint

lint:
	ruff check .
	mypy .


# ==========================================================
# Tests
# ==========================================================

.PHONY: test

test:
	pytest


.PHONY: coverage

coverage:
	coverage run -m pytest
	coverage report


# ==========================================================
# Individual Services
# ==========================================================

.PHONY: pipeline

pipeline:
	$(PYTHON) -m scripts.run_pipeline


.PHONY: backend

backend:
	$(UVICORN)


.PHONY: frontend

frontend:
	cd $(FRONTEND_DIR) && npm run dev


# ==========================================================
# Demo
# ==========================================================

.PHONY: demo

demo:
	@echo "==========================================="
	@echo " Activating Virtual Environment..."
	@echo "==========================================="
	@. .venv/bin/activate && \
	echo "Using Python: $$(which python)" && \
	echo "" && \
	echo "Installing Backend Dependencies..." && \
	pip install -r requirements.txt && \
	echo "" && \
	echo "Running Consensus Pipeline..." && \
	python -m scripts.run_pipeline

	@echo ""
	@echo "==========================================="
	@echo " Installing Frontend..."
	@echo "==========================================="
	@cd frontend && npm install

	@echo ""
	@echo "==========================================="
	@echo " Starting FastAPI..."
	@echo "==========================================="
	@nohup .venv/bin/python -m uvicorn app.main:app --reload > backend.log 2>&1 &

	@sleep 3

	@echo ""
	@echo "==========================================="
	@echo " Starting React..."
	@echo "==========================================="
	@cd frontend && nohup npm run dev > ../frontend.log 2>&1 &

	@sleep 5

	@echo ""
	@echo "==========================================="
	@echo " Consensus is Ready!"
	@echo ""
	@echo " Backend : http://localhost:8000"
	@echo " Swagger : http://localhost:8000/docs"
	@echo " Frontend: http://localhost:5173"
	@echo "==========================================="


# ==========================================================
# Stop
# ==========================================================

.PHONY: stop

stop:
	@pkill -f uvicorn || true
	@pkill -f vite || true
	@echo "Consensus stopped."


# ==========================================================
# Clean
# ==========================================================

.PHONY: clean

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f backend.log
	rm -f frontend.log


# ==========================================================
# Help
# ==========================================================

.PHONY: help

help:
	@echo ""
	@echo "Consensus Commands"
	@echo "-------------------------------"
	@echo "make install     Install dependencies"
	@echo "make pipeline    Run analysis pipeline"
	@echo "make backend     Start FastAPI"
	@echo "make frontend    Start React"
	@echo "make demo        Run everything"
	@echo "make test        Run unit tests"
	@echo "make coverage    Run coverage"
	@echo "make lint        Run linting"
	@echo "make format      Format code"
	@echo "make clean       Remove temporary files"
	@echo "make stop        Stop backend/frontend"
	@echo ""