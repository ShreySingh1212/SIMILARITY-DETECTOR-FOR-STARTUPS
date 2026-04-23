import { Link } from 'react-router-dom';

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-bg">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>
      <div className="container hero-content">
        <div className="animate-fade-in-up">
          <span className="hero-badge">⚡ AI-Powered Analysis</span>
        </div>
        <h1 className="hero-title animate-fade-in-up delay-1">
          Is Your Startup Idea<br />
          <span className="gradient-text">Truly Unique?</span>
        </h1>
        <p className="hero-description animate-fade-in-up delay-2">
          Discover how your startup idea compares to existing companies. Get instant
          similarity analysis, competitive insights, and AI-powered gap analysis
          to validate and differentiate your concept.
        </p>
        <div className="hero-actions animate-fade-in-up delay-3">
          <Link to="/analyze" className="btn-primary" style={{padding: '16px 40px', fontSize: '1.1rem'}}>
            🚀 Analyze Your Idea
          </Link>
          <a href="#how-it-works" className="btn-secondary">
            Learn More ↓
          </a>
        </div>
        <div className="hero-stats animate-fade-in-up delay-4">
          <div className="hero-stat">
            <div className="hero-stat-value">100+</div>
            <div className="hero-stat-label">Startups Indexed</div>
          </div>
          <div className="hero-stat">
            <div className="hero-stat-value">20+</div>
            <div className="hero-stat-label">Industry Categories</div>
          </div>
          <div className="hero-stat">
            <div className="hero-stat-value">AI</div>
            <div className="hero-stat-label">Gap Analysis</div>
          </div>
        </div>
      </div>
    </section>
  );
}
