from influxdb import InfluxDBClient
import pandas as pd

class InfluxDBHandler:
    def __init__(self, host, port, username, password):
        # Initialize the InfluxDB client
        self.client = InfluxDBClient(host=host, port=port, username=username, password=password)
        
        # Verify connection and list databases
        try:
            databases = self.get_databases()
            print(f"Successfully connected to InfluxDB. Available databases: {databases}")
        except Exception as e:
            print(f"Error connecting to InfluxDB: {e}")

    def get_databases(self):
        """Returns a list of available databases in InfluxDB."""
        try:
            return [db['name'] for db in self.client.get_list_database()]
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
            for point in points:
                print(point)

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
            # Ensure the client is switched to the target database (create if not exists)
            self.ensure_database(database)

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
            self.client.write_points(json_body)
            print("Data written successfully to InfluxDB.")

        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

    def influx_to_csv(self, measurement_name, output_filename, database):
        """Exports data from a specified measurement in the given database to CSV."""
        try:
            # Ensure the client is switched to the target database
            self.client.switch_database(database)

            # Query data from the specified measurement
            query = f'SELECT * FROM "{measurement_name}"'
            result = self.client.query(query)
            
            # Convert query result to a DataFrame and export to CSV
            points = list(result.get_points())
            if not points:
                print(f"No data found in measurement '{measurement_name}'")
                return

            df = pd.DataFrame(points)
            df.to_csv(output_filename, index=False)
            print(f"Data exported successfully to {output_filename}")

        except Exception as e:
            print(f"Error exporting data from measurement '{measurement_name}': {e}")







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