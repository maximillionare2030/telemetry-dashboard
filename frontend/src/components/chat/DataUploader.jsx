import React, { useState, useEffect } from "react";
import { fetchInfluxInfo, uploadData } from "../../api/api";

const DataUploader = () => {
const [file, setFile] = useState(null);
const [loading, setLoading] = useState(false);
const [measurements, setMeasurements] = useState([]);

// fetch available measurements from influxdb
useEffect(() => {
    const fetchMeasurements = async () => {
        try {
            const response = await fetchInfluxInfo();
            setMeasurements(response.info.measurements);
        } catch (error) {
            console.error("Error fetching measurements:", error);
        }
    };

    fetchMeasurements();
}, []);

// handle upload
const handleUpload = async () => {
    if (!file) return;

    // create an empty form data object
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
        await uploadData(formData);
        alert("Data uploaded successfully");
        // Refresh measurements list
        const response = await fetchInfluxInfo();
        setMeasurements(response.info.measurements);
    } catch (error) {
        alert("Error uploading data: " + error.message);
    }
    setLoading(false);
};

// return the form
return (
    <div className="container">
        {/* file input */}
        <div className="file-input">
            <i className="fa-solid fa-cloud-arrow-up"></i>
            <p>Upload CSV file</p>
            <input
                type="file"
                accept=".csv"
                // set the file state to the file selected by the user
                onChange={(e) => setFile(e.target.files[0])}
            />
        </div>

        {/* upload button */}
        <button onClick={handleUpload} disabled={loading || !file}>
            {loading ? "Uploading..." : "Upload"}
        </button>
    </div>
);
};

export default DataUploader;
