import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

class InfluxDBHandler:
    def __init__(self):
        # Get environment variables
        self.token = os.getenv('INFLUXDB_TOKEN')
        self.org = os.getenv('INFLUX_ORG_NAME')
        self.url = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
        
        # Initialize InfluxDB client
        try:
            self.client = InfluxDBClient(
                url=self.url,
                token=self.token,
                org=self.org
            )
            print("Successfully connected to InfluxDB.")
        except Exception as e:
            print(f"Failed to connect to InfluxDB: {e}")

    def get_databases(self):
        """Returns a list of available databases in InfluxDB."""
        try:
            return [db['name'] for db in self.client.get_list_database() if db['name'] != '_internal']
        except Exception as e:
            print(f"Error retrieving databases: {e}")
            return []
        
    def drop_database(self, database):
        """Drops a specific database from InfluxDB."""
        try:
            self.client.drop_database(database)
            print(f"Database '{database}' dropped successfully.")
        except Exception as e:
            print(f"Error dropping database '{database}': {e}")

    def get_measurements(self, database):
        """Returns a list of measurements in the specified database."""
        try:
            # Switch to the specified database
            self.client.switch_database(database)
            measurements = self.client.query('SHOW MEASUREMENTS')
            print("Successfully retrieved measurements")
            return [m['name'] for m in measurements.get_points()]
        except Exception as e:
            print(f"Error retrieving measurements from '{database}': {e}")
            return []
        
    def get_fields(self, database, measurement_name):
        """Returns a list of field keys in the specified measurement of the given database."""
        try:
            # Switch to the specified database
            self.client.switch_database(database)
            
            # Query to get the fields of the measurement
            query = f'SHOW FIELD KEYS FROM "{measurement_name}"'
            result = self.client.query(query)
            
            # Log successful retrieval of fields
            print(f"Successfully retrieved fields from '{measurement_name}' in database '{database}'")
            
            # Return a list of field keys
            return [field['fieldKey'] for field in result.get_points()]
        
        except Exception as e:
            print(f"Error retrieving fields from measurement '{measurement_name}' in database '{database}': {e}")
            return []


    def get_points(self, database, measurement_name):
        """Retrieves all points from a specified measurement in the given database."""
        try:
            # Ensure the client is switched to the target database
            self.client.switch_database(database)

            # Query all points from the specified measurement
            query = f'SELECT * FROM "{measurement_name}"'
            result = self.client.query(query)
            points = list(result.get_points())

            if not points:
                print(f"No points found in measurement '{measurement_name}'")
                return []

            print(f"Retrieved {len(points)} points from measurement '{measurement_name}':")

            return points  # Optionally return the points for further processing

        except Exception as e:
            print(f"Error retrieving points from measurement '{measurement_name}': {e}")
            return []

    def ensure_database(self, database):
        """Ensures that the specified database exists; creates it if it doesn't."""
        
        databases = self.get_databases()
        
        if database not in databases:
            print(f"Database '{database}' does not exist. Creating it.")
            self.client.create_database(database)
        
        self.client.switch_database(database)
        print(f"Switched to database: {database}")

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
    handler = InfluxDBHandler()
    
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