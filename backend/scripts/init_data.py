import os
from pathlib import Path
from influxdb import InfluxDBClient
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """ 
    Initialize a local db on a influxdb server
    """
    try:
        client = InfluxDBClient(
            host='localhost',
            port=8086,
            username='',
            password='',
            database='telemetry',
            ssl=False
        )

        # Create database if it doesn't exist
        databases = client.get_list_database()
        if not any(db['name'] == 'telemetry' for db in databases):
            client.create_database('telemetry')
            logger.info("Created database: telemetry")
        
        client.switch_database('telemetry')

        # Get the data directory
        data_dir = Path(__file__).parent.parent.parent / 'data'
        
        for csv_file in data_dir.glob('*.csv'):
            logger.info(f"Processing file: {csv_file}")
            df = pd.read_csv(csv_file)
            measurement_name = csv_file.stem

            # Write points in batches
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch_df = df.iloc[i:i+batch_size]
                json_body = []
                
                for _, row in batch_df.iterrows():
                    json_body.append({
                        "measurement": measurement_name,
                        "time": row.iloc[0],
                        "fields": {field: row[field] for field in df.columns[1:]}
                    })
                
                client.write_points(json_body)
                logger.info(f"Uploaded batch of {len(json_body)} points to {measurement_name}")

        return True
    except Exception as e:
        logger.error(f"Error uploading data: {e}")
        return False

if __name__ == "__main__":
    init_database()
