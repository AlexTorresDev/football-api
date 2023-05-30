from fastapi import FastAPI
from server.routes import router as MatchRouter

app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "Hello World"}

app.include_router(MatchRouter, prefix="/match")