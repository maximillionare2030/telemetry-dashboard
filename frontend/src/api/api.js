// handle api requests to the backend

export const fetchInfluxInfo = async () => {
    try {
        const response = await fetch('http://localhost:8000/api/influx/get/info');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return {
            info: {
                measurements: data.info?.measurements || [],
                fields: data.info?.fields || {}
            }
        };
    } catch (error) {
        console.error('Error fetching InfluxDB info:', error);
        throw error;
    }
};

export const fetchPoints = async (measurementName) => {
    /**
     * @api To fetch points from InfluxDB (JSON format)
     */
    const response = await fetch('http://localhost:8000/api/influx/get/points', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            measurement_name: measurementName,
        }),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // This should return the data in JSON format
};

export const uploadData = async (file) => {
    /**
     * @api to upload data to InfluxDB with user provided params (file, database)
     */
    const formData = new FormData();
    formData.append('file', file);

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

export const analyzeData = async (message) => {
    try {
        // send message from user to the backend
        const response = await fetch('http://localhost:8000/api/analysis/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        console.log("response from backend after processing user message: ", response);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        // return the analysis results in JSON format
        const data = await response.json();
        if (!data.analysis) {
            throw new Error('No analysis results available');
        }

        return data;
    } catch (error) {
        console.error('Analysis error:', error);
        throw error;
    }
};

export const fetchMeanData = async () => {
    /**
     * @api to fetch mean of the data from influxdb
     */
    try {
        const response = await fetch('http://localhost:8000/api/influx/get/mean');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // return the response in JSON format
        return response.json();
    } catch (error) {
        console.error('Error fetching mean data:', error);
        throw error;
    }
};