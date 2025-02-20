from fastapi import APIRouter

router = APIRouter()


@router.get('/', tags=['Index Page'])
async def index() -> dict:
    """Returns a dict with basic information of the service"""
    return {
        "name": "Training App",
        "description": "REST API for training application",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@router.get('/health', tags=['Health'])
async def health_check() -> dict:
    """Returns a dict with the running status of the service"""
    return {
        'status': 'ok',
    }
