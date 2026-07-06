#!/bin/bash

echo "🚀 Bootstrapping Consensus..."

###############################################
# Create Virtual Environment
###############################################

python3.13 -m venv .venv
source .venv/bin/activate

###############################################
# Install Dependencies
###############################################

pip install --upgrade pip

pip install \
fastapi \
"uvicorn[standard]" \
requests \
httpx \
feedparser \
beautifulsoup4 \
lxml \
sqlalchemy \
alembic \
pandas \
numpy \
openai \
python-dotenv \
pytest \
pytest-cov \
black \
ruff \
mypy \
pydantic \
pydantic-settings \
rich \
typer \
jinja2 \
markdown \
python-multipart \
aiofiles \
loguru

pip freeze > requirements.txt

###############################################
# Project Structure
###############################################

mkdir -p \
app/{ai,api,config,database,models,scrapers,services,utils} \
tests \
docs \
data \
scripts \
.vscode

###############################################
# Python Packages
###############################################

find app -type d -exec touch {}/__init__.py \;
touch tests/__init__.py

###############################################
# Root Files
###############################################

touch \
main.py \
.env \
.gitignore \
.editorconfig \
pyproject.toml \
README.md

###############################################
# VS Code
###############################################

cat > .vscode/settings.json <<EOF
{
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.analysis.typeCheckingMode": "basic",
    "editor.defaultFormatter": "ms-python.black-formatter",

    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports.ruff": "explicit",
            "source.fixAll.ruff": "explicit"
        }
    }
}
EOF

###############################################
# Editor Config
###############################################

cat > .editorconfig <<EOF
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
EOF

###############################################
# Git Ignore
###############################################

cat > .gitignore <<EOF
.venv/
.env
__pycache__/
.pytest_cache/
.coverage
.vscode/
*.db
.DS_Store
EOF

###############################################
# Environment Variables
###############################################

cat > .env <<EOF
OPENAI_API_KEY=

DATABASE_URL=sqlite:///data/news.db
EOF

###############################################
# PyProject
###############################################

cat > pyproject.toml <<EOF
[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E","F","I","UP"]

[tool.pytest.ini_options]
pythonpath = ["."]
EOF

###############################################
# README
###############################################

cat > README.md <<EOF
# Consensus

AI-powered News Consensus Engine.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI
EOF

###############################################
# Settings
###############################################

cat > app/config/settings.py <<EOF
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///data/news.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
EOF

###############################################
# Database
###############################################

cat > app/database/database.py <<EOF
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
EOF

###############################################
# API Routes
###############################################

cat > app/api/routes.py <<EOF
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    return {
        "application": "Consensus",
        "version": "0.1.0",
        "status": "Running"
    }


@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }
EOF

###############################################
# Main
###############################################

cat > main.py <<EOF
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Consensus",
    description="AI News Consensus Engine",
    version="0.1.0",
)

app.include_router(router)
EOF

###############################################
# Success
###############################################

echo ""
echo "✅ Bootstrap Complete!"
echo ""
echo "Activate:"
echo "source .venv/bin/activate"
echo ""
echo "Run:"
echo "python -m uvicorn main:app --reload"
echo ""
echo "Swagger:"
echo "http://127.0.0.1:8000/docs"
echo ""