import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import IdeaInput from '../components/IdeaInput';
import UniquenessScore from '../components/UniquenessScore';
import CategoryChart from '../components/CategoryChart';
import ResultCard from '../components/ResultCard';
import GapAnalysis from '../components/GapAnalysis';
import LoadingAnimation from '../components/LoadingAnimation';
import Footer from '../components/Footer';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function AnalyzePage() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const { getAuthHeaders, isAuthenticated } = useAuth();

  const handleAnalyze = async (idea) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify({
          idea,
          top_k: 10,
          include_gap_analysis: true
        })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${res.status}`);
      }

      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to connect to the server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="analyze-page">
        <div className="container">
          <div className="analyze-header animate-fade-in-up">
            <h1>
              Analyze Your <span className="gradient-text">Startup Idea</span>
            </h1>
            <p style={{color: 'var(--text-secondary)', marginTop: 12, fontSize: '1.1rem'}}>
              Describe your idea below and discover how it compares to existing startups
            </p>
            {!isAuthenticated && (
              <p className="auth-hint animate-fade-in" style={{
                color: 'var(--accent-cyan)',
                fontSize: '0.9rem',
                marginTop: 8,
                opacity: 0.8
              }}>
                💡 <a href="/login" style={{color: 'var(--accent-cyan)'}}>Sign in</a> to save your analyses and view history
              </p>
            )}
          </div>

          <IdeaInput onAnalyze={handleAnalyze} loading={loading} />

          {loading && <LoadingAnimation />}

          {error && (
            <div className="glass-card animate-scale-in" style={{
              padding: 24, textAlign: 'center', maxWidth: 600, margin: '0 auto',
              borderColor: 'rgba(239,68,68,0.3)'
            }}>
              <p style={{color: 'var(--accent-red)', fontSize: '1rem'}}>❌ {error}</p>
              <p style={{color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 8}}>
                Make sure the backend server is running on port 8000
              </p>
            </div>
          )}

          {results && (
            <div className="results-section">
              <div className="results-header">
                <UniquenessScore
                  score={results.uniqueness_score}
                  label={results.uniqueness_label}
                />
                <CategoryChart distribution={results.category_distribution} />
              </div>

              <div className="similar-section">
                <h2 style={{display: 'flex', alignItems: 'center', gap: 10}}>
                  🏢 Similar Startups
                  <span style={{
                    fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 400
                  }}>
                    (compared against {results.total_comparisons} startups)
                  </span>
                </h2>
                <div className="startup-grid">
                  {results.similar_startups.map((startup, i) => (
                    <ResultCard key={i} startup={startup} index={i} />
                  ))}
                </div>
              </div>

              {results.gap_analysis && (
                <GapAnalysis data={results.gap_analysis} />
              )}
            </div>
          )}
        </div>
      </div>
      <Footer />
    </>
  );
}
