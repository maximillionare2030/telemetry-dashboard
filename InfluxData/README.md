#  Run InfluxDB

###  Start InfluxDB
`./usr/bin/influxd -config influxdb.conf`

### Initialize DB
Open a new terminal and run:
`cd ~/telemetry-dashboard/InfluxData/influxdb/influxdb-1.8.10-1`
`./usr/bin/influx`

In the same terminal, run the following to create a local database:
`CREATE DATABASE telemetry`
In general, the following command is used to create a database:
`CREATE DATABASE <database_name>`

Check the available databases:
`SHOW databases`

Switch to the database:
`USE telemetry`
In general, the following command is used to switch to a database:
`USE <database_name>`

Write to the database:
`INSERT motorData,location=us-west, temperature=82`
In general, the following command is used to write to a database:
`INSERT <measurement_name>,<tag_name>=<tag_value>,<field_name>=<field_value>`

Check what is inside of the database:
`SHOW MEASUREMENTS` will show the measurements in the database (ex: motorData, controllerData, etc.)
`SHOW FIELD KEYS ON <measurement_name>` will show the fields and field type of the measurement
`SHOW TAG KEYS ON <measurement_name>` will show the tags and tag type of the measurement
`SELECT * FROM <measurement_name> LIMIT 10` will show the first 10 rows of the measurement

### Useful commands
DROP DATABASE <database_name>  # drop the database (delete)
clear <database_name>  # clear tables

# Run the backend

### Run the initialization script to upload data to the database.
In a new terminal:
`python backend/scripts/init_data.py`

### Start the backend server
In a new terminal:
`python backend/main.py` 
or
`uvicorn backend.main:app --reload`
