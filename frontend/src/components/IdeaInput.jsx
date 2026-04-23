import { useState } from 'react';

export default function IdeaInput({ onAnalyze, loading }) {
  const [idea, setIdea] = useState('');

  const handleSubmit = () => {
    if (idea.trim().length >= 20) {
      onAnalyze(idea.trim());
    }
  };

  return (
    <div className="input-section">
      <div className="idea-input-wrapper">
        <textarea
          className="idea-textarea"
          placeholder="Describe your startup idea in detail... For example: 'An AI-powered platform that helps small restaurants optimize their menu pricing based on local competitor analysis, ingredient costs, and customer demand patterns.'"
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          maxLength={5000}
          id="idea-input"
        />
      </div>
      <div className="input-footer">
        <span className="char-count">
          {idea.length} / 5,000 characters
          {idea.length > 0 && idea.length < 20 && (
            <span style={{color: 'var(--accent-orange)', marginLeft: 8}}>
              (minimum 20 characters)
            </span>
          )}
        </span>
        <button
          className="btn-primary"
          onClick={handleSubmit}
          disabled={loading || idea.trim().length < 20}
          id="analyze-btn"
        >
          {loading ? (
            <>
              <span className="loading-spinner" style={{width: 20, height: 20, margin: 0, borderWidth: 2}}></span>
              Analyzing...
            </>
          ) : (
            <>🚀 Analyze Idea</>
          )}
        </button>
      </div>
    </div>
  );
}
