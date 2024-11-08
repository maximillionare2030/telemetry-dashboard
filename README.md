# The following program utilizes a FastAPI backend and ReactJS frontend
Make sure to install InfluxDB separately using this [website](https://www.influxdata.com/downloads/).

## 1. Install required dependencies
    
pip install -r requirements.txt
npm install package.json

In order to successfully run the development build of the dashboard do the following in separate terminals:

- Terminal 1: Start the backend (localhost:8000)

cd backend
python main.py runserver

#Terminal 2: Start the Frontend (localhost:3000)

cd frontend
npm start

#Terminal 3: Start the InfluxDB Engine (localhost:8086)

cd InfluxData\influxdb/influxdb-1.8.10-1
.\influxd  # start the InfluxDB



#When all three are running, visit localhost:3000 and choose

1.Database
2.Measurement
3.Fieldset

#To display relevant data


