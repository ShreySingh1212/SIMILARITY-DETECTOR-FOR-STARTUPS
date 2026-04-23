export default function Features() {
  const features = [
    {
      icon: '🧠',
      color: 'purple',
      title: 'Semantic Analysis',
      description: 'Advanced AI embeddings understand the meaning of your idea, not just keywords. Captures nuance and context.'
    },
    {
      icon: '📊',
      color: 'cyan',
      title: 'Similarity Scoring',
      description: 'Get precise similarity percentages against 100+ real startups across 20+ categories with detailed breakdowns.'
    },
    {
      icon: '🎯',
      color: 'pink',
      title: 'Gap Analysis',
      description: 'AI-powered competitive analysis identifies your strengths, weaknesses, and key differentiators.'
    },
    {
      icon: '💡',
      color: 'green',
      title: 'Uniqueness Score',
      description: 'Instant uniqueness rating (0-100%) tells you exactly how crowded or open your market space is.'
    }
  ];

  return (
    <section className="features" id="features">
      <div className="container">
        <div style={{textAlign: 'center'}}>
          <h2 className="section-title animate-fade-in-up">
            Powerful <span className="gradient-text">Features</span>
          </h2>
          <p className="section-subtitle animate-fade-in-up delay-1">
            Everything you need to validate your startup idea against the competitive landscape
          </p>
        </div>
        <div className="features-grid">
          {features.map((f, i) => (
            <div key={i} className={`glass-card feature-card animate-fade-in-up delay-${i + 1}`}>
              <div className={`feature-icon ${f.color}`}>{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
