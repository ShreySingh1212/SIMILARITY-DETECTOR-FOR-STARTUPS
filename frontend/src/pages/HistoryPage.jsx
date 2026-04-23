import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const API_URL = 'http://localhost:8000/api';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const { isAuthenticated, getAuthHeaders } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    fetchHistory();
  }, [isAuthenticated]);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_URL}/history`, {
        headers: {
          ...getAuthHeaders()
        }
      });

      if (!res.ok) throw new Error('Failed to load history');

      const data = await res.json();
      setHistory(data.history);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    setDeletingId(id);
    try {
      const res = await fetch(`${API_URL}/history/${id}`, {
        method: 'DELETE',
        headers: { ...getAuthHeaders() }
      });

      if (res.ok) {
        setHistory(prev => prev.filter(h => h.id !== id));
      }
    } catch (err) {
      console.error('Delete failed:', err);
    } finally {
      setDeletingId(null);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'var(--accent-green)';
    if (score >= 40) return 'var(--accent-orange)';
    return 'var(--accent-red)';
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  };

  return (
    <>
      <Navbar />
      <div className="history-page">
        <div className="container">
          <div className="history-header animate-fade-in-up">
            <h1>
              📊 Your <span className="gradient-text">Search History</span>
            </h1>
            <p style={{ color: 'var(--text-secondary)', marginTop: 12, fontSize: '1.1rem' }}>
              Review your past startup idea analyses
            </p>
          </div>

          {loading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
              <p className="loading-text">Loading your history...</p>
            </div>
          )}

          {error && (
            <div className="glass-card animate-scale-in" style={{
              padding: 24, textAlign: 'center', maxWidth: 600, margin: '0 auto',
              borderColor: 'rgba(239,68,68,0.3)'
            }}>
              <p style={{ color: 'var(--accent-red)' }}>❌ {error}</p>
            </div>
          )}

          {!loading && !error && history.length === 0 && (
            <div className="history-empty glass-card animate-scale-in">
              <div className="empty-icon">🔍</div>
              <h3>No analyses yet</h3>
              <p>Start analyzing startup ideas to build your history</p>
              <Link to="/analyze" className="btn-primary" style={{ marginTop: 20 }}>
                Analyze Your First Idea →
              </Link>
            </div>
          )}

          {!loading && history.length > 0 && (
            <div className="history-list">
              {history.map((item, index) => (
                <div
                  key={item.id}
                  className="history-item glass-card animate-fade-in-up"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <div className="history-item-header">
                    <div className="history-item-score" style={{
                      color: getScoreColor(item.uniqueness_score)
                    }}>
                      <span className="history-score-value">{Math.round(item.uniqueness_score || 0)}%</span>
                      <span className="history-score-label">{item.uniqueness_label || 'N/A'}</span>
                    </div>
                    <div className="history-item-date">
                      {formatDate(item.created_at)}
                    </div>
                  </div>

                  <div className="history-item-idea">
                    {item.input_text.length > 200
                      ? item.input_text.substring(0, 200) + '...'
                      : item.input_text
                    }
                  </div>

                  {item.top_matches && item.top_matches.length > 0 && (
                    <div className="history-matches">
                      <span className="history-matches-label">Top matches:</span>
                      {item.top_matches.slice(0, 3).map((m, i) => (
                        <span key={i} className="history-match-tag">
                          {m.name} ({m.similarity}%)
                        </span>
                      ))}
                    </div>
                  )}

                  {item.gap_analysis && (
                    <div className="history-gap-summary">
                      <span>💡</span>
                      {item.gap_analysis.length > 150
                        ? item.gap_analysis.substring(0, 150) + '...'
                        : item.gap_analysis
                      }
                    </div>
                  )}

                  <div className="history-item-actions">
                    <button
                      className="btn-delete"
                      onClick={() => handleDelete(item.id)}
                      disabled={deletingId === item.id}
                    >
                      {deletingId === item.id ? '⏳' : '🗑️'} Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <Footer />
    </>
  );
}
