import { useState, useEffect, useRef } from 'react';
import Subheader from '../Subheader';
import { analyzeData } from '../../api/api';
import ReactMarkdown from 'react-markdown';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // function to scroll to bottom of chat
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
    
    // scroll to the bottom of the chat when new message is added
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // format ai response
    const formatAIResponse = (content) => {
        if (!content) return '';

        // Format code blocks
        let formattedContent = content.replace(
            /```(\w+)?\n([\s\S]*?)```/g,
            (_, language, code) => `\`\`\`${language || ''}\n${code.trim()}\`\`\``
        );

        // Format bullet points and numbered lists
        formattedContent = formattedContent
            // Add breaks after bullet points
            .replace(/([•\-\*]\s.*?)(?=(?:[•\-\*]|\d+\.|\n|$))/g, '$1\n')
            // Add breaks after numbered lists
            .replace(/(\d+\.\s.*?)(?=(?:[•\-\*]|\d+\.|\n|$))/g, '$1\n')
            // Remove extra line breaks
            .replace(/\n{3,}/g, '\n\n')
            .trim();

        return formattedContent;
    };

    const handleSubmit = async (e) => {
        // cancel default form behavior
        e.preventDefault();
        if (!input.trim()) return;

        // add user message to the array
        const userMessage = { role: 'user', content: input };
        // update the messages array state
        setMessages(prev => [...prev, userMessage]);
        // clear the chat input
        setInput('');
        setLoading(true);

        // send user message to the backend
        try {
            // analyze user message in the backend
            const data = await analyzeData(input);
            const formattedContent = formatAIResponse(data.analysis);
            const aiMessage = { 
                role: 'assistant', 
                content: formattedContent,
                sources: data.sources || []
            };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'error',
                content: 'An error occurred while processing your request. Please try again.'
            }]);
        }

        setLoading(false);
    };

    return (
        <div className="container chat">
            <div className="flex-1 overflow-y-auto">
                <Subheader title="Chat" isCollapsible={false}/>
                {/* map message roles to ui */}
                <div className="message-container">
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.role}`}>
                            {/* for assistant */}
                            {message.role === 'assistant' && (
                                <>
                                    {/* // sources */}
                                        
                                        {message.sources && message.sources.length > 0 && (
                                            <div className="container sources">
                                                {/* header */}
                                                <div 
                                                    className="row card-heading"
                                                    style={{
                                                        marginBottom: '8px'
                                                    }}
                                                >
                                                    <i className="fa-solid fa-book" style={{color: 'white'}}></i>
                                                    <div className="subtext">Sources</div>
                                                </div>
                                                {/* sources */}
                                                <div className="sources-list">
                                                    {message.sources.map((source, index) => (
                                                        <div key={index} className="source-item">
                                                            <div className="subheading">{source.content}</div>
                                                            <div className="subtext">{source.title}</div>
                                                        </div>
                                                    ))}
                                                </div>

                                            </div>
                                        )}
                                    {/* // analysis */}
                                    <div 
                                        className="row card-heading"
                                        style={{
                                            marginBottom: '8px'
                                        }}
                                    >
                                        <i className="fa-solid fa-robot" style={{color: 'white'}}></i>
                                        <div className="subtext">Analysis</div>
                                    </div>
                                </>
                            )}
                            {/* rest of content */}
                            <div className="message-content">
                                <ReactMarkdown>
                                    {message.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="message loading">
                            <div className="message-content">
                                <div className="animate-pulse">Analyzing...</div>
                            </div>
                        </div>
                    )}
                </div>
                <div ref={messagesEndRef} />
            </div>

            {/* handle input */}
            <form onSubmit={handleSubmit} className="form-input-wrapper">
                <div className="row">
                    <input 
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                        className="flex-1"
                    />
                    {/* send button */}
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <i className="fa-solid fa-paper-plane"></i>
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Chat;