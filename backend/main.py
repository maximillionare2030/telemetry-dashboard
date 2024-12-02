import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.influx_routes import router
 

app = FastAPI()

origins = [
    "http://localhost:3000", 
    "http://localhost:61810",  
    "localhost:3000",
    "localhost:61810",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:61810"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router, prefix="/api/influx", tags=["InfluxDB"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)