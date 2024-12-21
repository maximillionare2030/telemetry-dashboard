import React, { useState, useEffect } from 'react';
import { fetchInfluxInfo } from '../api/api'

const DataUploader = () => {
    const [file, setFile] = useState(null);
    const [database, setDatabase] = useState('');
    const [loading, setLoading] = useState(false);

    const [availableDatabases, setAvailableDatabases] = useState([]); // list of available databases
    const [showNewDbInput, setShowNewDbInput] = useState(false); // show option to create a new database
    const [newDbName, setNewDbName] = useState(''); // create a new db

    // fetch available databases
    useEffect(() => {
        const fetchDatabases = async () => {
            try {
                const response = await fetchInfluxInfo();
                const databases = response.info.databases.map(db => Object.keys(db)[0]); // get the database names and assign a unique id
            } catch (error) {
                console.error('Error fetching databases:', error);
            }
        };
        
        fetchDatabases();
    }, []);

    // handle upload
    const handleUpload = async () => {
        if (!file || !database) return;

        // create an empty form data object
        const formData = new FormData();
        formData.append('file', file); // add file name
        formData.append('database', database); // add database name

        setLoading(true);

        try {
            // send the form data to the backend containing user input
            const response = await fetch('http://localhost:8000/api/influx/upload', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) throw new Error('upload failed');

            alert('Data uploaded successfully');
        } catch (error) {
            alert('Error uploading data: ' + error.message);
        }
        setLoading(false);
    }

    // return the form
    return(
        <div>
            <h2>Upload Data to InfluxDB</h2>
            {/* file input */}
            <input
                type="file"
                accept=".csv"
                // set the file state to the file selected by the user
                onChange={(e) => setFile(e.target.files[0])}
            />
            {/* database input */}
            {!showNewDbInput ? (
                // show existing databases
                <div>
                    {/* select existing database */}
                    <select
                        value={database} // pulled from available databases
                        onChange={(e) => setDatabase(e.target.value)}
                    >
                        <option value="">Select database</option>
                        {/* map all available databases to options */}
                        {availableDatabases.map(db => (
                            <option
                                key={db}
                                value={db}
                            >
                                {db}
                            </option>
                        ))}

                    </select>
                    {/* create new database */}
                    <button onClick={() => setShowNewDbInput(true)}>
                        Create new database
                    </button>
                </div>
            ) : (
                // create new database
                <div>
                    <input
                        type="text"
                        placeholder="Enter new database name"
                        value={newDbName}
                        onChange={(e) => setNewDbName(e.target.value)}
                    />
                    {/* return to existing databases */}
                    <button onClick={() => setShowNewDbInput(false)}>
                        Use existing database
                    </button>
                </div>
            )}
             {/* upload button */}
            <button 
                onClick={handleUpload} 
                disabled={loading || !file || !database}
            >
                {loading ? 'Uploading...' : 'Upload'}
            </button>
        </div>
    )
}

export default DataUploader;