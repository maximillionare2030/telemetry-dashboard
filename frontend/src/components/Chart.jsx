import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import 'chartjs-adapter-date-fns'; // Import the date adapter
import { fetchPoints } from '../api/api';
import Skeleton from '../components/Skeleton';

Chart.register(...registerables, zoomPlugin);

function LineChart({ selectedConfig }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const chartRef = useRef(null);

  useEffect(() => {
    /**
     * useEffect gets the selectedConfig and passes parameters to API fetch functions
     */
    if (!selectedConfig) return;

    const config = extractSelectedConfig(selectedConfig);
    if (!config || !config.database || !config.measurement || config.fields.length === 0) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await fetchPoints(config.database, config.measurement);
        const chartData = formatChartData(result.points, config.fields);
        setData(chartData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedConfig]);

  const extractSelectedConfig = (config) => {
    /**
     * Function to receive selectedConfig from JSON object selectedConfig
     */
    if (!config || !config.databases) return {};
    for (const db in config.databases) {
      const database = config.databases[db];
      if (database.isSelected && database.measurements) {
        for (const meas in database.measurements) {
          const measurement = database.measurements[meas];
          if (measurement.isSelected && measurement.fields) {
            const selectedFields = Object.keys(measurement.fields).filter(
              (field) => measurement.fields[field].isSelected
            );
            if (selectedFields.length > 0) {
              return { database: db, measurement: meas, fields: selectedFields };
            }
          }
        }
      }
    }
    return {};
  };

  const formatChartData = (points, fields) => {
    /***
     * Add dataset to CHARTJS chart
     */
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
    /**
     * Generate a random color HEX code, to be passed to chart data
     */
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
      {loading ? (
        <Skeleton/>
      ) : (
        <Line ref={chartRef} data={{ datasets: data }} options={options} />
      )}
      {/* <button onClick={() => chartRef.current.resetZoom()} style={{ marginLeft: 'auto' }}>Reset Zoom</button> */}
    </div>
  );
}

export default LineChart;