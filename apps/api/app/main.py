from fastapi import FastAPI

from app.api import crews


app = FastAPI()


@app.get("/")
def read_root():
    return "Assalamualaikom, Welcome to the nextcrew.ai"


app.include_router(crews.router)
