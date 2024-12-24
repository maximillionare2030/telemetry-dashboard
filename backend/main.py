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
from fastapi import Request

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

@app.get("/api/influx/get/mean")
async def get_mean():
    """
    Return mean of the data from influxdb
    """
    try:
        measurements = influx.get_measurements()
        logger.info(f"Found measurements: {measurements}")
        
        if not measurements:
            return {"message": "No measurements found"}
            
        # define key params to track
        key_metrics = {
            'motorSPD': 'Motor speed',
            'motorTEMP': 'Motor temp',
            'packVOLT': 'Pack voltage',
            'packTEMP': 'Pack temp',
            'packCURR': 'Pack current',
            'packCCL': 'Pack ccl'
        }

        # store the means of each metric
        means = {}

        #* only accessing the first measurement for now. In the future, allow user to select the measurment to analyze
        measurement = measurements[0]  # Get the first measurement
        
        # get the mean of each metric
        for metric, display_name in key_metrics.items():
            try:
                query = f'SELECT MEAN("{metric}") as mean FROM "{measurement}"'
                result = influx.client.query(query)
                
                if result:
                    points = list(result.get_points())
                    if points and len(points) > 0:
                        mean_value = points[0].get('mean')  
                        if mean_value is not None:
                            means[display_name] = round(float(mean_value), 2)
                            logger.info(f"Successfully processed {display_name}: {means[display_name]}")
            
            except Exception as e:
                logger.error(f"Error processing metric {metric}: {str(e)}")
                continue

        logger.info(f"Final means: {means}")

        if means:
            # Create analysis instance
            analyzer = Analysis()
            status_analysis = analyzer.analyze_nominal_ranges(means)
            
            # Combine means with their status
            result = {
                'means': means,
                'status': status_analysis
            }
            
            return result
            
        return {'means': {}, 'status': {}}
        
    except Exception as e:
        logger.error(f"Error in get_mean: {str(e)}")
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
    
# time series routes
@app.get("/api/influx/get/timerange")
async def get_time_range():
    """ 
    Get the earliest and latest timestamp from InfluxDB
    """
    try:
        # get the measurements from influxdb
        measurements = influx.get_measurements()
        if not measurements:
            raise {"message": "No measurements found"}
        measurement = measurements[0] # get the first measurement

        # get earliest time (first record)
        earliest_query = f'SELECT * FROM "{measurement}" ORDER BY time ASC LIMIT 1'
        earliest_result = influx.client.query(earliest_query)

        # get latest time (last record)
        latest_query = f'SELECT * FROM "{measurement}" ORDER BY time DESC LIMIT 1'
        latest_result = influx.client.query(latest_query)

        # return the earliest and latest time
        if earliest_result and latest_result:
            # get the first point from the result
            earliest_point = list(earliest_result.get_points())[0]
            latest_point = list(latest_result.get_points())[0]

            # Convert InfluxDB timestamps to Unix timestamps
            from datetime import datetime
            import pytz

            def parse_influx_time(time_str):
                dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
                dt = pytz.utc.localize(dt)
                return int(dt.timestamp())

            earliest_time = parse_influx_time(earliest_point['time'])
            latest_time = parse_influx_time(latest_point['time'])

            # return the earliest and latest time
            return {
                "earliest": earliest_time,
                "latest": latest_time
            }
        else:
            raise HTTPException(status_code=404, detail="No resulting time range found")
        
    except Exception as e:
        logger.error(f"Error in get_time_range: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/influx/get/timeseries")
async def get_timeseries_data(request: Request):
    """
    Extract time series configs from influxdb
    """
    try:
        body = await request.json()
        measurement = body.get('measurement')
        fields = body.get('fields')
        from_time = body.get('from')
        to_time = body.get('to')

        if not all([measurement, fields, from_time, to_time]):
            raise HTTPException(status_code=400, detail="Missing required parameters")

        # Query InfluxDB for time series data
        query = f'SELECT {",".join(fields)} FROM {measurement} WHERE time >= {from_time}s AND time <= {to_time}s'
        result = influx.query(query)

        points = []
        for point in result.get_points():
            points.append(point)

        return {"points": points}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # verify db has data
    measurements = influx.get_measurements()
    if not measurements:
        logger.warning("No measurements found in the database. Please upload data first.")
    else:
        logger.info(f"Found {len(measurements)} measurements in the database.")

    uvicorn.run(app, host="localhost", port=8000)
