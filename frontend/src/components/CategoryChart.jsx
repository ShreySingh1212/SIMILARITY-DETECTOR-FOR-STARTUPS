export default function CategoryChart({ distribution }) {
  if (!distribution || Object.keys(distribution).length === 0) return null;

  const sorted = Object.entries(distribution).sort((a, b) => b[1] - a[1]);
  const max = sorted[0][1];
  const colors = ['var(--accent-purple)', 'var(--accent-cyan)', 'var(--accent-pink)', 'var(--accent-green)', 'var(--accent-orange)'];

  return (
    <div className="glass-card category-card animate-scale-in" style={{animationDelay: '0.2s'}}>
      <h3>📊 Category Distribution</h3>
      {sorted.map(([name, count], i) => (
        <div key={name} className="category-bar">
          <span className="category-name">{name}</span>
          <div className="category-bar-fill">
            <div
              className="category-bar-inner"
              style={{
                width: `${(count / max) * 100}%`,
                background: colors[i % colors.length],
                animationDelay: `${i * 0.15}s`
              }}
            />
          </div>
          <span className="category-count">{count}</span>
        </div>
      ))}
    </div>
  );
}
