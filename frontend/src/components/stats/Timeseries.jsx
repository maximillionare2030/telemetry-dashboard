import React, { useEffect, useState, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import { fetchTimeRange, fetchTimeSeriesData, extractSelectedConfig } from '../../api/api';

const getRandomColor = () => {
    const colors = [
        { 
            // purple
            bg: 'linear-gradient(to bottom, rgba(70, 95, 255, 1), rgba(70, 95, 255, 0))', 
            border: '#465FFF' 
        }, 
        {
            // blue
            bg: `linear-gradient(to bottom, rgba(80, 219, 250, 1), rgba(80, 219, 250, 0))`,
            border: '#50DBFA'
        }
    ]
    return colors[Math.floor(Math.random() * colors.length)];
}

const formatTimeSeriesData = (points) => {
    /**
     * @param {Array} points - the points to format
     * @returns {Array} - points formatted for the time series
     */
    console.log('Raw points:', points);
    
    if (!Array.isArray(points) || points.length === 0) {
        return { datasets: [] };
    }
    
    // Create a series for each field
    const fields = Object.keys(points[0] || {}).filter(key => key !== 'time');
    console.log('Fields found:', fields);
    
    const datasets = fields.map(field => {
        const color = getRandomColor();
        return {
            label: field,
            data: points.map(point => ({
                x: new Date(point.time).getTime(), // Convert to timestamp
                y: parseFloat(point[field]) || 0
            })),
            backgroundColor: color.bg,
            borderColor: color.border,
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 2,
            pointHoverRadius: 5
        };
    });

    return { datasets };
};

const Timeseries = ({ selectedConfig }) => {
    /**
     * @param {Object} selectedConfig - configurations for the timeseries (ex: measurement, fields, etc.)
     */
    const [data, setData] = useState({ datasets: [] }); // store time series data in a json object
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const chartRef = useRef(null);

    // fetch data when selected config changes
    useEffect(() => {
        if (!selectedConfig) {
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                setLoading(true);
                
                // fetch time range
                const timeRangeData = await fetchTimeRange();
                if (!timeRangeData?.earliest || !timeRangeData?.latest) {
                    throw new Error('Invalid time range received');
                }
                console.log('Time range data successfully fetched:', timeRangeData);

                // extract selected config
                const { measurement, fields } = extractSelectedConfig(selectedConfig);
                if (!measurement || !fields?.length) {
                    throw new Error('Invalid configuration');
                }
                console.log('Selected configuration successfully extracted:', { measurement, fields });
                // fetch time series data
                const timeSeriesData = await fetchTimeSeriesData(
                    measurement,
                    fields,
                    timeRangeData.earliest, 
                    timeRangeData.latest
                );
                console.log('Time series data points:', timeSeriesData.points);

                if (!timeSeriesData?.points || !Array.isArray(timeSeriesData.points)) {
                    throw new Error('Invalid time series data received');
                }

                if (timeSeriesData.points.length === 0) {
                    console.warn('No data points received from API');
                }

                // format data
                const formattedData = formatTimeSeriesData(timeSeriesData.points);
                console.log('Formatted data:', formattedData);
                // set the config data
                setData(formattedData);

                console.log('Successfully formatted data:', formattedData);
            } catch (error) {
                console.error('Error in fetchData:', error);
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [selectedConfig]);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                    displayFormats: {
                        second: 'HH:mm:ss'
                    }
                }
            },
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'x'
                },
                zoom: {
                    wheel: { enabled: true },
                    pinch: { enabled: true },
                    mode: 'x'
                }
            }
        }
    };

    if (!selectedConfig) return <div>No configuration selected</div>;
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="container timeseries">
            {loading && <div>Loading...</div>}
            {error && <div>Error: {error.message}</div>}
            {!loading && !error && (
                <Line
                    ref={chartRef}
                    data={data}
                    options={options}
                    className="chart"
                />
            )}
        </div>
    );
};

export default Timeseries;