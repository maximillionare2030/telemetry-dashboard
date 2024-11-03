from influxdb_client import InfluxDBClient, Point
from typing import List
from exceptions import BadQueryException
import logging
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from a .env file located in the backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUX_ORG_NAME = os.getenv("INFLUX_ORG_NAME")

# Print the token and organization for debugging
print(f"Using InfluxDB Token: {INFLUXDB_TOKEN}")
print(f"Using InfluxDB Organization: {INFLUX_ORG_NAME}")

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

    def write_data(self, bucket: str, data: List[Point]):
        try:
            self.write_api.write(bucket=bucket, record=data)
            logger.info("Data written successfully to InfluxDB.")
        except Exception as e:
            logger.error(f"Failed to write data: {str(e)}")
            raise BadQueryException() from e

    def query_data(self, measurement: str, fields: List[str], timestamp: str):
        logger.info(f"Querying data from {measurement} on {timestamp}")
        field_filters = ' or '.join([f'r["_field"] =="{field}"' for field in fields])
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {timestamp}, stop: {timestamp})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> filter(fn: (r) => {field_filters})
        """
        try:
            result = self.query_api.query(query)
            data_list = []
            for table in result:
                for record in table.records:
                    data_list.append(record.values)
            return data_list
        except Exception as e:
            logger.error(f"Error querying data: {str(e)}")
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

 # test case
def test_query_data():
    client_handler = InfluxDBClientHandler(url="http://localhost:8086", token=INFLUXDB_TOKEN, org=INFLUX_ORG_NAME)

    measurement = "motor_data"
    fields = ["motorSPD", "motorTEMP", "packVOLT", "packTEMP", "packCURR", "packCCL"]
    timestamp = "2024-09-01T00:00:00Z"

    try:
        data = client_handler.query_data(measurement, fields, timestamp)
        print(data)
    except BadQueryException:
        print("Failed to query data. Please check your credentials and query parameters.")

# Call the test function
if __name__ == "__main__":
    test_query_data()
