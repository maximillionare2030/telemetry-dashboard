from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5000",
    "localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags = ["root"])
async def read_drood() -> dict:
    return {"message": "Home Page"}

@app.get("/Influx")
async def read_drood() -> dict:
    return {"message": "Influx"}