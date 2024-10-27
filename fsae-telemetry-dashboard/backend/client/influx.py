from influxdb_client import InfluxDBClient, Point
from typing import List
from models import MotorData, ControllerData, BatteryData
from .exceptions import InfluxNotAvailableException, BucketNotFoundException, BadQueryException

# InfluxDB client setup
class InfluxDBClientHandler:
    def __init__(self, url: str, token: str, org: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = "OrionBMS"  # Set the bucket name to "OrionBMS"
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api()  # Create a write API instance
        self.write_fake_data()  # Call to write fake data

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
            # create a new data point for each piece of data (syntax for orionbms)
            point = (
                Point(data["measurement"])
                .tag("location", data["tags"]["location"]) # tag data with a location (dataName, dataValue)
                .field("motorSPD", data["fields"].get("motorSPD", None)) # fields represent data to store (dataName, dataValue)
                .field("motorTMP", data["fields"].get("motorTMP", None))
                .field("batteryVOLT", data["fields"].get("batteryVOLT", None))
                .field("batteryTEMP", data["fields"].get("batteryTEMP", None))
                .field("batteryCURR", data["fields"].get("batteryCURR", None))
            )
            self.write_api.write(bucket=self.bucket, record=point)  # Write to the db
        print("Fake data written to InfluxDB.")

    def query_motor_data(self, start_time: str, end_time: str) -> List[MotorData]:
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "motor_data")
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

    def query_battery_data(self, start_time: str, end_time: str) -> List[BatteryData]:
        query = f"""
        from(bucket: "{self.bucket}")
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

    def fetch_recent_data(self):
        """
        Fetch recent data from InfluxDB for the last 10 minutes.
        """
        query = """from(bucket: "OrionBMS")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "measurement1")"""
        
        try:
            tables = self.query_api.query(query, org=self.org)
            for table in tables:
                for record in table.records:
                    print(record)
        except Exception as e:
            print(f"Error fetching recent data: {e}")

    def close(self):
        """Close the InfluxDB client connection."""
        self.client.close()
