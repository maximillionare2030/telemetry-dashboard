from influxdb import InfluxDBClient
import pandas as pd
from pathlib import Path

class InfluxDBHandler:
    def __init__(self, host='localhost', port=8086, database='telemetry'):
        self.host = host
        self.port = port
        self.database = database
        self.client = InfluxDBClient(
            host=self.host,
            port=self.port,
            database=self.database,
            username='',
            password='',
            ssl=False,
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
            # Make sure we're using the right database
            self.client.switch_database(self.database)
            result = self.client.query('SHOW MEASUREMENTS')
            measurements = list(result.get_points())
            if not measurements:
                return []
            return [m['name'] for m in measurements]
        except Exception as e:
            print(f"Error retrieving measurements: {e}")
            return []

    def get_fields(self, measurement):
        """Returns fields for a specific measurement."""
        try:
            result = self.client.query(f'SHOW FIELD KEYS FROM "{measurement}"')
            return [field['fieldKey'] for field in result.get_points()]
        except Exception as e:
            print(f"Error retrieving fields for {measurement}: {e}")
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