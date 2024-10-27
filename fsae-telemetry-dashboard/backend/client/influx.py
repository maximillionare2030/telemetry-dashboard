from influxdb_client import InfluxDBClient, Point
from typing import List
from models import MotorData, ControllerData, BatteryData
from .exceptions import InfluxNotAvailableException, BucketNotFoundException, BadQueryException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# InfluxDB client setup
class InfluxDBClientHandler:
    def __init__(self, url: str, token: str, org: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = "OrionBMS"  # Set the bucket name to "OrionBMS"
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api()  # Create a write API instance

    def write_data(self, bucket: str, data: List[Point]): # each point is a row of data to add to the database
        try:
            self.write_api.write(bucket=bucket, record=data) # use the write api to write data to the database in the bucket
            logger.info("Data written successfully to InfluxDB.")
        except Exception as e:
            logger.error(f"Failed to write data: {str(e)}")
            raise BadQueryException() from e

    def query_controller_data(self, start_time: str, end_time: str) -> List[ControllerData]:
        logger.info(f"Querying controller data from {start_time} to {end_time}")
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "controller_data")
        """
        try:
            result = self.query_api.query(query)
            controller_data_list = []
            for table in result:
                for record in table.records:
                    controller_data_list.append(
                        ControllerData(
                            controllerTMP=record.get_value() if record.get_field() == "controllerTMP" else None
                        )
                    )
            return controller_data_list
        except Exception as e:
            logger.error(f"Error querying controller data: {str(e)}")
            raise BadQueryException() from e

    def query_battery_data(self, start_time: str, end_time: str) -> List[BatteryData]:
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "battery_data")
        |> filter(fn: (r) => r["_field"] == "batteryVOLT" or r["_field"] == "batteryTEMP" or r["_field"] == "batteryCURR")
        """
        try:
            result = self.query_api.query(query)
            battery_data_list = []
            for table in result:
                for record in table.records:
                    battery_data_list.append(
                        BatteryData(
                            batteryVOLT=record.get_value() if record.get_field() == "batteryVOLT" else None,
                            batteryTEMP=record.get_value() if record.get_field() == "batteryTEMP" else None,
                            batteryCURR=record.get_value() if record.get_field() == "batteryCURR" else None
                        )
                    )
            return battery_data_list
        except Exception as e:
            raise BadQueryException() from e

    def fetch_recent_data(self):
        """
        Fetch recent data from InfluxDB for the last 10 minutes.
        """
        query = """from(bucket: "OrionBMS")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "measurement1")"""
        
        try:
            tables = self.query_api.query(query, org=self.org)
            for table in tables:
                for record in table.records:
                    print(record)
        except Exception as e:
            print(f"Error fetching recent data: {e}")

    def close(self):
        """Close the InfluxDB client connection."""
        self.client.close()

    def query_motor_data(self, start_time: str, end_time: str) -> List[MotorData]:
        logger.info(f"Querying motor data from {start_time} to {end_time}")
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "motor_data")
        """
        try:
            result = self.query_api.query(query)
            motor_data_list = []
            for table in result:
                for record in table.records:
                    motor_data_list.append(
                        MotorData(
                            motorSPD=record.get_value() if record.get_field() == "motorSPD" else None,
                            motorTMP=record.get_value() if record.get_field() == "motorTMP" else None
                        )
                    )
            return motor_data_list
        except Exception as e:
            logger.error(f"Error querying motor data: {str(e)}")
            raise BadQueryException() from e
