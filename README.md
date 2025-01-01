# FSAE Telemetry Dashboard
Visualize telemetry data from the race car in real time, as the race happens. The dashboard performs the following functions:
1. Visualize time series data for Kilozott
2. Forecast errors in historic racing data (ex: from previous laps)
3. Make decisions with an intelligent chatbot trained with context from previous Formula Races and FSAE guidelines

<hr/>

Download all dependencies
```pip install -r requirements.txt```

## Terminal 1: Run InfluxDB (localhost:8086)

### Inilialize DB
Open a new terminal and run:
```cd ~/telemetry-dashboard/InfluxData/influxdb/influxdb-1.8.10-1```
```./usr/bin/influx```

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
`INSERT motorData,location=us-west, temperature=82` <br/>
In general, the following command is used to write to a database: <br/>
`INSERT <measurement_name>,<tag_name>=<tag_value>,<field_name>=<field_value>` <br/>

Check what is inside of the database:
`SHOW MEASUREMENTS` will show the measurements in the database (ex: motorData, controllerData, etc.) <br/>
`SHOW FIELD KEYS ON <measurement_name>` will show the fields and field type of the measurement <br/>
`SHOW TAG KEYS ON <measurement_name>` will show the tags and tag type of the measurement <br/>
`SELECT * FROM <measurement_name> LIMIT 10` will show the first 10 rows of the measurement <br/>

<br/>

example: 
`SELECT * FROM "Kilozott_Dummy_Data" LIMIT 10`

### Useful commands
`DROP DATABASE <database_name>`  # drop the database (delete) <br/>
`clear <database_name>`  # clear tables <br/>

<br/>

## Terminal 2: Run the backend (localhost:8000)

### Run the initialization script to upload data to the database.
In a new terminal:
```python backend/scripts/init_data.py```

### Start the backend server
In a new terminal:
```python backend/main.py```

or
```uvicorn backend.main:app --reload```


## Terminal 3: Run the frontend (localhost:3000)
```cd frontend``` 
```npm run start```

The default endpoint is `localhost:3000/home`
