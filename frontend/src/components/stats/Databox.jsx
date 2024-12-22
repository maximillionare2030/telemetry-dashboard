import { useState, useEffect } from 'react';
import { fetchMeanData } from '../../api/api';

const Databox = () => {
    /**
     * @param {string} title - the title of the databox item (ex: motor speed)
     * @param {number} value - the value of the databox item (ex: 1000)
     */
    const [aggregates, setAggregates] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // fetch data from the backend
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMeanData();
                setAggregates(data);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    // states
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="container databox">
            {/* map over aggregates and create a databox item for each */}
            {Object.entries(aggregates).map(([title, value]) => (
                <div key={title} className="databox-item">
                    <div className="subheading">{title}</div>
                    <div className="number">
                        {typeof value === 'number' ? value.toFixed(2) : value}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Databox;