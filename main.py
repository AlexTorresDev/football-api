from fastapi import FastAPI
from server.routes import router as MatchRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
  return {"message": "Hello World"}

app.include_router(MatchRouter, prefix="/match")