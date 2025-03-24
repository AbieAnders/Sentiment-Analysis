from fastapi import APIRouter
from api.search import router as search_router
from api.extract import router as extract_router
from api.analyse import router as analyse_router

api_router = APIRouter()

api_router.include_router(search_router, prefix="/search", tags=["Search"])
api_router.include_router(extract_router, prefix="/extract", tags=["Extract"])
api_router.include_router(analyse_router, prefix="/analyse", tags=["Analyse"])