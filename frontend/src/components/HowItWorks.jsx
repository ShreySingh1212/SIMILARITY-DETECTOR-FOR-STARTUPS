export default function HowItWorks() {
  const steps = [
    {
      number: '1',
      title: 'Describe Your Idea',
      description: 'Enter a detailed description of your startup concept, including the problem it solves and your target market.'
    },
    {
      number: '2',
      title: 'AI Analysis',
      description: 'Our AI engine generates semantic embeddings and searches across 100+ startups to find the closest matches.'
    },
    {
      number: '3',
      title: 'Get Insights',
      description: 'Receive similarity scores, uniqueness rating, competitive landscape, and actionable AI-powered gap analysis.'
    }
  ];

  return (
    <section className="how-it-works" id="how-it-works">
      <div className="container">
        <div style={{textAlign: 'center'}}>
          <h2 className="section-title animate-fade-in-up">
            How It <span className="gradient-text">Works</span>
          </h2>
          <p className="section-subtitle animate-fade-in-up delay-1">
            Three simple steps to validate your startup idea
          </p>
        </div>
        <div className="steps">
          {steps.map((s, i) => (
            <div key={i} className={`step animate-fade-in-up delay-${i + 1}`}>
              <div className="step-number">{s.number}</div>
              <h3>{s.title}</h3>
              <p>{s.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
