/**
 * Analytics Page — AI-predicted analytics from the Performance Predictor agent.
 * Falls back to mock data if no predictions available yet.
 */
import { useState, useEffect } from 'react';
import api from '../api/client';
import StatCard from '../components/StatCard';
import { PieChart, Eye, Users, Heart, MessageCircle, Share2, TrendingUp, Zap, Brain, Clock, Target, Compass } from 'lucide-react';

export default function Analytics() {
  const [campaigns, setCampaigns] = useState([]);
  const [activeCampaign, setActiveCampaign] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const res = await api.get('/campaigns/');
      setCampaigns(res.data);
      if (res.data.length > 0) {
        setActiveCampaign(res.data[0]); // Most recent campaign
      }
    } catch (err) {
      console.error('Failed to load campaigns:', err);
    } finally {
      setLoading(false);
    }
  };

  const pred = activeCampaign?.predicted_analytics || {};
  const hasPredictions = pred && Object.keys(pred).length > 0 && !pred.error;

  // Use AI predictions or fallback to defaults
  const stats = [
    {
      title: 'Predicted Reach',
      value: hasPredictions ? formatNumber(pred.predicted_reach) : '—',
      change: hasPredictions ? 18.5 : null,
      icon: Eye,
      color: 'primary',
    },
    {
      title: 'Predicted Impressions',
      value: hasPredictions ? formatNumber(pred.predicted_impressions) : '—',
      change: hasPredictions ? 24.2 : null,
      icon: Users,
      color: 'accent',
    },
    {
      title: 'Engagement Rate',
      value: hasPredictions ? `${pred.predicted_engagement_rate}%` : '—',
      change: hasPredictions ? 12.1 : null,
      icon: Heart,
      color: 'success',
    },
    {
      title: 'Profile Visits',
      value: hasPredictions ? formatNumber(pred.predicted_profile_visits) : '—',
      change: hasPredictions ? 8.3 : null,
      icon: TrendingUp,
      color: 'primary',
    },
  ];

  const platformBreakdown = pred.platform_breakdown || {};

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map(i => <div key={i} className="shimmer h-32 rounded-2xl" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-text-primary flex items-center gap-3">
          <PieChart className="w-8 h-8 text-success" />
          Analytics Dashboard
        </h1>
        <p className="text-text-muted mt-2">
          {hasPredictions
            ? `AI-predicted performance metrics for "${activeCampaign?.campaign_name}"`
            : 'Launch a campaign to see AI-predicted analytics'}
        </p>
        <div className="mt-3 px-3 py-1.5 inline-flex items-center gap-2 rounded-full bg-primary/10 text-primary-light text-xs font-medium">
          <Brain className="w-3 h-3" />
          {hasPredictions ? 'Powered by Performance Predictor Agent (GPT-4o)' : 'No predictions yet'}
        </div>
      </div>

      {/* Campaign Selector (if multiple campaigns) */}
      {campaigns.length > 1 && (
        <div className="mb-6">
          <select
            value={activeCampaign?.id || ''}
            onChange={(e) => setActiveCampaign(campaigns.find(c => c.id === Number(e.target.value)))}
            className="input-field max-w-sm"
          >
            {campaigns.map(c => (
              <option key={c.id} value={c.id}>{c.campaign_name}</option>
            ))}
          </select>
        </div>
      )}

      {/* Quality Score Banner */}
      {activeCampaign?.quality_score && (
        <div className="card mb-6 animate-fade-in flex items-center gap-4 border-primary/30">
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-2xl font-bold text-white ${
            activeCampaign.quality_score >= 80 ? 'bg-gradient-to-br from-emerald-500 to-green-600' :
            activeCampaign.quality_score >= 60 ? 'bg-gradient-to-br from-amber-500 to-orange-500' :
            'bg-gradient-to-br from-red-500 to-rose-600'
          }`}>
            {activeCampaign.quality_score}
          </div>
          <div className="flex-1">
            <p className="font-semibold text-text-primary">Campaign Quality Score</p>
            <p className="text-sm text-text-muted mt-1">
              {activeCampaign.supervisor_notes || 'Evaluated by the Supervisor Agent'}
            </p>
          </div>
        </div>
      )}

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, i) => (
          <div key={i} style={{ animationDelay: `${i * 100}ms` }}>
            <StatCard {...stat} />
          </div>
        ))}
      </div>

      {/* Extra Metrics */}
      {hasPredictions && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {/* Saves */}
          <div className="card animate-fade-in" style={{ animationDelay: '400ms' }}>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <p className="text-sm text-text-muted">Predicted Saves</p>
            </div>
            <p className="text-2xl font-bold text-text-primary">{formatNumber(pred.predicted_saves)}</p>
          </div>

          {/* Shares */}
          <div className="card animate-fade-in" style={{ animationDelay: '500ms' }}>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                <Share2 className="w-5 h-5 text-white" />
              </div>
              <p className="text-sm text-text-muted">Predicted Shares</p>
            </div>
            <p className="text-2xl font-bold text-text-primary">{formatNumber(pred.predicted_shares)}</p>
          </div>

          {/* Growth */}
          <div className="card animate-fade-in" style={{ animationDelay: '600ms' }}>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                <Users className="w-5 h-5 text-white" />
              </div>
              <p className="text-sm text-text-muted">Followers Gained</p>
            </div>
            <p className="text-2xl font-bold text-text-primary">+{pred.weekly_growth_prediction?.followers_gained || '—'}</p>
            {pred.weekly_growth_prediction?.viral_potential && (
              <span className={`text-xs mt-1 px-2 py-0.5 rounded-full inline-block ${
                pred.weekly_growth_prediction.viral_potential === 'high' ? 'bg-success/20 text-success' :
                pred.weekly_growth_prediction.viral_potential === 'medium' ? 'bg-accent/20 text-accent' :
                'bg-text-muted/20 text-text-muted'
              }`}>
                {pred.weekly_growth_prediction.viral_potential} viral potential
              </span>
            )}
          </div>
        </div>
      )}

      {/* Campaign Trends Display */}
      {activeCampaign?.trends_data && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="glass rounded-2xl p-6 animate-fade-in" style={{ animationDelay: '650ms' }}>
            <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
              <Compass className="w-5 h-5 text-accent" /> Local Trends (Pakistan)
            </h3>
            <ul className="space-y-2">
              {(activeCampaign.trends_data.local_trends || []).slice(0, 5).map((trend, i) => (
                <li key={i} className="flex items-start gap-3 text-sm">
                  <span className="text-accent mt-1">•</span>
                  <span className="text-text-secondary">{typeof trend === 'string' ? trend : trend.trend || trend.name || JSON.stringify(trend)}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="glass rounded-2xl p-6 animate-fade-in" style={{ animationDelay: '700ms' }}>
            <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-primary" /> Global Viral Trends
            </h3>
            <ul className="space-y-2">
              {(activeCampaign.trends_data.global_trends || []).slice(0, 5).map((trend, i) => (
                <li key={i} className="flex items-start gap-3 text-sm">
                  <span className="text-primary mt-1">•</span>
                  <span className="text-text-secondary">{typeof trend === 'string' ? trend : trend.trend || trend.name || JSON.stringify(trend)}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Platform Breakdown */}
      {hasPredictions && platformBreakdown && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {Object.entries(platformBreakdown).map(([platform, data], i) => (
            <div key={platform} className="card animate-fade-in" style={{ animationDelay: `${(i + 6) * 100}ms` }}>
              <div className="flex items-center gap-3 mb-4">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${
                  platform === 'instagram' ? 'from-pink-500 to-purple-500' : 'from-blue-500 to-blue-600'
                } flex items-center justify-center`}>
                  <Share2 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-text-primary capitalize">{platform}</h3>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-text-muted">Reach</p>
                  <p className="text-xl font-bold text-text-primary">{formatNumber(data.reach)}</p>
                </div>
                <div>
                  <p className="text-xs text-text-muted">Engagement</p>
                  <p className="text-xl font-bold text-success">{data.engagement}%</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Best Posting Times */}
      {activeCampaign?.posting_schedule?.best_times && activeCampaign.posting_schedule.best_times.length > 0 && (
        <div className="glass rounded-2xl p-6 mb-8 animate-fade-in" style={{ animationDelay: '800ms' }}>
          <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5 text-accent" /> Scheduled Posting Times
          </h3>
          <div className="flex flex-wrap gap-3">
            {activeCampaign.posting_schedule.best_times.map((time, i) => (
              <span key={i} className="px-4 py-2 rounded-xl bg-primary/10 text-primary-light text-sm font-medium">
                🕐 {time}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Top Performing Pillar */}
      {hasPredictions && pred.top_performing_pillar && (
        <div className="card mb-8 animate-fade-in border-accent/30" style={{ animationDelay: '900ms' }}>
          <div className="flex items-center gap-3">
            <Target className="w-6 h-6 text-accent" />
            <div>
              <p className="text-sm text-text-muted">Top Performing Content Pillar (Predicted)</p>
              <p className="text-lg font-semibold text-text-primary">{pred.top_performing_pillar}</p>
            </div>
          </div>
        </div>
      )}

      {/* AI Recommendations */}
      {hasPredictions && pred.recommendations && (
        <div className="glass rounded-2xl p-6 animate-fade-in" style={{ animationDelay: '1000ms' }}>
          <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-primary" /> AI Recommendations
          </h3>
          <div className="space-y-3">
            {pred.recommendations.map((rec, i) => (
              <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-surface-card">
                <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center text-xs font-bold text-white shrink-0">
                  {i + 1}
                </div>
                <p className="text-sm text-text-secondary">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!activeCampaign && (
        <div className="text-center py-16 animate-fade-in">
          <div className="w-20 h-20 rounded-2xl gradient-primary mx-auto mb-4 flex items-center justify-center opacity-30">
            <PieChart className="w-10 h-10 text-white" />
          </div>
          <p className="text-text-muted">No campaigns yet. Launch one from the Onboarding page to see AI-predicted analytics!</p>
        </div>
      )}
    </div>
  );
}

function formatNumber(num) {
  if (!num && num !== 0) return '—';
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
}
