from fastapi import FastAPI
from .routes import router as MatchRouter

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Hello World"}

app.include_router(MatchRouter, prefix="/match")