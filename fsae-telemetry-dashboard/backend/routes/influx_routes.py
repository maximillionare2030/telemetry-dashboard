from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from client.influxv1 import InfluxDBHandler

# Create a router instance
influx_bp = APIRouter()


# Instantiate the handler
influx = InfluxDBHandler(
    host="localhost",
    port=8086,
    username="root",
    password="root",
)


# Define a model for the request parameters
class PointsRequest(BaseModel):
    database: str
    measurement_name: str

@influx_bp.get("/get/info")
async def query_info():
    """
    Get information about InfluxDB.

    Returns: Databases, Measurements, Field Keys,
    """
    try:
        info = {
            "databases": []  # Start with an empty list for databases
        }

        # Retrieve the list of databases
        databases = influx.get_databases()

        for database in databases:
            db_info = {
                database: {  # Use the database name as the key
                    "measurements": {}
                }
            }

            # Get measurements for the current database
            measurements = influx.get_measurements(database)

            for measurement in measurements:
                # Add fields for each measurement in the current database
                fields = influx.get_fields(database, measurement)
                db_info[database]["measurements"][measurement] = {
                    "fields": fields
                }

            # Append db_info dictionary to the main info list
            info["databases"].append(db_info)

        print(info)

        return {"info": info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve InfluxDB info: {str(e)}")

@influx_bp.post("/get/points", response_model=List[dict])
async def get_points(request: PointsRequest):
    """
    Get specific points from InfluxDB for a given database and measurement.

    Returns: Points from the specified measurement.
    """
    try:
        # Use the provided database and measurement name to retrieve points
        points = influx.get_points(request.database, request.measurement_name)

        if not points:
            raise HTTPException(status_code=404, detail="No points found for the specified measurement.")

        return {"points": points}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve points: {str(e)}")