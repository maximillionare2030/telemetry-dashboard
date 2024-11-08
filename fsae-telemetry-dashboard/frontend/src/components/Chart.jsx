import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import 'chartjs-adapter-date-fns'; // Import the date adapter
import { fetchPoints } from '../api/api';


Chart.register(...registerables, zoomPlugin);

function LineChart({ selectedConfig }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!selectedConfig) return;

    const config = extractSelectedConfig(selectedConfig);
    if (config.error) {
      setError(config.error);
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await fetchPoints(config.database, config.measurement);
        const chartData = formatChartData(result.points, config.fields);
        setData(chartData);
      } catch (error) {
        setError(error.message);
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedConfig]);

  const extractSelectedConfig = (config) => {
    if (!config || !config.databases) {
      console.error("No databases found in the config.");
      return { error: "No databases found." };
    }

    const database = Object.values(config.databases).find(db => db.isSelected && db.measurements);
    if (!database) {
      console.error("No selected database with measurements found.");
      return { error: "No selected database with measurements found." };
    }

    const measurement = Object.values(database.measurements).find(meas => meas.isSelected && meas.fields);
    if (!measurement) {
      console.error("No selected measurement with fields found.");
      return { error: "No selected measurement with fields found." };
    }

    const selectedFields = Object.keys(measurement.fields).filter(field => measurement.fields[field].isSelected);
    if (selectedFields.length === 0) {
      console.error("No selected fields found.");
      return { error: "No selected fields found." };
    }

    return {
      database: database.name,
      measurement: measurement.name,
      fields: selectedFields
    };
  };

  const formatChartData = (points, fields) => {
    return fields.map((field) => ({
      label: field,
      data: points.map((point) => ({
        x: new Date(point.time),
        y: point[field],
      })),
      borderColor: getRandomColor(),
      fill: false,
    }));
  };

  const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'minute',
        },
      },
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'x',
        },
      },
    },
  };

  return (
    <div style={{ width: '100%', height: '100%' }}>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading ? (
        <p>Loading...</p>
      ) : data.length > 0 ? (
        <>
          <Line ref={chartRef} data={{ datasets: data }} options={options} />
          <button onClick={() => chartRef.current.resetZoom()}>Reset Zoom</button>
        </>
      ) : (
        <p>No data available. Please select database, measurement, and fields.</p>
      )}
    </div>
  );
}

export default LineChart;
