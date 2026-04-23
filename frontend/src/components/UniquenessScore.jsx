export default function UniquenessScore({ score, label }) {
  const radius = 75;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 70) return 'var(--accent-green)';
    if (score >= 40) return 'var(--accent-orange)';
    return 'var(--accent-red)';
  };

  return (
    <div className="glass-card uniqueness-card animate-scale-in">
      <h3 style={{fontSize: '1.1rem', fontWeight: 700, marginBottom: 20}}>Uniqueness Score</h3>
      <div className="uniqueness-gauge">
        <svg viewBox="0 0 170 170">
          <circle className="bg-circle" cx="85" cy="85" r={radius} />
          <circle
            className="progress-circle"
            cx="85" cy="85" r={radius}
            stroke={getColor()}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="uniqueness-value">
          <span className="uniqueness-number" style={{color: getColor()}}>
            {score}%
          </span>
          <span className="uniqueness-label">{label}</span>
        </div>
      </div>
      <p style={{fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 8}}>
        {score >= 70 ? 'Your idea has strong uniqueness potential!' :
         score >= 40 ? 'Similar concepts exist — differentiation is key.' :
         'Highly competitive space — focus on unique value.'}
      </p>
    </div>
  );
}
