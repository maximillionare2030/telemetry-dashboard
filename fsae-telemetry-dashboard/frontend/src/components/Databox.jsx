import React, {useEffect, useState} from 'react';

const DataBox = ({ measurement }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // fetch data independently
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/data/${measurement}?start_time=-1h&end_time=now()`);
                if (!response.ok) {
                    throw new Error('Network response not working');
                }
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error("Error fetching data: ", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [measurement]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            {/* display data on cards. sample with battery data */}
            <h1>{measurement} Data</h1>
            <ul>
                {data.map((item, index) => (
                    <li key = {index}>
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
                ))}
            </ul>
        </div>
    );
};

export default DataBox;
