from influxdb_client import InfluxDBClient
from typing import List
from models import MotorData, ControllerData, BatteryData
from .influx import InfluxNotAvailableException, BucketNotFoundException, BadQueryException

# InfluxDB client setup
class InfluxDBClientHandler:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.query_api = self.client.query_api()

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

    def query_battery_data(self, start_time: str, end_time: str) -> List[BatteryData]:
        # This function queries the InfluxDB database for battery data within a specified time range.
        # It constructs a Flux query, sends it to the InfluxDB server, and processes the response.
        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: {start_time}, stop: {end_time})
        |> filter(fn: (r) => r["_measurement"] == "battery_data")
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
