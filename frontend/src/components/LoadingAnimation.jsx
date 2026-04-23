export default function LoadingAnimation() {
  return (
    <div className="loading-overlay">
      <div className="loading-spinner"></div>
      <p className="loading-text">Analyzing your startup idea...</p>
      <p className="loading-subtext">Generating embeddings & searching 100+ startups</p>
    </div>
  );
}
