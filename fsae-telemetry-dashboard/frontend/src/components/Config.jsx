import React, { useEffect, useState } from "react";
import { fetchInfluxInfo } from "../api/api";
import { Checkbox, Box, Text, VStack } from "@chakra-ui/react";

function Config({ onChange }) { // Add onChange as a prop
    const [info, setInfo] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [selectedOptions, setSelectedOptions] = useState({
        databases: {},
    });

    useEffect(() => {
        const getInfo = async () => {
            setLoading(true);
            try {
                const data = await fetchInfluxInfo();
                setInfo(data.info);
            } catch (err) {
                setError("Failed to fetch data");
            } finally {
                setLoading(false);
            }
        };

        getInfo();
    }, []);

    const toggleSelection = (level, dbName, measurementName, field) => {
        setSelectedOptions((prev) => {
            const updated = { ...prev };

            updated.databases[dbName] = updated.databases[dbName] || {
                isSelected: false,
                measurements: {},
            };

            if (level === "database") {
                updated.databases[dbName].isSelected = !updated.databases[dbName].isSelected;
            } else if (level === "measurement") {
                updated.databases[dbName].measurements[measurementName] = updated.databases[dbName].measurements[measurementName] || {
                    isSelected: false,
                    fields: {},
                };
                updated.databases[dbName].measurements[measurementName].isSelected = !updated.databases[dbName].measurements[measurementName].isSelected;
            } else if (level === "field") {
                updated.databases[dbName].measurements[measurementName].fields[field] = updated.databases[dbName].measurements[measurementName].fields[field] || { isSelected: false };
                updated.databases[dbName].measurements[measurementName].fields[field].isSelected = !updated.databases[dbName].measurements[measurementName].fields[field].isSelected;
            }
            return updated;
        });

        // Call onChange to update selectedConfig in the parent
        onChange(selectedOptions);
    };

    return (
        <Box p={4}>
            <Text fontSize="xl" fontWeight="bold">InfluxDB Configuration</Text>
            {error && <Text color="red.500">{error}</Text>}
            {loading ? (
                <Text>Loading...</Text>
            ) : info ? (
                <VStack align="start" spacing={4}>
                    {info.databases.map((dbObj) => {
                        const dbName = Object.keys(dbObj)[0];
                        const measurements = dbObj[dbName].measurements;
                        return (
                            <Box key={dbName}>
                                <Checkbox 
                                    isChecked={selectedOptions.databases[dbName]?.isSelected || false} 
                                    onChange={() => toggleSelection("database", dbName)}
                                >
                                    {dbName}
                                </Checkbox>
                                {selectedOptions.databases[dbName]?.isSelected && (
                                    <VStack align="start" pl={6} spacing={2}>
                                        {Object.entries(measurements).map(([measurementName, fieldsObj]) => (
                                            <Box key={measurementName}>
                                                <Checkbox
                                                    isChecked={selectedOptions.databases[dbName].measurements[measurementName]?.isSelected || false}
                                                    onChange={() => toggleSelection("measurement", dbName, measurementName)}
                                                >
                                                    {measurementName}
                                                </Checkbox>
                                                {selectedOptions.databases[dbName].measurements[measurementName]?.isSelected && (
                                                    <VStack align="start" pl={6} spacing={1}>
                                                        {fieldsObj.fields.map((field) => (
                                                            <Checkbox
                                                                key={field}
                                                                isChecked={selectedOptions.databases[dbName].measurements[measurementName].fields[field]?.isSelected || false}
                                                                onChange={() => toggleSelection("field", dbName, measurementName, field)}
                                                            >
                                                                {field}
                                                            </Checkbox>
                                                        ))}
                                                    </VStack>
                                                )}
                                            </Box>
                                        ))}
                                    </VStack>
                                )}
                            </Box>
                        );
                    })}
                </VStack>
            ) : (
                <Text>No data available</Text>
            )}
        </Box>
    );
}

export default Config;
