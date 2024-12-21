from fastapi import APIRouter, HTTPException
from client.influx import InfluxDBClientHandler
from pydantic import BaseModel
import logging

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(
    prefix="/api/influx",
    tags=["influx"],
    responses={404: {"description": "Not found"}},
)

influx = InfluxDBClientHandler(url="http://localhost:8086", token="", org="FSAE")

class PointsRequest(BaseModel):
    database: str
    measurement_name: str

@router.get("/get/info")
async def query_info():
    """
    Get information about InfluxDB.
    Returns: Databases, Measurements, Field Keys
    """
    try:
        info = {
            "databases": []
        }
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

@router.post("/get/points")
async def get_points(request: PointsRequest):
    """Endpoint to return InfluxDB points at a given measurement and database"""
    try:
        points = influx.get_points(request.database, request.measurement_name)
        if not points:
            raise HTTPException(status_code=404, detail="No points found for the specified measurement")
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve points: {str(e)}")
    

