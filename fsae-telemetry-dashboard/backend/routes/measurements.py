# api request to retrieve measurements data 
from fastapi import APIRouter, HTTPException
from client.influx import InfluxDBClientHandler
from dotenv import load_dotenv
import os

# creates blueprint for a new router in the application
measurements_bp = APIRouter()

load_dotenv()
influx_client = InfluxDBClientHandler(url="http://localhost:8086", token=os.getenv("INFLUX_API_KEY"), org=os.getenv("INFLUX_ORG_NAME"))

MEASUREMENT_BUCKETS = {
    'motor_data': 'motor_bucket',
    'battery_data': 'battery_bucket',
}

@measurements_bp.get('/data/{measurement}')
# pull mesurement data from the buckets in influxdb
async def get_measurement_data(measurement: str, start_time: str = '-1h', end_time: str = 'now()'):
    bucket = MEASUREMENT_BUCKETS.get(measurement)
    if not bucket:
        raise HTTPException(status_code=400, detail="Invalid measurement type")
    
    try:
        if measurement == 'motor_data':
            data = await influx_client.query_motor_data(start_time, end_time, bucket)
        elif measurement == 'battery_data':
            data = await influx_client.query_controller_data(start_time, end_time, bucket)
        else:
            raise HTTPException(status_code=400, detail="Invalid Measurement Type")
        
        return data  # Return the data directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
