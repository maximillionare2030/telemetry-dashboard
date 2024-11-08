# store the fastapi app connection
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.influx_routes import router as influx_router

app = FastAPI(title="FSAE Telemetry API")

origins = [
    "http://localhost:3000", 
    "http://localhost:61810",  
    "localhost:3000",
    "localhost:61810",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(influx_router, prefix="/api/influx", tags=["InfluxDB"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)



