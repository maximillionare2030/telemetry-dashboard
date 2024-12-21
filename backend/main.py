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

# Initialize services
influx = InfluxDBHandler(
    host='localhost',
    port=8086,
    username='',
    password=''
)

analyzer = Analysis()

# Request models
class PointsRequest(BaseModel):
    database: str
    measurement_name: str

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

# Influx routes
@app.get("/api/influx/get/info")
async def query_info():
    """ 
    Return info about the influxdb
    """
    try:
        info = {"databases": []}
        databases = influx.get_databases()
        for database in databases:
            db_info = {
                database: {
                    "measurements": {}
                }
            }
            measurements = influx.get_measurements(database)
            for measurement in measurements:
                fields = influx.get_fields(database, measurement)
                db_info[database]["measurements"][measurement] = {
                    "fields": fields
                }
            info["databases"].append(db_info)
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve InfluxDB info: {str(e)}")

@app.post("/api/influx/get/points")
async def get_points(request: PointsRequest):
    """ 
    Return a datapoint from influxdb
    """
    try:
        points = influx.get_points(request.database, request.measurement_name)
        if not points:
            raise HTTPException(status_code=404, detail="No points found")
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/influx/upload")
async def upload_data(file: UploadFile = File(...), database: str = Form(...)):
    """ 
    Upload info from a file to influxdb
    Parameters:
        file: takes a file uploaded to a form
        database: takes a database name from the form
    """
    try:
        # read the uploaded file
        contents = await file.read()
        temp_file_path = f"temp_{file.filename}"

        # save file temporarily
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        # upload to influxdb
        influx.csv_to_influx(temp_file_path, database)

        # clean up and remove temp file
        os.remove(temp_file_path)

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analysis routes
@app.post("/api/analysis/analyze")
async def analyze_telemetry(data: dict):
    logger.info("Accessing endpoint: /api/analysis/analyze")
    try:
        df = pd.DataFrame(data['telemetry'])
        user_message = data.get('message', '')
        analysis = analyzer.analyze_telemetry(df)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)