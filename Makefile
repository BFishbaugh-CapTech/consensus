# ==========================================================
# Consensus Makefile
# ==========================================================

VENV := .venv

PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy
COVERAGE := $(PYTHON) -m coverage

UVICORN := $(PYTHON) -m uvicorn app.main:app --reload

FRONTEND_DIR := frontend


# ==========================================================
# Install
# ==========================================================

.PHONY: install

install:
	@echo "Installing Backend dependencies..."
	@$(PIP) install -r requirements.txt

	@echo ""
	@echo "Installing Frontend dependencies..."
	@cd $(FRONTEND_DIR) && npm install


# ==========================================================
# Formatting
# ==========================================================

.PHONY: format

format:
	$(BLACK) .
	$(RUFF) check . --fix


# ==========================================================
# Linting
# ==========================================================

.PHONY: lint

lint:
	$(RUFF) check .
	$(MYPY) .


# ==========================================================
# Tests
# ==========================================================

.PHONY: test

test:
	$(PYTEST)


.PHONY: coverage

coverage:
	$(COVERAGE) run -m pytest
	$(COVERAGE) report


# ==========================================================
# Utility Scripts
# ==========================================================

.PHONY: rssService

rssService:
	$(PYTHON) -m scripts.test_rss


.PHONY: llm

llm:
	$(PYTHON) -m scripts.test_llm


.PHONY: analysis

analysis:
	$(PYTHON) -m scripts.test_analysis


.PHONY: pipeline

pipeline:
	$(PYTHON) -m scripts.run_pipeline


# ==========================================================
# Servers
# ==========================================================

.PHONY: backend

backend:
	$(UVICORN)


.PHONY: frontend

frontend:
	cd $(FRONTEND_DIR) && npm run dev


# ==========================================================
# Demo
# ==========================================================

.PHONY: run
run: demo


.PHONY: demo

demo: install

	@echo ""
	@echo "==========================================="
	@echo " Running Consensus Pipeline..."
	@echo "==========================================="
	@$(PYTHON) -m scripts.run_pipeline

	@echo ""
	@echo "==========================================="
	@echo " Starting FastAPI..."
	@echo "==========================================="
	@nohup $(UVICORN) > backend.log 2>&1 &

	@sleep 3

	@echo ""
	@echo "==========================================="
	@echo " Starting React..."
	@echo "==========================================="
	@cd $(FRONTEND_DIR) && nohup npm run dev > ../frontend.log 2>&1 &

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
	@echo "-----------------------------------------"
	@echo "make install     Install dependencies"
	@echo "make pipeline    Run full pipeline"
	@echo "make rssService  Run RSS test"
	@echo "make llm         Run LLM test"
	@echo "make analysis    Run Analysis test"
	@echo "make backend     Start FastAPI"
	@echo "make frontend    Start React"
	@echo "make run         Install and launch everything"
	@echo "make demo        Same as make run"
	@echo "make test        Run unit tests"
	@echo "make coverage    Run coverage"
	@echo "make lint        Run linting"
	@echo "make format      Format source"
	@echo "make clean       Remove generated files"
	@echo "make stop        Stop backend/frontend"
	@echo ""