/**
 * TakhleeqX Layout — App shell with sidebar navigation.
 */
import { useState } from 'react';
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
  PanelLeftClose,
  PanelLeftOpen,
  Users
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Onboarding', end: true },
  { to: '/agents', icon: Bot, label: 'Agent Monitor' },
  { to: '/campaign', icon: BarChart3, label: 'Campaign' },
  { to: '/feed', icon: Rss, label: 'Social Feed' },
  { to: '/analytics', icon: PieChart, label: 'Analytics' },
  { to: '/about', icon: Users, label: 'About Us' },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} glass flex flex-col justify-between p-0 fixed h-full z-50 transition-all duration-300`}>
        {/* Logo */}
        <div>
          <div className={`flex items-center ${isSidebarOpen ? 'justify-between px-6' : 'justify-center'} py-6 border-b border-border`}>
            {isSidebarOpen && (
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 gradient-primary rounded-xl flex items-center justify-center shrink-0">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="text-lg font-bold text-text-primary leading-tight">TakhleeqX</h1>
                  <p className="text-[10px] text-text-muted leading-tight">AI Marketing</p>
                </div>
              </div>
            )}
            <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="text-text-muted hover:text-text-primary p-1 rounded-lg hover:bg-surface-hover transition-colors shrink-0" title="Toggle Sidebar">
              {isSidebarOpen ? <PanelLeftClose className="w-5 h-5" /> : <PanelLeftOpen className="w-6 h-6" />}
            </button>
          </div>

          {/* Navigation */}
          <nav className="mt-4 px-3 space-y-1">
            {navItems.map(({ to, icon: Icon, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `flex items-center ${isSidebarOpen ? 'gap-3 px-4' : 'justify-center'} py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'gradient-primary text-white shadow-lg'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
                  }`
                }
                title={!isSidebarOpen ? label : ''}
              >
                <Icon className="w-5 h-5 shrink-0" />
                {isSidebarOpen && <span className="whitespace-nowrap">{label}</span>}
              </NavLink>
            ))}
          </nav>
        </div>

        {/* User Info */}
        <div className={`px-4 py-4 border-t border-border flex ${isSidebarOpen ? 'justify-between items-center' : 'flex-col items-center gap-4'}`}>
          {isSidebarOpen ? (
            <>
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="w-8 h-8 shrink-0 rounded-full gradient-accent flex items-center justify-center text-sm font-bold text-white">
                  {user?.username?.[0]?.toUpperCase() || 'U'}
                </div>
                <span className="text-sm text-text-secondary truncate">{user?.username}</span>
              </div>
              <button onClick={logout} className="text-text-muted hover:text-danger transition-colors shrink-0" title="Logout">
                <LogOut className="w-4 h-4" />
              </button>
            </>
          ) : (
            <>
              <div className="w-8 h-8 shrink-0 rounded-full gradient-accent flex items-center justify-center text-sm font-bold text-white" title={user?.username}>
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </div>
              <button onClick={logout} className="text-text-muted hover:text-danger transition-colors shrink-0" title="Logout">
                <LogOut className="w-5 h-5" />
              </button>
            </>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 ${isSidebarOpen ? 'ml-64' : 'ml-20'} p-8 transition-all duration-300`}>
        <Outlet />
      </main>
    </div>
  );
}
