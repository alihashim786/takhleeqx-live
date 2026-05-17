/**
 * TakhleeqX Layout — App shell with sidebar navigation.
 */
import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Bot,
  BarChart3,
  Rss,
  PieChart,
  LogOut,
  Sparkles,
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Onboarding', end: true },
  { to: '/agents', icon: Bot, label: 'Agent Monitor' },
  { to: '/campaign', icon: BarChart3, label: 'Campaign' },
  { to: '/feed', icon: Rss, label: 'Social Feed' },
  { to: '/analytics', icon: PieChart, label: 'Analytics' },
];

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-64 glass flex flex-col justify-between p-0 fixed h-full z-50">
        {/* Logo */}
        <div>
          <div className="flex items-center gap-3 px-6 py-6 border-b border-border">
            <div className="w-10 h-10 gradient-primary rounded-xl flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-text-primary">TakhleeqX</h1>
              <p className="text-xs text-text-muted">AI Marketing</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="mt-4 px-3 space-y-1">
            {navItems.map(({ to, icon: Icon, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'gradient-primary text-white shadow-lg'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                {label}
              </NavLink>
            ))}
          </nav>
        </div>

        {/* User Info */}
        <div className="px-4 py-4 border-t border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full gradient-accent flex items-center justify-center text-sm font-bold text-white">
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </div>
              <span className="text-sm text-text-secondary">{user?.username}</span>
            </div>
            <button onClick={logout} className="text-text-muted hover:text-danger transition-colors" title="Logout">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64 p-8">
        <Outlet />
      </main>
    </div>
  );
}
