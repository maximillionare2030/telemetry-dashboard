# api request to retrieve measurements data 
from flask import Blueprint, jsonify, request
from client.influx import InfluxDBClientHandler
from dotenv import load_dotenv
import os


measurements_bp = Blueprint('measurements', __name__)  # create a blueprint object to store the route to measurements
load_dotenv()
influx_client = InfluxDBClientHandler(url="http://localhost:8086", token=os.getenv("INFLUX_API_KEY"), org=os.getenv("INFLUX_ORG_NAME"))

MEASUREMENT_BUCKETS = {
    'motor_data': 'motor_bucket',
    'battery_data': 'battery_bucket',
}

@measurements_bp.route('/data/<measurement>', methods=['GET'])
def get_measurement_data(measurement):
    # Your logic to fetch data based on the measurement type
    start_time = request.args.get('start_time', '-1h') # set default time to last hour
    end_time = request.args.get('end_time', 'now()')     # set default end time to now

    bucket = MEASUREMENT_BUCKETS.get(measurement)
    if not bucket:
        return jsonify({"error": "Invalid measurement type"}), 400
    
    try:
        if measurement == 'motor_data':
            data = influx_client.query_motor_data(start_time, end_time, bucket)
        elif measurement == 'battery_data':
            data = influx_client.query_controller_data(start_time, end_time, bucket)
        else:
            return jsonify({"error" : "Invalid Measurement Type"}), 400
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
