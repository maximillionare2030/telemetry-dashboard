// handle api requests to the backend

export const fetchInfluxInfo = async () => {
    /***
     * @api To retrieve higher level data from InfluxDB
     */
    const response = await fetch('http://localhost:8000/api/influx/get/info'); // Use the full URL
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // This should return the data in JSON format
};

export const fetchPoints = async (database, measurementName) => {
    /**
     * @api To fetch points from InfluxDB (JSON format)
     */
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

export const uploadData = async (file, database) => {
    /**
     * @api to upload data to InfluxDB with user provided params (file, database)
     */
    const formData = new FormData();
    formData.append('file', file);
    formData.append('database', database);

    // send the form data to the backend
    const response = await fetch('http://localhost:8000/api/influx/upload', {
        method: 'POST',
        body: formData,
    })

    // handle error
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    
    // return the response in JSON format
    return response.json();
}