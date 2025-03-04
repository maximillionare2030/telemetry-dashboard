from influxdb import InfluxDBClient
import pandas as pd
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

class InfluxDBHandler:
    def __init__(self, host, port=8086, database='telemetry'):
        self.host = host
        self.port = port
        self.database = database
        self.client = InfluxDBClient(
            host=self.host,
            port=self.port,
            database=self.database,
            username=os.getenv('INFLUXDB_USER', ''),
            password=os.getenv('INFLUXDB_PASSWORD', ''),
            ssl=True,
        )
        try:
            # Get list of databases first
            databases = self.client.get_list_database()
            if not any(db['name'] == self.database for db in databases):
                self.client.create_database(self.database)
                print(f"Created database: {self.database}")
            
            # Switch to the database
            self.client.switch_database(self.database)
            
        except Exception as e:
            print(f"Error initializing database: {e}")

    def get_measurements(self):
        """Returns a list of measurements in the database."""
        try:
            measurements = self.client.get_list_measurements()
            return [m['name'] for m in measurements]
        except Exception as e:
            logger.error(f"Error getting measurements: {str(e)}")
            return []

    def get_fields(self, measurement):
        """Returns a list of field names for a given measurement."""
        try:
            query = f"SHOW FIELD KEYS FROM {measurement}"
            result = self.client.query(query)
            fields = list(result.get_points())
            return [field['fieldKey'] for field in fields]
        except Exception as e:
            logger.error(f"Error getting fields for {measurement}: {str(e)}")
            return []

    def get_points(self, measurement):
        """Returns points from a specific measurement."""
        try:
            self.client.switch_database(self.database)
            query = f'SELECT * FROM "{measurement}" LIMIT 1000'
            result = self.client.query(query)
            return list(result.get_points())
        except Exception as e:
            print(f"Error retrieving points for {measurement}: {e}")
            return []

    def csv_to_influx(self, csv_file_path):
        """Convert CSV file to InfluxDB points and write them."""
        try:
            df = pd.read_csv(csv_file_path)
            measurement_name = Path(csv_file_path).stem
            
            # Prepare data in batches
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch_df = df.iloc[i:i+batch_size]
                json_body = []
                
                for _, row in batch_df.iterrows():
                    json_body.append({
                        "measurement": measurement_name,
                        "time": row.iloc[0],
                        "fields": {field: row[field] for field in df.columns[1:]}
                    })
                
                self.client.write_points(json_body)
                
            return True
        except Exception as e:
            print(f"Error converting CSV to InfluxDB: {e}")
            return False

    def query(self, query_string):
        try:
            return self.client.query(query_string)
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            return None






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
|  | Continuous Queries  | |
|  +--------------------+  |
|                          |
|  +--------------------+  |
|  | Shards & Shard     |  |
|  | Groups              | |
|  +--------------------+  |
+--------------------------+


"""
