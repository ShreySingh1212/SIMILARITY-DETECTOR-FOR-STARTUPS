import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
    setMenuOpen(false);
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="container navbar-inner">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">🔍</span>
          IdeaLens
        </Link>
        <ul className="navbar-links">
          {location.pathname === '/' ? (
            <>
              <li><a href="#features">Features</a></li>
              <li><a href="#how-it-works">How It Works</a></li>
            </>
          ) : (
            <li><Link to="/">Home</Link></li>
          )}

          {isAuthenticated ? (
            <>
              <li>
                <Link to="/history" className="nav-history-link">
                  📊 History
                </Link>
              </li>
              <li className="nav-user-menu">
                <button
                  className="nav-user-btn"
                  onClick={() => setMenuOpen(!menuOpen)}
                >
                  <span className="nav-avatar">
                    {user?.name?.charAt(0)?.toUpperCase() || '?'}
                  </span>
                  <span className="nav-username">{user?.name?.split(' ')[0]}</span>
                </button>
                {menuOpen && (
                  <div className="nav-dropdown glass-card">
                    <div className="nav-dropdown-header">
                      <span className="nav-dropdown-name">{user?.name}</span>
                      <span className="nav-dropdown-email">{user?.email}</span>
                    </div>
                    <div className="nav-dropdown-divider"></div>
                    <Link to="/history" className="nav-dropdown-item" onClick={() => setMenuOpen(false)}>
                      📊 Search History
                    </Link>
                    <button className="nav-dropdown-item nav-logout-btn" onClick={handleLogout}>
                      🚪 Sign Out
                    </button>
                  </div>
                )}
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login" className="nav-login-link">Sign In</Link>
              </li>
            </>
          )}
          <li>
            <Link to="/analyze" className="btn-primary" style={{ padding: '10px 24px', fontSize: '0.9rem' }}>
              Analyze Idea
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
