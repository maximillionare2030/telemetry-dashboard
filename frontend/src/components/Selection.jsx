// selection component to select database, measurement, and fields
import React from "react";
import { Select, FormControl, FormLabel, Stack } from "@chakra-ui/react";

function Selection({ databases = [], selectedConfig = { databases: {} }, onConfigChange }) { 
  /**
   * databases is the list of databases fetched from the API
   *  selectedConfig is the selected configuration passed to the chart component
   * onConfigChange is the function to update the selected configuration
   */
  if (!databases || !Array.isArray(databases)) {
    return <div>Loading databases...</div>;
  }

  // handles access to the database
  const handleDatabaseChange = (dbName) => {
    if (!dbName) return;
    
    // tags the selected database based on the selected database name
    const newConfig = {
      databases: {
        
        ...selectedConfig.databases, // copies all existing databases
        [dbName]: { 
          ...selectedConfig.databases[dbName],
          isSelected: true,
          name: dbName,
          measurements: selectedConfig.databases[dbName]?.measurements || {}
        }
      }
    };

    // Deselect other databases
    Object.keys(newConfig.databases).forEach((db) => {
      if (db !== dbName) {
        newConfig.databases[db] = { 
          ...newConfig.databases[db], 
          isSelected: false 
        };
      }
    });
    onConfigChange(newConfig);
  };

  const handleMeasurementChange = (dbName, measurementName) => {
    if (!dbName || !measurementName) return;

    const newConfig = {
      databases: {
        ...selectedConfig.databases,
        [dbName]: {
          ...selectedConfig.databases[dbName],
          measurements: {
            ...selectedConfig.databases[dbName]?.measurements,
            [measurementName]: {
              isSelected: true,
              name: measurementName,
              fields: selectedConfig.databases[dbName]?.measurements?.[measurementName]?.fields || {}
            }
          }
        }
      }
    };
    onConfigChange(newConfig);
  };

  const handleFieldChange = (dbName, measurementName, fieldName) => {
    if (!dbName || !measurementName || !fieldName) return;

    const currentDb = selectedConfig.databases[dbName] || {};
    const currentMeasurement = currentDb.measurements?.[measurementName] || {};
    
    const newConfig = {
      databases: {
        ...selectedConfig.databases,
        [dbName]: {
          ...currentDb,
          measurements: {
            ...currentDb.measurements,
            [measurementName]: {
              ...currentMeasurement,
              fields: {
                ...currentMeasurement.fields,
                [fieldName]: {
                  isSelected: !currentMeasurement.fields?.[fieldName]?.isSelected,
                  name: fieldName
                }
              }
            }
          }
        }
      }
    };
    onConfigChange(newConfig);
  };

  const selectedDb = Object.keys(selectedConfig.databases || {}).find(
    db => selectedConfig.databases[db]?.isSelected
  );

  return (
    <Stack spacing={4} p={4}>
      <FormControl p={4}>
        <FormLabel fontSize="lg">Database</FormLabel>
        <Select
          placeholder="Select database"
          onChange={(e) => handleDatabaseChange(e.target.value)}
          value={selectedDb || ''}
          p={2}
        >
          {databases.map((db) => (
            <option key={db} value={db}>
              {db}
            </option>
          ))}
        </Select>
      </FormControl>

      {selectedDb && (
        <FormControl>
          <FormLabel>Measurement</FormLabel>
          <Select
            placeholder="Select measurement"
            onChange={(e) => handleMeasurementChange(selectedDb, e.target.value)}
            value={Object.keys(selectedConfig.databases[selectedDb]?.measurements || {}).find(
              m => selectedConfig.databases[selectedDb]?.measurements[m]?.isSelected
            ) || ''}
          >
            {selectedConfig.databases[selectedDb]?.measurements && 
              Object.keys(selectedConfig.databases[selectedDb].measurements).map((measurementName) => (
                <option key={measurementName} value={measurementName}>
                  {measurementName}
                </option>
              ))}
          </Select>
        </FormControl>
      )}

      {selectedDb && (
        <FormControl>
          <FormLabel>Fields</FormLabel>
          <Select
            placeholder="Select fields"
            multiple
            onChange={(e) => {
              const selectedFields = Array.from(e.target.selectedOptions, option => option.value);
              handleFieldChange(selectedDb, selectedFields);
            }}
          >
            {selectedConfig.databases[selectedDb]?.measurements && 
              Object.keys(selectedConfig.databases[selectedDb].measurements).map((measurementName) => (
                <option key={measurementName} value={measurementName}>
                  {measurementName}
                </option>
              ))}
          </Select>
        </FormControl>
      )}
    </Stack>
  );
}

export default Selection;
