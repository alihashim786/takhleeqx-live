/**
 * StatCard — Analytics stat display card.
 */
export default function StatCard({ title, value, change, icon: Icon, color = 'primary' }) {
  const colorMap = {
    primary: 'from-primary to-primary-light',
    accent: 'from-accent to-amber-400',
    success: 'from-success to-emerald-400',
    danger: 'from-danger to-rose-400',
  };

  return (
    <div className="card animate-fade-in group">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-text-muted mb-1">{title}</p>
          <p className="text-3xl font-bold text-text-primary">{value}</p>
          {change && (
            <p className={`text-xs mt-2 font-medium ${change > 0 ? 'text-success' : 'text-danger'}`}>
              {change > 0 ? '↑' : '↓'} {Math.abs(change)}% from last week
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorMap[color]} flex items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity`}>
          {Icon && <Icon className="w-6 h-6 text-white" />}
        </div>
      </div>
    </div>
  );
}
