import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.influx_routes import influx_bp 
from client.influx import InfluxDBClientHandler 

app = FastAPI()

origins = [
    "http://localhost:3000", 
    "http://localhost:61810",  
    "localhost:3000",
    "localhost:61810",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# app.include_router(measurements_bp) 

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'influx_client'):
        await app.state.influx_client.close()  # Close the InfluxDB client if it exists

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
