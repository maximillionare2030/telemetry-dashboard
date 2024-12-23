import React, { useEffect, useState } from 'react';
import { TimeSeries, DrawStyle } from '@grafana/ui';
import { dateTime } from '@grafana/data';
import { fetchTimeRange, fetchTimeSeriesData, extractSelectedConfig } from '../../api/api';

const formatTimeSeriesData = (points) => {
    /**
     * @param {Array} points - the points to format
     * @returns {Array} - points formatted for the time series
     */
    if (!Array.isArray(points)) return [];
    
    // Create a series for each field
    const fields = Object.keys(points[0] || {}).filter(key => key !== 'time');
    
    // format data into a time series for each field
    return fields.map(field => ({
        label: field,
        data: points.map(point => ({
            time: new Date(point.time).getTime(),
            value: point[field]
        }))
    }));
};

const Timeseries = ({ selectedConfig }) => {
    /**
     * @param {Object} selectedConfig - configurations for the timeseries (ex: measurement, fields, etc.)
     */
    // set the time range
    const [timeRange, setTimeRange] = useState(null);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // initialize the time range
    useEffect(() => {
        if (!selectedConfig) {
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                // Use existing fetchTimeSeriesData instead of batch
                const timeRangeData = await fetchTimeRange();
                setTimeRange({
                    from: dateTime(timeRangeData.earliest),
                    to: dateTime(timeRangeData.latest)
                });

                const { measurement, fields } = extractSelectedConfig(selectedConfig);
                const timeSeriesData = await fetchTimeSeriesData(
                    measurement,
                    fields,
                    timeRangeData.earliest,
                    timeRangeData.latest
                );
                
                const formattedData = formatTimeSeriesData(timeSeriesData.points);
                setData(formattedData);
            } catch (error) {
                console.error('Error in fetchData:', error);
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const pollInterval = setInterval(fetchData, 1000);
        return () => clearInterval(pollInterval);
    }, [selectedConfig]);

    if (!selectedConfig) return <div>No configuration selected</div>;
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <TimeSeries
            data={data}
            timeRange={timeRange}
            timeZone="browser"
            width="100%"
            height="100%"
            options={{
                drawStyle: DrawStyle.Line,
                lineWidth: 1,
                fillOpacity: 0.1,
                showPoints: 'never',
                pointSize: 5,
                minStep: 1,
                gradientMode: 'opacity',
            }}
        />
    );
};

export default Timeseries;