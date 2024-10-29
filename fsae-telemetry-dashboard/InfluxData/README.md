#  How to start InfluxDB

#  IN main terminal

cd InfluxData\influxdb/influxdb-1.8.10-1
.\influxd  # start the InfluxDB



# in separate terminal:
# this will start the Influx CLI shell

cd InfluxData\influx
./influx v1 shell



#  How to create new databae:
CREATE DATABASE <database_name>
SHOW databases # shows available databases
use <database_name>

#  Writing to DB with shell:
USE <database_name>
INSERT <measurement_name>,location=us-west, temperature=82

INSERT motorDATA,location=us-west, temperature=82

# Useful commands

DROP DATABASE <database_name>  # drop the database (delete)
clear <database_name>  # clear tables


