// api/api.js

export const fetchInfluxInfo = async () => {
    const response = await fetch('http://localhost:8000/api/influx/get/info'); // Use the full URL
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // This should return the data in JSON format
};

export const fetchPoints = async (database, measurementName) => {
    const response = await fetch('http://localhost:8000/api/influx/get/points', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            database: database,
            measurement_name: measurementName,
        }),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // This should return the data in JSON format
};
