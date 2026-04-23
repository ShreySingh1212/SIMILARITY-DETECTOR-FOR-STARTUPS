export default function GapAnalysis({ data }) {
  if (!data) return null;

  const sections = [
    { title: '💪 Strengths', items: data.strengths, color: 'var(--accent-green)' },
    { title: '⚠️ Weaknesses', items: data.weaknesses, color: 'var(--accent-orange)' },
    { title: '🎯 Differentiators', items: data.differentiators, color: 'var(--accent-cyan)' },
    { title: '💡 Suggestions', items: data.suggestions, color: 'var(--accent-purple)' },
  ];

  return (
    <div className="gap-section animate-fade-in-up">
      <h2>🤖 AI Gap Analysis</h2>

      <div className="glass-card gap-summary">
        <p>{data.summary}</p>
        <div style={{marginTop: 12}}>
          <span className={`saturation-badge saturation-${data.market_saturation}`}>
            Market Saturation: {data.market_saturation.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="gap-grid">
        {sections.map((section, i) => (
          <div key={i} className="glass-card gap-card animate-fade-in-up" style={{animationDelay: `${i * 0.1}s`}}>
            <h4 style={{color: section.color}}>{section.title}</h4>
            <ul>
              {section.items.map((item, j) => (
                <li key={j}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
