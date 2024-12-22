import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Header from '../Header';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    // ref to the end of the messages container
    const messagesEndRef = useRef(null);

    // function to scroll to bottom of chat
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
    
    // scroll to the bottom of the chat when new message is added
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // handle user input asynchronously
    const handleSubmit = async (e) => {
        // cancel default form behavior
        e.preventDefault();

        // add user message to the array
        const userMessage = { role: 'user', content: input };
        // update the messages array state
        setMessages(prev => [...prev, userMessage]);
        // clear the chat input
        setInput('');
        setLoading(true);

        // send user message to the backend
        try {
            // create response object to send input to backend
            const response = await axios.post('/api/analysis/analyze', {
                message: input,
                telemetry: window.telemetryData // assume data is stored globally
            });

            // add ai response
            const aiMessage = { role: 'assistant', content: response.data.analysis };
            // copy response and add to the ai messages array
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error: ', error);
            setMessages(prev => [...prev, {
                role: 'error',
                content: 'An error occurred while processing your request. Please try again.'
            }]);
        }

        setLoading(false);

    };

    return(
        <div className="container">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <Header title="Chat" isCollapsible={false}/>
                {/* map message roles to ui */}
                {messages.map((message, index) => (
                    <div key={index}>
                        <div className={`message--${message.role}`}>
                            {message.content}
                        </div>

                    </div>
                ))}

                {/* loading */}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg p-3">
                            <div className="animate-pulse"> Analyzing... </div>
                        </div>
                    </div>
                )}

                {/* scroll to bottom */}
                <div ref={messagesEndRef} />
            </div>

            {/* handle input */}
            <form onSubmit={handleSubmit} className="border-t p-4">
                <div className="row">
                    <input 
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question..."
                    className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {/* send button */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Send
                    </button>

                </div>
            </form>

        </div>

    )
}

export default Chat;