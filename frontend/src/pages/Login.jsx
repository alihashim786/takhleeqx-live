/**
 * Login Page — JWT authentication form.
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, LogIn, Eye, EyeOff } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [openaiKey, setOpenaiKey] = useState(localStorage.getItem('takhleeqx_openai_key') || '');
  const [showPassword, setShowPassword] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    localStorage.setItem('takhleeqx_openai_key', openaiKey);
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center gradient-hero p-4">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-[100px] animate-float-orb" />
        <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-accent/20 rounded-full blur-[100px] animate-float-orb" style={{ animationDelay: '3s' }} />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-text-primary">TakhleeqX</h1>
          <p className="text-text-muted mt-2">AI-Powered Marketing Automation</p>
        </div>

        {/* Form Card */}
        <div className="glass rounded-2xl p-8 animate-fade-in" style={{ animationDelay: '150ms' }}>
          <h2 className="text-xl font-semibold text-text-primary mb-6">Welcome back</h2>

          {error && (
            <div className="bg-danger/10 border border-danger/30 rounded-xl px-4 py-3 text-sm text-danger mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-text-secondary mb-2">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field"
                placeholder="Enter your username"
                required
              />
            </div>

            <div>
              <label className="block text-sm text-text-secondary mb-2">OpenAI API Key <span className="text-xs text-text-muted">(Optional - For live testing)</span></label>
              <input
                type="password"
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
                className="input-field"
                placeholder="sk-..."
              />
              <p className="text-xs text-text-muted mt-1">If left blank, mock data will be used. Your key is never stored on our servers.</p>
            </div>

            <div>
              <label className="block text-sm text-text-secondary mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field pr-10"
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full mt-6">
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <LogIn className="w-4 h-4" />
                  Sign In
                </>
              )}
            </button>
          </form>

          <p className="text-center text-sm text-text-muted mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-light hover:text-primary font-medium">
              Create one
            </Link>
          </p>

          <div className="mt-6 pt-6 border-t border-border/50 text-center">
            <button 
              type="button" 
              onClick={() => setShowHelp(!showHelp)}
              className="text-xs text-text-muted hover:text-primary transition-colors font-medium"
            >
              Need Help?
            </button>
            {showHelp && (
              <div className="mt-4 p-4 rounded-xl bg-surface-light border border-border text-left text-sm text-text-secondary animate-fade-in">
                <p className="font-semibold text-text-primary mb-2">Support & Onboarding</p>
                <p className="mb-1">Phone: <span className="text-primary-light">+923215017784</span></p>
                <p>Email: <a href="https://mail.google.com/mail/?view=cm&fs=1&to=muhammadalihashim514@gmail.com" target="_blank" rel="noopener noreferrer" className="text-primary-light hover:underline">muhammadalihashim514@gmail.com</a></p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
