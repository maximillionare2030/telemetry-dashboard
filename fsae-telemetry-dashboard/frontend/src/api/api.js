// api.js
const API_BASE_URL = "http://localhost:8000/api";

export const getInfluxInfo = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/influx/get/info`);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch InfluxDB info:", error);
        throw error; // Re-throw the error for further handling if needed
    }
};

// Other API functions can be added here
