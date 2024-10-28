import pandas as pd
from influxdb import InfluxDBClient

# Step 1: Create a connection to the InfluxDB server
client = InfluxDBClient(host='localhost', port=8086)
database_name = 'dummy_data'  # Replace with your database name
client.switch_database(database_name)

# Step 2: Read the CSV file into a DataFrame  ** CHANGE TO DIRECT PATH ON YOUR DEVICE **
df = pd.read_csv('C:\\Users\\User\\Desktop\\School and Life\\EV\\HCI\\fsae-telemetry-dashboard\\backend\\client\\vehicle_data\\Kilozott_Dummy_Data.csv')

# Step 3: Prepare the JSON body for InfluxDB
json_body = []

# Get the column names for tags and fields
tags = []  # List for any tags if needed
fields = df.columns[1:]  # All columns except the timestamp
measurement_name = "motor_data"  # Name of the measurement

for index, row in df.iterrows():
    entry = {
        "measurement": f"{measurement_name}",  # Replace with your measurement name
        "time": row['timeStamp'],  # Use the timestamp column
        "tags": {tag: row[tag] for tag in tags},  # If you have tags, populate them here
        "fields": {field: row[field] for field in fields}  # All other columns are fields
    }
    json_body.append(entry)



# Step 4: Write data to InfluxDB
print(client.write_points(json_body))

print("Data written successfully to InfluxDB.")


# Step 5: Query data from the database
query = f'SELECT * FROM {measurement_name}'
result = client.query(query)

# Step 6: Process the results
points = list(result.get_points())
for point in points:
    print(point)