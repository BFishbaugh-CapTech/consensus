from pathlib import Path
import json

from fastapi import APIRouter, HTTPException

from app.pipeline import Pipeline

router = APIRouter()


DATA_DIR = Path("data")


@router.get("/analysis")
def get_analysis():
    """
    Return the most recently generated analysis.
    """

    files = sorted(
        DATA_DIR.glob("*Analysis.json"),
        reverse=True,
    )

    if not files:
        raise HTTPException(
            status_code=404,
            detail="No analysis has been generated.",
        )

    with files[0].open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


@router.get("/articles")
def get_articles():
    """
    Return the most recently generated articles.
    """

    files = sorted(
        DATA_DIR.glob("*Articles.json"),
        reverse=True,
    )

    if not files:
        raise HTTPException(
            status_code=404,
            detail="No articles have been generated.",
        )

    with files[0].open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


@router.post("/pipeline/run")
def run_pipeline():
    """
    Execute the Consensus pipeline.
    """

    Pipeline().run()

    return {
        "status": "success",
        "message": "Pipeline completed successfully.",
    }