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
