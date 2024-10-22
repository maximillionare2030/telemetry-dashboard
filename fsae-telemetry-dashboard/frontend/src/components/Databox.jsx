import React, {useEffect, useState} from 'react';

const DataBox = ({ measurement }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // fetch data independently
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/data/${measurement}`);
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
   
            <h1>{measurement}</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre> {/* displays data in readable format */}
        </div>
    );
};

export default DataBox;
