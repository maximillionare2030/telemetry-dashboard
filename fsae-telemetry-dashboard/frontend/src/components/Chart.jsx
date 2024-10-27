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
    // Fetch data when the component prop changes
    const fetchData = async () => {
      setLoading(true);
      try {
        // Use dummy data for testing
        const result = [
          { x: 1, y: 10 },
          { x: 2, y: 15 },
          { x: 3, y: 20 },
          { x: 4, y: 25 },
        ];
        setData(result);
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
          mode: 'xy',
        },
      },
    },
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ width: '100%', height: '100%'}}>
      <Line ref={chartRef} data={chartData} options={options} />
      <button onClick={() => chartRef.current.resetZoom()} ml="auto">Reset Zoom</button>
    </div>
  );
}

export default LineChart;


/*
const response = await fetch(`http://localhost:5000/api/data/${component}`);
const result = await response.json();

*/