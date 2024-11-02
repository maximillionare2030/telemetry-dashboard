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

    def get_measurements(self, database):
        """Returns a list of measurements in the specified database."""
        try:
            # Switch to the specified database
            self.client.switch_database(database)
            measurements = self.client.query('SHOW MEASUREMENTS')
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
            return [field['fieldKey'] for field in result.get_points()]
        except Exception as e:
            print(f"Error retrieving fields from measurement '{measurement_name}' in database '{database}': {e}")
            return []

    def get_points(self, measurement_name, database):
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
                    "time": row["timestamp"],  # Timestamp should be in RFC3339 format
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

# Instantiate the handler
handler = InfluxDBHandler(
    host="localhost",
    port=8086,
    username="root",
    password="root",
)

# Test get_databases
print("Testing get_databases()")
databases = handler.get_databases()
print("Databases:", databases)

# Test get_measurements
print("\nTesting get_measurements()")
if databases:
    first_database = databases[0]  # Get the first database for testing
    measurements = handler.get_measurements(first_database)
    print(f"Measurements in '{first_database}':", measurements)
else:
    print("No databases available for testing measurements.")

# Test get_fields
print("\nTesting get_fields()")
if measurements:
    first_measurement = measurements[0]  # Get the first measurement for testing
    fields = handler.get_fields(first_database, first_measurement)
    print(f"Fields in measurement '{first_measurement}' of database '{first_database}':", fields)
else:
    print("No measurements available for testing fields.")

# Test get_points
print("\nTesting get_points()")
if measurements:
    points = handler.get_points(first_measurement, first_database)
    print(f"Points in measurement '{first_measurement}':", points)

# Test ensure_database
print("\nTesting ensure_database()")
test_database_name = "TestDatabase"
handler.ensure_database(test_database_name)
print(f"Ensured existence of database '{test_database_name}'.")

# Test csv_to_influx (Make sure to have a valid CSV file for testing)
# Uncomment and set your own CSV file path
# print("\nTesting csv_to_influx()")
# test_csv_file = "path/to/your/testfile.csv"
# handler.csv_to_influx(test_csv_file, test_database_name)

# Test influx_to_csv (Make sure to have a measurement with data)
"""
print("\nTesting influx_to_csv()")
output_csv_file = "output_data.csv"
handler.influx_to_csv(first_measurement, output_csv_file, first_database)
"""

print("All tests executed.")


"""
InfluxDB Visualization:
+--------------------------+
|       InfluxDB           |
|                          |
|   +-------------------+  |
|   |    Database       |  |
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