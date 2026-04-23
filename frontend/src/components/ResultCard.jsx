export default function ResultCard({ startup, index }) {
  const getBarColor = (pct) => {
    if (pct >= 70) return 'var(--accent-red)';
    if (pct >= 50) return 'var(--accent-orange)';
    if (pct >= 30) return 'var(--accent-cyan)';
    return 'var(--accent-green)';
  };

  return (
    <div
      className="glass-card startup-card animate-fade-in-up"
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className="startup-card-header">
        <span className="startup-name">{startup.name}</span>
        <span className="startup-category">{startup.category}</span>
      </div>

      <p className="startup-description">{startup.description}</p>

      <div className="similarity-meter">
        <div className="similarity-header">
          <span className="similarity-label">Similarity</span>
          <span className="similarity-value" style={{color: getBarColor(startup.similarity_percentage)}}>
            {startup.similarity_percentage}%
          </span>
        </div>
        <div className="similarity-bar">
          <div
            className="similarity-bar-fill"
            style={{
              width: `${startup.similarity_percentage}%`,
              background: getBarColor(startup.similarity_percentage)
            }}
          />
        </div>
      </div>

      {startup.tags && startup.tags.length > 0 && (
        <div className="startup-tags">
          {startup.tags.map((tag, i) => (
            <span key={i} className="startup-tag">{tag}</span>
          ))}
        </div>
      )}

      <div className="startup-meta">
        {startup.founded_year > 0 && <span>📅 {startup.founded_year}</span>}
        {startup.funding_stage && <span>💰 {startup.funding_stage}</span>}
        {startup.status && (
          <span>{startup.status === 'active' ? '🟢' : startup.status === 'dead' ? '🔴' : '🟡'} {startup.status}</span>
        )}
      </div>
    </div>
  );
}
