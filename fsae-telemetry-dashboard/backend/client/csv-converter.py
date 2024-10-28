import csv
import requests

# InfluxDB settings
influxdb_url = 'http://localhost:8086/write?db=your_database_name'  # Change to your database name

# CSV file path
csv_file_path = 'data.csv'  # Change to your CSV file path

# Function to convert CSV to InfluxDB line protocol and insert into InfluxDB
def import_csv_to_influxdb(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = []
        
        for row in reader:
            # Convert each row to InfluxDB line protocol format
            # Assuming 'temperature' and 'humidity' are fields and 'time' is the timestamp
            line = f"weather,location=room temperature={row['temperature']},humidity={row['humidity']} {row['time']}"
            data.append(line)

        # Join all lines and send to InfluxDB
        payload = '\n'.join(data)
        response = requests.post(influxdb_url, data=payload)
        
        if response.status_code == 204:
            print("Data imported successfully.")
        else:
            print(f"Failed to import data: {response.status_code} - {response.text}")

# Call the function
import_csv_to_influxdb(csv_file_path)
