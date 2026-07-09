# Consensus

Consensus is an AI-powered news analysis platform that ingests articles from multiple news sources, analyzes them using a Large Language Model, and produces structured, source-agnostic summaries and metadata.

Rather than simply summarizing articles, Consensus extracts the underlying event, identifies key entities, estimates political leaning and bias, and produces a consistent JSON representation that can later be grouped into a single "consensus" view across multiple publishers.

---

## Features

* RSS ingestion from multiple news organizations
* Automatic article normalization
* AI-powered article analysis using OpenAI GPT-5
* Structured JSON output
* Bias estimation
* Political leaning classification
* Entity extraction
* Export of both raw articles and AI analyses
* Modular architecture designed for future API and web UI integration

---

## Project Architecture

```
RSS Sources
     │
     ▼
RSSService
     │
     ▼
Article Models
     │
     ▼
Analyzer
     │
     ▼
OpenAI GPT-5
     │
     ▼
Analysis Models
     │
     ▼
AnalysisService
     │
     ▼
JSON Export
     │
     ▼
FastAPI (Upcoming)
     │
     ▼
Frontend (Upcoming)
```

---

## Current Project Structure

```
app/
│
├── ai/
│   ├── analyzer.py
│   ├── llm_client.py
│   └── exceptions.py
│
├── api/
│
├── config/
│
├── database/
│
├── models/
│   ├── article.py
│   └── analysis.py
│
├── services/
│   ├── rss_service.py
│   └── analysis_service.py
│
├── pipeline.py
└── main.py

scripts/
tests/
data/
```

---

## Analysis Output

Each article is converted into a structured `Analysis` object containing:

* Neutral headline
* Primary event
* Topics
* Important people
* Organizations
* Locations
* Objective summary
* Political leaning
* Bias score
* Emotional tone
* Confidence score
* Classification reasoning

Example:

```json
{
  "headline": "Former Olympian pleads not guilty",
  "primary_event": "David Hearn entered a not guilty plea...",
  "topics": [
    "Crime",
    "Courts"
  ],
  "people": [
    "David Hearn"
  ],
  "organizations": [
    "D.C. Superior Court"
  ],
  "locations": [
    "Washington, D.C."
  ],
  "political_lean": "Center",
  "bias_score": 0.0,
  "confidence": 0.87
}
```

---

## Running the Project

### Clone the repository

```bash
git clone <repository-url>
cd consensus
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file in the project root.

```
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5
```

---

### Run the Pipeline

```bash
python -m scripts.run_pipeline
```

The pipeline will:

1. Fetch RSS articles
2. Analyze each article using GPT-5
3. Export articles
4. Export AI analyses

---

## Output

Generated files are written to the `data/` directory.

Example:

```
data/

2026_07_09_MorningArticles.json
2026_07_09_MorningAnalysis.json
```

---

## Testing

Run the test suite:

```bash
pytest
```

Coverage:

```bash
coverage run -m pytest
coverage report
```

---

## Technologies

* Python 3.13
* OpenAI Responses API
* FastAPI
* Feedparser
* Pytest
* Ruff
* Black
* MyPy

---

## Roadmap

### Completed

* RSS ingestion
* AI article analysis
* JSON export pipeline
* Modular service architecture
* OpenAI integration

### In Progress

* FastAPI REST endpoints
* React frontend
* Story clustering
* Consensus generation
* Daily report generation

### Future Enhancements

* Multiple LLM support
* Scheduled background ingestion
* Historical trend analysis
* Source comparison dashboard
* User authentication
* Cloud deployment

---

## Design Principles

Consensus follows several guiding principles:

* Source-agnostic analysis
* Separation of concerns
* Strong typing
* Dependency injection
* Testable services
* Modular architecture
* AI as a replaceable component
