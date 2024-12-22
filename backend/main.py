import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from client.influxv1 import InfluxDBHandler
from utils.analysis import Analysis
from pydantic import BaseModel
import pandas as pd
import logging
from fastapi import File, UploadFile, Form
import os
import json
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",
    "http://localhost:61810",
    "localhost:3000",
    "localhost:61810",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:61810",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with simplified config
influx = InfluxDBHandler(
    host='localhost',
    port=8086,
    database='telemetry'
)

analyzer = Analysis()

# Request models
class PointsRequest(BaseModel):
    database: str
    measurement_name: str

class AnalysisRequest(BaseModel):
    message: str

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

# Influx routes
@app.get("/api/influx/get/info")
async def query_info():
    """ 
    Return info about the influxdb measurements
    """
    try:
        info = {
            "measurements": influx.get_measurements(),
            "fields": {}  # Will store fields for each measurement
        }
        
        # Get fields for each measurement
        for measurement in info["measurements"]:
            fields = influx.get_fields(measurement)
            info["fields"][measurement] = fields
            
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/influx/get/points")
async def get_points(request: PointsRequest):
    """ 
    Return points from a specific measurement
    """
    try:
        points = influx.get_points(request.measurement_name)
        if not points:
            raise HTTPException(status_code=404, detail="No points found")
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/influx/upload")
async def upload_data(file: UploadFile = File(...)):
    """ 
    Upload info from a file to influxdb
    Parameters:
        file: takes a file uploaded to a form
    """
    try:
        contents = await file.read()
        temp_file_path = f"temp_{file.filename}"
        
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        influx.csv_to_influx(temp_file_path)
        os.remove(temp_file_path)
        
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analysis routes
@app.post("/api/analysis/analyze")
async def analyze_data(request: AnalysisRequest):
    """ 
    Analyze data from influxdb
    """
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
            
        result = await analyzer.analyze_data(request.message)
        if not result:
            raise HTTPException(status_code=404, detail="No analysis results found")
            
        return {"analysis": result}
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # verify db has data
    measurements = influx.get_measurements()
    if not measurements:
        logger.warning("No measurements found in the database. Please upload data first.")
    else:
        logger.info(f"Found {len(measurements)} measurements in the database.")

    uvicorn.run(app, host="localhost", port=8000)
