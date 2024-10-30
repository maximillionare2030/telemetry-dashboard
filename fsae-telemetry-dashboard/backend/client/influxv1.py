from influxdb import InfluxDBClient
import pandas as pd

class InfluxDBHandler(object):
    def __init__(self, host, port, username, password, database):
        self.client = InfluxDBClient(host=host, port=port, username=username, password=password)
        self.database = database

        try:
            # Check if database exists, and create if it doesn't
            databases = self.client.get_list_database()
            if not any(db['name'] == database for db in databases):
                self.client.create_database(database)
            self.client.switch_database(database)
            print(f"Successfully connected to database: {database}")
        except Exception as e:
            print(f"Error connecting to database '{database}': {e}")

    def csv_to_influx(self, filename):
        try:
            # Ensure the client is switched to the target database
            self.client.switch_database(self.database)

            # Read CSV
            df = pd.read_csv(filename)
            measurement_name = filename.split("\\")[-1][:-4]  # Use filename for measurement name without .csv extension
            print(f"Measurement_name: {measurement_name}")
            json_body = []
            fields = df.columns[1:]  # Exclude timestamp column

            for _, row in df.iterrows():
                json_body.append({
                    "measurement": measurement_name,
                    "time": row["timestamp"],  # Already in RFC3339 format
                    "fields": {
                        field: row[field] for field in fields
                    }
                })

            # Write to InfluxDB
            self.client.write_points(json_body)
            print("Data written successfully to InfluxDB.")

            # Query data and print to verify
            query = f'SELECT * FROM "{measurement_name}"'
            result = self.client.query(query)
            points = list(result.get_points())
            for point in points:
                print(point)

        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

    def influx_to_csv(self, measurement_name, output_filename):
        try:
            # Query data from the specified measurement
            query = f'SELECT * FROM "{measurement_name}"'
            result = self.client.query(query)
            
            # Convert query result to a list of points
            points = list(result.get_points())
            
            # If there are no data points, exit early
            if not points:
                print(f"No data found in measurement '{measurement_name}'")
                return

            # Convert points to a DataFrame
            df = pd.DataFrame(points)

            # Export DataFrame to CSV
            df.to_csv(output_filename, index=False)
            print(f"Data exported successfully to {output_filename}")

        except Exception as e:
            print(f"Error exporting data from measurement '{measurement_name}': {e}")

# Instantiate the handler


# Call the csv_to_influx method to test
#handler.csv_to_influx("C:\\Users\\User\\Desktop\\School and Life\\EV\\HCI\\fsae-telemetry-dashboard\\backend\\client\\vehicle_data\\Kilozott_Dummy_Data.csv")

#handler.influx_to_csv("Kilozott_Dummy_Data", "Kilozott_Dummy_Data_Influx_to_CSV.csv")
