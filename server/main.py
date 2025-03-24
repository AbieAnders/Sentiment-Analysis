from fastapi import FastAPI
from api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root_url():
    return { "message": "The homepage is a static Frontend page" }
