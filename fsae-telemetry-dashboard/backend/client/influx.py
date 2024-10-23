from influxdb_client import InfluxDBClient
from typing import List
from models import MotorData, ControllerData, BatteryData
from .exceptions import InfluxNotAvailableException, BucketNotFoundException, BadQueryException

# InfluxDB client setup
class InfluxDBClientHandler:
    def __init__(self, url: str, token: str, org: str):
        self.url = url
        self.token = token
        self.org = org
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.query_api = self.client.query_api()
        self.write_fake_data()  # Call to write fake data

    def query_motor_data(self, start_time: str, end_time: str) -> List[MotorData]:
        # This function queries the InfluxDB database for motor data within a specified time range.
        # It constructs a Flux query, sends it to the InfluxDB server, and processes the response.
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "motor_data")
        |> yield(name: "mean")
        """
        try:
            result = self.query_api.query(query)
            motor_data_list = []
            for table in result:
                for record in table.records:
                    motor_data_list.append(
                        MotorData(
                            motorSPD=record.get_value() if record.get_field() == "motorSPD" else None,
                            motorTMP=record.get_value() if record.get_field() == "motorTMP" else None
                        )
                    )
            return motor_data_list
        except Exception as e:
            raise BadQueryException() from e

    def query_controller_data(self, start_time: str, end_time: str) -> List[ControllerData]:
        # This function queries the InfluxDB database for controller data within a specified time range.
        # It constructs a Flux query, sends it to the InfluxDB server, and processes the response.
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "controller_data")
        """
        try:
            result = self.query_api.query(query)
            controller_data_list = []
            for table in result:
                for record in table.records:
                    controller_data_list.append(
                        ControllerData(
                            controllerTMP=record.get_value() if record.get_field() == "controllerTMP" else None
                        )
                    )
            return controller_data_list
        except Exception as e:
            raise BadQueryException() from e

    def query_battery_data(self, start_time: str, end_time: str, bucket: str) -> List[BatteryData]:
        query = f"""
        from(bucket: "{bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "battery_data")
        |> filter(fn: (r) => r["_field"] == "batteryVOLT" or r["_field"] == "batteryTEMP" or r["_field"] == "batteryCURR")
        """
        try:
            result = self.query_api.query(query)
            battery_data_list = []
            for table in result:
                for record in table.records:
                    battery_data_list.append(
                        BatteryData(
                            batteryVOLT=record.get_value() if record.get_field() == "batteryVOLT" else None,
                            batteryTEMP=record.get_value() if record.get_field() == "batteryTEMP" else None,
                            batteryCURR=record.get_value() if record.get_field() == "batteryCURR" else None
                        )
                    )
            return battery_data_list
        except Exception as e:
            raise BadQueryException() from e

def write_fake_data(self):
    """
    Write fake data to InfluxDB.
    This is fake data for testing purposes only.
    """
    fake_data = [
        # Motor Data
        {
            "measurement": "motor_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T00:00:00Z",
                "end_time": "2023-10-01T01:00:00Z",
                "value": 1500,  # Example motor speed
                "type": "motor"
            }
        },
        {
            "measurement": "motor_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T01:00:00Z",
                "end_time": "2023-10-01T02:00:00Z",
                "value": 1600,  # Example motor speed
                "type": "motor"
            }
        },
        {
            "measurement": "motor_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T02:00:00Z",
                "end_time": "2023-10-01T03:00:00Z",
                "value": 1550,  # Example motor speed
                "type": "motor"
            }
        },
        {
            "measurement": "motor_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T03:00:00Z",
                "end_time": "2023-10-01T04:00:00Z",
                "value": 1580,  # Example motor speed
                "type": "motor"
            }
        },
        {
            "measurement": "motor_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T04:00:00Z",
                "end_time": "2023-10-01T05:00:00Z",
                "value": 1620,  # Example motor speed
                "type": "motor"
            }
        },

        # Controller Data
        {
            "measurement": "battery_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T00:00:00Z",
                "end_time": "2023-10-01T01:00:00Z",
                "value": 80, 
                "type": "battery"
            }
        },
        {
            "measurement": "battery_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T01:00:00Z",
                "end_time": "2023-10-01T02:00:00Z",
                "value": 82,  
                "type": "battery"
            }
        },
        {
            "measurement": "battery_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T02:00:00Z",
                "end_time": "2023-10-01T03:00:00Z",
                "value": 79,  # Example controller temperature
                "type": "battery"
            }
        },
        {
            "measurement": "battery_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T03:00:00Z",
                "end_time": "2023-10-01T04:00:00Z",
                "value": 81,  # Example controller temperature
                "type": "battery"
            }
        },
        {
            "measurement": "battery_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                "start_time": "2023-10-01T04:00:00Z",
                "end_time": "2023-10-01T05:00:00Z",
                "value": 83,  # Example controller temperature
                "type": "battery"
            }
        }
    ]
    
    for data in fake_data:
        self.client.write_api().write(bucket = bucket, record = data) # write to the db
    print("Fake data written to InfluxDB.")

def fetch_data():
    """
    Fetch data from InfluxDB.
    """
    query = 'SELECT * FROM temperature'
    result = client.query(query)
    return list(result.get_points())
