import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(...registerables, zoomPlugin);

function LineChart({ selectedConfig }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const chartRef = useRef(null);

  useEffect(() => {
    // Fetch data when the selectedConfig prop changes
    const fetchData = async () => {
      setLoading(true);
      try {
        // Simulated data fetching based on selectedConfig
        // Replace this with your actual data fetching logic
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
  }, [selectedConfig]); // Dependency array includes selectedConfig

  // Chart data and options setup
  const chartData = {
    datasets: [
      {
        label: 'Dataset',
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

  console.log('Config:', {selectedConfig})
  return (
    <div style={{ width: '100%', height: '100%' }}>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <Line ref={chartRef} data={chartData} options={options} />
      )}
      <button onClick={() => chartRef.current.resetZoom()} style={{ marginLeft: 'auto' }}>Reset Zoom</button>
    </div>
  );
}

export default LineChart;
