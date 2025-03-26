from fastapi import APIRouter
from api.ddg_search import router as ddg_search_router
from api.sentiment import router as sentiment_router

api_router = APIRouter()

api_router.include_router(ddg_search_router, prefix="/search", tags=["Search"])
api_router.include_router(sentiment_router, prefix="/analyse", tags=["Analyse"])