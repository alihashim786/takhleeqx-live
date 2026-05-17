/**
 * AgentCard — Displays a single agent's status in the live monitor.
 */
import { Bot, CheckCircle, XCircle, Loader, Clock } from 'lucide-react';

const statusConfig = {
  idle: { icon: Clock, color: 'text-text-muted', bg: 'bg-text-muted/10', label: 'Waiting' },
  running: { icon: Loader, color: 'text-accent', bg: 'bg-accent/10', label: 'Running' },
  done: { icon: CheckCircle, color: 'text-success', bg: 'bg-success/10', label: 'Completed' },
  error: { icon: XCircle, color: 'text-danger', bg: 'bg-danger/10', label: 'Error' },
};

export default function AgentCard({ name, description, status = 'idle', message, order }) {
  const config = statusConfig[status] || statusConfig.idle;
  const Icon = config.icon;

  return (
    <div
      className={`card animate-fade-in relative overflow-hidden ${
        status === 'running' ? 'animate-pulse-glow border-accent' : ''
      }`}
      style={{ animationDelay: `${order * 100}ms` }}
    >
      {/* Progress indicator for running */}
      {status === 'running' && (
        <div className="absolute top-0 left-0 w-full h-1 gradient-accent opacity-60">
          <div className="h-full bg-white/30 animate-shimmer" style={{ width: '30%' }} />
        </div>
      )}

      <div className="flex items-start gap-4">
        {/* Agent Icon */}
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${config.bg} shrink-0`}>
          <Bot className={`w-6 h-6 ${config.color}`} />
        </div>

        {/* Agent Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h3 className="font-semibold text-text-primary">{name}</h3>
            <div className={`flex items-center gap-1.5 text-xs font-medium ${config.color}`}>
              <Icon className={`w-3.5 h-3.5 ${status === 'running' ? 'animate-spin' : ''}`} />
              {config.label}
            </div>
          </div>
          <p className="text-sm text-text-muted mb-2">{description}</p>
          {message && (
            <div className="text-xs text-text-secondary bg-surface/50 rounded-lg px-3 py-2 mt-2">
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
