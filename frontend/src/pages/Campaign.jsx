/**
 * Campaign Page — Displays the generated campaign strategy.
 */
import { useState, useEffect } from 'react';
import api from '../api/client';
import { BarChart3, Target, MessageSquare, Calendar, Hash, Palette, TrendingUp, ChevronDown, ChevronUp } from 'lucide-react';

export default function Campaign() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const res = await api.get('/campaigns/');
      setCampaigns(res.data);
    } catch (err) {
      console.error('Failed to load campaigns:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto">
        <div className="space-y-4">
          {[1, 2, 3].map(i => <div key={i} className="shimmer h-32 rounded-2xl" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-text-primary flex items-center gap-3">
          <BarChart3 className="w-8 h-8 text-primary" />
          Campaign Dashboard
        </h1>
        <p className="text-text-muted mt-2">View generated marketing strategies and campaign details</p>
      </div>

      {campaigns.length === 0 ? (
        <div className="text-center py-16 animate-fade-in">
          <div className="w-20 h-20 rounded-2xl gradient-primary mx-auto mb-4 flex items-center justify-center opacity-30">
            <BarChart3 className="w-10 h-10 text-white" />
          </div>
          <p className="text-text-muted">No campaigns yet. Launch one from the Onboarding page!</p>
        </div>
      ) : (
        <div className="space-y-6">
          {campaigns.map((campaign, idx) => (
            <div key={campaign.id} className="glass rounded-2xl overflow-hidden animate-fade-in" style={{ animationDelay: `${idx * 100}ms` }}>
              {/* Campaign Header */}
              <div
                className="p-6 cursor-pointer flex items-center justify-between"
                onClick={() => setExpanded(expanded === campaign.id ? null : campaign.id)}
              >
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      campaign.status === 'published' ? 'bg-success/20 text-success' : 'bg-accent/20 text-accent'
                    }`}>
                      {campaign.status}
                    </span>
                    <span className="text-xs text-text-muted">
                      {new Date(campaign.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-text-primary">{campaign.campaign_name}</h2>
                  {campaign.target_audience && (
                    <p className="text-sm text-text-muted mt-1 flex items-center gap-2">
                      <Target className="w-4 h-4" /> {campaign.target_audience}
                    </p>
                  )}
                </div>
                {expanded === campaign.id ? <ChevronUp className="w-5 h-5 text-text-muted" /> : <ChevronDown className="w-5 h-5 text-text-muted" />}
              </div>

              {/* Expanded Details */}
              {expanded === campaign.id && (
                <div className="px-6 pb-6 space-y-6 border-t border-border pt-6">
                  {/* Strategy Overview */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {campaign.tone && (
                      <div className="card">
                        <div className="flex items-center gap-2 text-sm text-text-muted mb-1">
                          <Palette className="w-4 h-4" /> Tone
                        </div>
                        <p className="font-semibold text-text-primary">{campaign.tone}</p>
                      </div>
                    )}
                    {campaign.strategy_data?.campaign_duration && (
                      <div className="card">
                        <div className="flex items-center gap-2 text-sm text-text-muted mb-1">
                          <Calendar className="w-4 h-4" /> Duration & Freq
                        </div>
                        <p className="font-semibold text-text-primary">
                          {campaign.strategy_data.campaign_duration} • {campaign.posting_schedule?.frequency || 'Custom'}
                        </p>
                      </div>
                    )}
                    {campaign.strategy_data?.hashtag_strategy && (
                      <div className="card">
                        <div className="flex items-center gap-2 text-sm text-text-muted mb-1">
                          <Hash className="w-4 h-4" /> Hashtag Strategy
                        </div>
                        <p className="font-semibold text-text-primary text-sm line-clamp-2">{campaign.strategy_data.hashtag_strategy}</p>
                      </div>
                    )}
                  </div>
                  
                  {/* Scheduled Times */}
                  {campaign.posting_schedule?.best_times && campaign.posting_schedule.best_times.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-text-primary mb-2 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-accent" /> Scheduled Posting Times
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {campaign.posting_schedule.best_times.map((time, i) => (
                          <span key={i} className="px-3 py-1 bg-surface-card border border-border rounded-lg text-xs font-medium text-text-secondary">
                            {time}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Content Pillars */}
                  {campaign.content_pillars && campaign.content_pillars.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-text-primary mb-3 flex items-center gap-2">
                        <MessageSquare className="w-5 h-5 text-accent" /> Content Pillars
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {campaign.content_pillars.map((pillar, i) => (
                          <div key={i} className="card">
                            <div className="flex items-center gap-2 mb-2">
                              <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center text-sm font-bold text-white">
                                {i + 1}
                              </div>
                              <h4 className="font-semibold text-text-primary">{pillar.pillar_name || pillar}</h4>
                            </div>
                            {pillar.description && <p className="text-sm text-text-muted">{pillar.description}</p>}
                            {pillar.example_topic && (
                              <p className="text-xs text-accent mt-2">💡 {pillar.example_topic}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Key Messages */}
                  {campaign.strategy_data?.key_messages && (
                    <div>
                      <h3 className="text-lg font-semibold text-text-primary mb-3">Key Messages</h3>
                      <div className="flex flex-wrap gap-2">
                        {campaign.strategy_data.key_messages.map((msg, i) => (
                          <span key={i} className="px-3 py-1.5 rounded-xl bg-primary/10 text-primary-light text-sm">
                            {msg}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Trends Used */}
                  {campaign.trends_data?.synthesis?.recommended_angle && (
                    <div className="card bg-surface border-primary/30">
                      <div className="flex items-center gap-2 mb-2">
                        <TrendingUp className="w-5 h-5 text-primary" />
                        <h3 className="font-semibold text-text-primary">Trend-Based Angle</h3>
                      </div>
                      <p className="text-text-secondary">{campaign.trends_data.synthesis.recommended_angle}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
