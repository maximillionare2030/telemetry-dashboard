import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(...registerables, zoomPlugin);

function LineChart({ component, selectedItems }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const chartRef = useRef(null);

  useEffect(() => {
    // Fetch InfluxDB data when the component prop changes
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch data from FastAPI
        const response = await fetch(`http://localhost:8000/api/influx/get/info`);
        const result = await response.json();

        // Extract data for the chart, assuming your API returns the structure you need
        const chartData = result.info.databases.map((db) => {
          return {
            x: db.someFieldX, // Replace with the actual field for x-axis
            y: db.someFieldY, // Replace with the actual field for y-axis
          };
        });

        setData(chartData);
      } catch (error) {
        console.error("Error fetching data: ", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [component]);

  // Chart data and options setup
  const chartData = {
    datasets: [
      {
        label: `${String(component)}`,
        data: data,
        borderColor: 'steelblue',
        backgroundColor: 'rgba(70, 130, 180, 0.2)',
        borderWidth: 2,
        parsing: {
          xAxisKey: 'x',
          yAxisKey: 'y',
        },
      },
      {
        label: `Voltage`,
        data: data,
        borderColor: 'steelblue',
        backgroundColor: 'rgba(70, 130, 180, 0.2)',
        borderWidth: 2,
        parsing: {
          xAxisKey: 'x',
          yAxisKey: 'y',
        },
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
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

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <Line ref={chartRef} data={chartData} options={options} />
      <button onClick={() => chartRef.current.resetZoom()} ml="auto">Reset Zoom</button>
    </div>
  );
}

export default LineChart;
