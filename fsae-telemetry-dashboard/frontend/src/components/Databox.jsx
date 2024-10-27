import React, {useEffect, useState} from 'react';

const DataBox = ({ measurement }) => {
    const [data, setData] = useState([]); // Initialize as an empty array
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // fetch data independently
        const fetchData = async () => {
            try {
                console.log("Fetching data for measurement:", measurement); // Log the measurement
                const response = await fetch(`http://localhost:8000/data/${measurement}?start_time=-1h&end_time=now()`);
                
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                
                const result = await response.json();
                console.log("Fetched data:", result); // Log the fetched data
                setData(result);
            } catch (error) {
                console.error("Fetch error:", error); // Log the error
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [measurement]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>{measurement} Data</h1>
            <ul>
                {data.length > 0 ? (
                    data.map((item, index) => (
                        <li key={index}>
                            {measurement === 'battery_data' ? (
                                <div>
                                    <p>Battery Voltage: {item.batteryVOLT}</p>
                                    <p>Battery Temperature: {item.batteryTEMP}</p>
                                    <p>Battery Current: {item.batteryCURR}</p>
                                </div>
                            ) : (
                                <p>{JSON.stringify(item)}</p> // else display data as a JSON string
                            )}
                        </li>
                    ))
                ) : (
                    <p>No data available for {measurement}.</p>
                )}
            </ul>
        </div>
    );
};

export default DataBox;
