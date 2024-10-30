from fastapi import APIRouter, HTTPException
from client.influxv1 import InfluxDBHandler
import os

handler = InfluxDBHandler(
    host="localhost",
    port=8086,
    username="root",
    password="root",
    database="dummy_data"
)

influx_bp = APIRouter()