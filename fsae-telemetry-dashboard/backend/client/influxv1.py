from influxdb_client import InfluxDBClient
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class InfluxDBHandler:
    def __init__(self, host, port):
        # Retrieve the token from the environment variables
        token = os.getenv("INFLUXDB_TOKEN")
        org = os.getenv("INFLUX_ORG_NAME")
        
        # Initialize the InfluxDB client with the token
        self.client = InfluxDBClient(
            url=f"http://{host}:{port}",
            token=token,
            org=org
        )
        
        # Verify connection
        try:
            print("Successfully connected to InfluxDB.")
        except Exception as e:
            print(f"Error connecting to InfluxDB: {e}")

    def csv_to_influx(self, filename, database):
        """Imports CSV data to a specified measurement in the given database."""
        try:
            # Read CSV and prepare JSON data for InfluxDB
            df = pd.read_csv(filename)
            measurement_name = filename.split("\\")[-1][:-4]  # Use filename for measurement name without .csv extension
            print(f"Uploading data to measurement: {measurement_name}")
            json_body = []
            fields = df.columns[1:]  # Exclude timestamp column

            for _, row in df.iterrows():
                json_body.append({
                    "measurement": measurement_name,
                    "time": row.iloc[0],  # Timestamp should be in RFC3339 format
                    "fields": {field: row[field] for field in fields}
                })

            # Write data to InfluxDB
            self.write_points(json_body, database)
            print("Data written successfully to InfluxDB.")

        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

    def write_points(self, json_body, bucket):
        try:
            # Use the write_api to write data
            write_api = self.client.write_api()
            write_api.write(bucket=bucket, record=json_body)
            print(f"Data written successfully to InfluxDB in bucket: {bucket}")
            print(f"Data: {json_body}")
        except Exception as e:
            print(f"Failed to write data: {e}")

if __name__ == "__main__":
    # Initialize the handler
    handler = InfluxDBHandler(host='localhost', port=8086)
    
    # Path to your CSV file
    csv_file_path = "./fsae-telemetry-dashboard/backend/client/vehicle_data/Kilozott_Dummy_Data.csv"
    
    # Write data to the OrionBMS database
    handler.csv_to_influx(csv_file_path, 'OrionBMS')







"""
InfluxDB Visualization:

Databases will be used as a dataset for each race (ex: ATOM, FSAE Final)
Measurements are the different sets of data that will be used from the vehicle (First Lap, Second Lap, Third Lap)

Each MEASUREMENT has
    Points: Set of data that we want to measure from
    Fields: Key-value pairs that hold the actual data you want to track (ex. temperature = 23.5, battery voltage = 10.0)
    Tags: Key-value pairs that provide additional context about the data (ex. car_id = 123, race_id = 456)

+--------------------------+
|       InfluxDB           |
|                          |
|   +-------------------+  |
|   |    Database      |  |
|   |  (e.g., mydb)    |  |
|   |                   |  |
|   | +---------------+ |  |
|   | | Measurement   | |  |
|   | | (e.g., cpu)   | |  |
|   | +---------------+ |  |
|   | | Points         | |  |
|   | |  +---------+   | |  |
|   | |  | Field   |   | |  |
|   | |  | (value) |   | |  |
|   | |  +---------+   | |  |
|   | |  | Tag     |   | |  |
|   | |  | (e.g.,  |   | |  |
|   | |  | host=...|   | |  |
|   | |  +---------+   | |  |
|   | +---------------+ |  |
|   +-------------------+  |
|                          |
|  +--------------------+  |
|  | Retention Policies  |  |
|  | Continuous Queries   |  |
|  +--------------------+  |
|                          |
|  +--------------------+  |
|  | Shards & Shard     |  |
|  | Groups              |  |
|  +--------------------+  |
+--------------------------+


"""