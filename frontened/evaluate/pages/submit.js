import { useState } from 'react';
import axios from 'axios';

export default function IdeaSubmit() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post('http://localhost:5000/evaluate', { text });
      if (res.data.success) {
        setResponse(res.data.data); 
        console.log(res) // Store Gemini's response
      } else {
        setError(res.data.error || "Unknown error");
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Evaluate Your Idea</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe your idea..."
          rows={5}
          style={{ width: '100%', marginBottom: '1rem' }}
          disabled={loading}
        />
        <button 
          type="submit" 
          disabled={loading}
          style={{ padding: '0.5rem 1rem', background: loading ? '#ccc' : '#0070f3', color: 'white' }}
        >
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>

      {/* Display Results */}
      {error && (
        <div style={{ color: 'red', marginTop: '1rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && (
        <div style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ddd' }}>
          <h2>Evaluation Results</h2>
          <p><strong>Originality:</strong> {response.originality}/10</p>
          <p><strong>Creativity:</strong> {response.creativity}/10</p>
          <p><strong>Critical Thinking:</strong> {response.critical_thinking}/10</p>
          <p><strong>Feedback:</strong> {response.feedback}</p>
        </div>
      )}
    </div>
  );
}