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
                "name": database,
                "measurements": {},  # Change to a dictionary
            }
            
            # Get measurements for the current database
            measurements = influx.get_measurements(database)
            
            for measurement in measurements:
                # Instead of using a list for fields, use a dictionary
                fields = influx.get_fields(database, measurement)
                db_info["measurements"][measurement] = {
                    "fields": fields
                }

            info["databases"].append(db_info)  # Append db_info to the main info dict

        print(info)

        return {"info": info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve InfluxDB info: {str(e)}")
