import { useState, useEffect } from 'react';
import { fetchMeanData } from '../../api/api';

const Databox = () => {
    /**
     * @param {string} title - the title of the databox item (ex: motor speed)
     * @param {number} value - the value of the databox item (ex: 1000)
     */
    const [aggregates, setAggregates] = useState({});
    const [loading, setLoading] = useState(true);
    const [status, setStatus] = useState({});
    const [error, setError] = useState(null);

    // fetch mean and status from the backend
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMeanData();
                setAggregates(data.means);
                setStatus(data.status);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    // set the state based on the status
    const getStatusComponent = (status) => {
        if (status === 'below') {
            return <div className="subtext" style={{color: '#FF5647'}}>BELOW NOMINAL</div>;
        } else if (status === 'above') {
            return <div className="subtext" style={{color: '#FF5647'}}>ABOVE NOMINAL</div>;
        } else {
            return <div className="subtext" style={{color: '#47FF85'}}>NOMINAL</div>;
        }
    }

    // states
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="container databox">
            <div className="row card-heading">
                <i class="fa-solid fa-chart-line" style={{color: 'white'}}></i>
                <div className="subtext">Average statistics</div>
            </div>
            <div className="databox-items-wrapper">
            {/* map over aggregates and create a databox item for each */}
            {Object.entries(aggregates).map(([title, value]) => (
                <div key={title} className="databox-item">
                    <div>
                        {getStatusComponent(status[title])}
                    </div>
                    <div className="subheading">{title}</div>
                    <div className="number">
                        {typeof value === 'number' ? value.toFixed(2) : value}
                    </div>
                </div>
            ))}
             </div>
        </div>
    );
};

export default Databox;