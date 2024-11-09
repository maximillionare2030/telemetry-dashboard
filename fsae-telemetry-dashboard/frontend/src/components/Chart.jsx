import React, { useEffect, useRef, useState } from "react";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import { fetchPoints, fetchInfluxInfo } from "../api/api";
import Selection from "./Selection";
import { Box, VStack, Text } from "@chakra-ui/react";

function LineChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);
  const [selectedConfig, setSelectedConfig] = useState({
    databases: {}
  });
  const [databases, setDatabases] = useState([]);
  const [rawData, setRawData] = useState(null);

  // Fetch available databases on component mount
  useEffect(() => {
    const fetchDatabases = async () => {
      try {
        const response = await fetchInfluxInfo();
        console.log("=== Database Information ===");
        console.log("Raw response:", response);
        
        // Convert database object to array if needed
        const dbArray = Array.isArray(response.info.databases) 
          ? response.info.databases 
          : Object.values(response.info.databases);
        
        setDatabases(dbArray);
        setRawData(response);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching databases:", error);
        setError("Failed to load databases");
        setLoading(false);
      }
    };
    fetchDatabases();
  }, []);

  useEffect(() => {
    const config = extractSelectedConfig(selectedConfig);
    if (config.error) {
      setError(config.error);
      setLoading(false);
      return;
    }

    if (!config.database || !config.measurement) return;

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

  // extract the selected config from the config object
  const extractSelectedConfig = (config) => {
    if (!config || !config.databases) {
      console.error("No databases found in the config.");
      return { error: "No databases found." };
    }

    // Convert to array and find selected database
    const databaseArray = Array.from(Object.values(config.databases));
    const database = databaseArray.find(db => db.isSelected);
    
    if (!database || !database.measurements) {
      console.error("No selected database with measurements found.");
      return { error: "No selected database with measurements found." };
    }

    // Convert measurements to array and find selected measurement
    const measurementArray = Array.from(Object.values(database.measurements));
    const measurement = measurementArray.find(meas => meas.isSelected);
    
    if (!measurement || !measurement.fields) {
      console.error("No selected measurement with fields found.");
      return { error: "No selected measurement with fields found." };
    }

    // Convert fields to array and filter selected ones
    const fieldsArray = Array.from(Object.entries(measurement.fields));
    const selectedFields = fieldsArray
      .filter(([_, field]) => field.isSelected)
      .map(([fieldName, _]) => fieldName);

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

  // format the data for the chart
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

  // get a random color to apply to the chart
  const getRandomColor = () => {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: "time",
        time: {
          unit: "minute",
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
          mode: "xy",
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: "x",
        },
      },
    },
  };

  return (
    <>
      <Box p={4} bg="gray.50" borderRadius="md" mb={4}>
        <Text fontSize="xl" fontWeight="bold" mb={2}>Database Information</Text>
        {loading ? (
          <Text>Loading...</Text>
        ) : error ? (
          <Text color="red.500">Error: {error}</Text>
        ) : (
          <VStack align="start" spacing={4}>
            <Box>
              <Text fontWeight="semibold">Available Databases:</Text>
              {databases.length > 0 ? (
                databases.map((db, index) => (
                  <Text key={index} pl={4}>
                    {typeof db === 'string' ? db : JSON.stringify(db)}
                  </Text>
                ))
              ) : (
                <Text pl={4}>No databases found.</Text>
              )}
            </Box>
          </VStack>
        )}
      </Box>

      <VStack spacing={4} width="100%" height="100%">
        <Box width="100%">
          <Selection
            databases={databases}
            selectedConfig={{ databases: {} }}
            onConfigChange={setSelectedConfig}
          />
        </Box>

        <Box width="100%" flex="1">
          {error && <Text color="red.500">{error}</Text>}
          {loading ? (
            <Text>Loading...</Text>
          ) : data.length > 0 ? (
            <>
              <Line
                ref={chartRef}
                data={{ datasets: data }}
                options={options}
              />
              <button onClick={() => chartRef.current.resetZoom()}>
                Reset Zoom
              </button>
            </>
          ) : (
            <Text>
              No data available. Please select database, measurement, and fields.
            </Text>
          )}
        </Box>
      </VStack>
    </>
  );
}

export default LineChart;
