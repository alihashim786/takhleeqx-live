/**
 * Agent Monitor Page — Real-time pipeline execution viewer.
 * Shows each agent's status (idle → running → done) with SSE streaming.
 * Displays trends, strategy, content writer output, and supervisor review.
 */
import { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import api from '../api/client';
import AgentCard from '../components/AgentCard';
import { Activity, CheckCircle2, AlertCircle, ArrowRight, TrendingUp, Compass, FileText, Lightbulb, Hash, MousePointerClick, X } from 'lucide-react';

const AGENTS = [
  { id: 'trend_scout', name: 'Trend Scout', description: 'Searching Pakistani & global trends using GPT-4o with web search', icon: '🔍' },
  { id: 'strategy_planner', name: 'Strategy Planner', description: 'Creating campaign strategy from trends + restaurant profile', icon: '📋' },
  { id: 'content_writer', name: 'Content Writer', description: 'Generating captions, hashtags, and CTAs per content pillar', icon: '✍️' },
  { id: 'visual_designer', name: 'Visual Designer', description: 'Creating AI images with GPT-Image-1 for each post', icon: '🎨' },
  { id: 'reel_producer', name: 'Reel Producer', description: 'Generating Urdu/Minglish meme scripts and triggering Creatomate video generation', icon: '🎬' },
  { id: 'campaign_publisher', name: 'Campaign Publisher', description: 'Assembling & publishing posts to the simulated feed', icon: '📤' },
  { id: 'supervisor', name: 'Supervisor', description: 'Reviewing pipeline quality, caching trends, and evaluating all agents', icon: '🧑‍💼' },
  { id: 'performance_predictor', name: 'Performance Predictor', description: 'Predicting engagement metrics using AI-based analytics', icon: '📊' },
];

export default function AgentMonitor() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const restaurantId = searchParams.get('restaurant');
  const [status, setStatus] = useState(null);
  const [agentStates, setAgentStates] = useState({});
  const [logs, setLogs] = useState([]);
  const [expandedSections, setExpandedSections] = useState({});
  const pollingRef = useRef(null);
  const [showMockInfo, setShowMockInfo] = useState(() => !localStorage.getItem('takhleeqx_openai_key'));

  const toggleSection = (section) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  useEffect(() => {
    if (!restaurantId) return;

    const poll = async () => {
      try {
        const res = await api.get(`/campaigns/status/${restaurantId}`);
        const data = res.data;
        setStatus(data);
        setLogs(data.logs || []);

        const states = {};
        const logNames = (data.logs || []).map(l => l.agent_name);
        AGENTS.forEach(agent => {
          const agentLog = (data.logs || []).find(l => l.agent_name === agent.name);
          if (agentLog) {
            states[agent.id] = { status: agentLog.status, message: agentLog.message };
          } else if (data.current_agent === agent.id) {
            states[agent.id] = { status: 'running', message: 'Processing...' };
          } else if (data.status === 'running' && !logNames.includes(agent.name)) {
            const myIdx = AGENTS.findIndex(a => a.id === agent.id);
            const currentIdx = AGENTS.findIndex(a => a.id === data.current_agent);
            if (currentIdx > myIdx && !states[agent.id]) {
              states[agent.id] = { status: 'done', message: 'Completed' };
            } else {
              states[agent.id] = { status: 'idle', message: '' };
            }
          } else {
            states[agent.id] = { status: states[agent.id]?.status || 'idle', message: '' };
          }
        });

        setAgentStates(states);

        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(pollingRef.current);
        }
      } catch (err) {
        console.error('Status poll error:', err);
      }
    };

    poll();
    pollingRef.current = setInterval(poll, 3000);

    return () => clearInterval(pollingRef.current);
  }, [restaurantId]);

  const isComplete = status?.status === 'completed';
  const isFailed = status?.status === 'failed';
  const isRunning = status?.status === 'running';

  // Extract data for display
  const trends = status?.trends || {};
  const localTrends = trends.local || [];
  const globalTrends = trends.global || [];
  const strategy = status?.strategy || {};
  const posts = status?.posts || [];

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-text-primary flex items-center gap-3">
          <Activity className="w-8 h-8 text-accent" />
          Agent Pipeline Monitor
        </h1>
        <p className="text-text-muted mt-2">
          {isRunning && 'Agents are working on your campaign...'}
          {isComplete && 'All agents completed successfully!'}
          {isFailed && 'Pipeline encountered an error.'}
          {!status && 'Select a restaurant and launch a campaign to begin.'}
          {status?.status === 'idle' && 'Pipeline is idle. Launch a campaign from Onboarding.'}
        </p>
      </div>

      {/* Mock Mode Instruction Box */}
      {showMockInfo && (
        <div className="mb-8 p-6 bg-accent/10 border border-accent/30 rounded-2xl relative animate-fade-in">
          <button onClick={() => setShowMockInfo(false)} className="absolute top-4 right-4 text-accent hover:text-accent-light">
            <X className="w-5 h-5" />
          </button>
          <div className="flex items-start gap-4">
            <div className="p-3 bg-accent/20 rounded-xl shrink-0 mt-1">
              <Activity className="w-6 h-6 text-accent" />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-lg">Live Execution Simulator</h3>
              <p className="text-text-muted mt-2 text-sm leading-relaxed">
                If an API Key was provided, the agents shown below would actively connect to LLMs and image/video generators 
                to build your campaign from scratch in real-time. 
              </p>
              <p className="text-text-muted mt-2 text-sm leading-relaxed">
                Because you are in <strong className="text-accent ml-1">Demo Mode</strong> with no API credits, we are fast-tracking the pipeline by securely restoring a previously executed, high-quality campaign. 
                All agent logs and outputs below are genuine artifacts from a real execution!
              </p>
              <p className="text-text-primary font-medium mt-3 text-sm flex items-center gap-2">
                <ArrowRight className="w-4 h-4 text-accent" />
                Proceed to the Social Feed, Analytics, and Campaign tabs to explore the results!
              </p>
              <button onClick={() => setShowMockInfo(false)} className="mt-4 px-5 py-2 bg-accent text-white rounded-lg text-sm font-semibold hover:bg-accent-light transition-colors">
                OK, Got it!
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Overall Status Banner */}
      {status && status.status !== 'idle' && (
        <div className={`card mb-6 animate-fade-in flex items-center gap-4 ${
          isComplete ? 'border-success' : isFailed ? 'border-danger' : 'border-accent animate-pulse-glow'
        }`}>
          {isComplete && <CheckCircle2 className="w-8 h-8 text-success shrink-0" />}
          {isFailed && <AlertCircle className="w-8 h-8 text-danger shrink-0" />}
          {isRunning && <div className="w-8 h-8 border-3 border-accent border-t-transparent rounded-full animate-spin shrink-0" />}
          <div className="flex-1">
            <p className="font-semibold text-text-primary">
              {isComplete && `Campaign "${status.strategy?.campaign_name || 'Generated'}" is ready!`}
              {isFailed && 'Pipeline failed — check logs below'}
              {isRunning && `Agent pipeline running — ${status.current_agent?.replace('_', ' ') || '...'}`}
            </p>
            {isComplete && (
              <div className="flex items-center gap-3 mt-1">
                <p className="text-sm text-text-muted">{status.posts_count || 0} posts generated</p>
                {status.quality_score && (
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                    status.quality_score >= 80 ? 'bg-success/20 text-success' :
                    status.quality_score >= 60 ? 'bg-accent/20 text-accent' : 'bg-danger/20 text-danger'
                  }`}>
                    Quality: {status.quality_score}/100
                  </span>
                )}
              </div>
            )}
          </div>
          {isComplete && (
            <button onClick={() => navigate('/feed')} className="btn-primary text-sm shrink-0">
              View Feed <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      )}

      {/* Agent Pipeline */}
      <div className="space-y-4">
        {AGENTS.map((agent, i) => (
          <div key={agent.id} className="relative">
            {/* Connector line */}
            {i < AGENTS.length - 1 && (
              <div className="absolute left-10 top-full w-0.5 h-4 bg-border z-0" />
            )}
            <AgentCard
              name={`${agent.icon} ${agent.name}`}
              description={agent.description}
              status={agentStates[agent.id]?.status || 'idle'}
              message={agentStates[agent.id]?.message}
              order={i}
            />

            {/* ── Trend Scout Output ── */}
            {agent.id === 'trend_scout' && agentStates[agent.id]?.status === 'done' && localTrends.length > 0 && (
              <div className="ml-20 mt-2 animate-fade-in">
                <button onClick={() => toggleSection('trends')} className="text-sm font-medium text-primary-light hover:text-primary flex items-center gap-1 mb-2">
                  <TrendingUp className="w-4 h-4" /> {expandedSections.trends ? 'Hide' : 'Show'} Top Trends Used
                </button>
                {expandedSections.trends && (
                  <div className="glass rounded-xl p-4 space-y-3">
                    <div>
                      <h4 className="text-xs font-semibold text-accent uppercase tracking-wider mb-2 flex items-center gap-1">
                        <Compass className="w-3 h-3" /> Local Trends (Pakistan)
                      </h4>
                      <div className="flex flex-wrap gap-1.5">
                        {localTrends.slice(0, 5).map((t, idx) => (
                          <span key={idx} className="px-2 py-1 rounded-full text-xs bg-primary/15 text-primary-light border border-primary/20">
                            {typeof t === 'string' ? t : t.topic || t.name || JSON.stringify(t).slice(0, 40)}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-xs font-semibold text-accent uppercase tracking-wider mb-2 flex items-center gap-1">
                        <TrendingUp className="w-3 h-3" /> Global Trends
                      </h4>
                      <div className="flex flex-wrap gap-1.5">
                        {globalTrends.slice(0, 5).map((t, idx) => (
                          <span key={idx} className="px-2 py-1 rounded-full text-xs bg-accent/15 text-accent border border-accent/20">
                            {typeof t === 'string' ? t : t.topic || t.name || JSON.stringify(t).slice(0, 40)}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* ── Strategy Planner Output ── */}
            {agent.id === 'strategy_planner' && agentStates[agent.id]?.status === 'done' && strategy.campaign_name && (
              <div className="ml-20 mt-2 animate-fade-in">
                <button onClick={() => toggleSection('strategy')} className="text-sm font-medium text-primary-light hover:text-primary flex items-center gap-1 mb-2">
                  <Lightbulb className="w-4 h-4" /> {expandedSections.strategy ? 'Hide' : 'Show'} Strategy Summary
                </button>
                {expandedSections.strategy && (
                  <div className="glass rounded-xl p-4 space-y-2">
                    <p className="text-sm"><span className="font-semibold text-text-primary">Campaign:</span> <span className="text-text-secondary">{strategy.campaign_name}</span></p>
                    <p className="text-sm"><span className="font-semibold text-text-primary">Audience:</span> <span className="text-text-secondary">{strategy.target_audience}</span></p>
                    <p className="text-sm"><span className="font-semibold text-text-primary">Tone:</span> <span className="text-text-secondary">{strategy.tone}</span></p>
                    {strategy.content_pillars && (
                      <div>
                        <p className="text-sm font-semibold text-text-primary mb-1">Content Pillars:</p>
                        <div className="flex flex-wrap gap-1.5">
                          {strategy.content_pillars.map((p, idx) => (
                            <span key={idx} className="px-2 py-1 rounded-full text-xs bg-success/15 text-success border border-success/20">
                              {typeof p === 'string' ? p : p.name || p.title || JSON.stringify(p).slice(0, 30)}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* ── Content Writer Output ── */}
            {agent.id === 'content_writer' && agentStates[agent.id]?.status === 'done' && posts.length > 0 && (
              <div className="ml-20 mt-2 animate-fade-in">
                <button onClick={() => toggleSection('content')} className="text-sm font-medium text-primary-light hover:text-primary flex items-center gap-1 mb-2">
                  <FileText className="w-4 h-4" /> {expandedSections.content ? 'Hide' : 'Show'} Generated Content ({posts.length} posts)
                </button>
                {expandedSections.content && (
                  <div className="space-y-3">
                    {posts.map((post, idx) => (
                      <div key={idx} className="glass rounded-xl p-4">
                        <p className="text-xs font-semibold text-accent uppercase tracking-wider mb-1">
                          Post {idx + 1} — {post.content_pillar || 'General'}
                        </p>
                        <p className="text-sm text-text-secondary mb-2 line-clamp-3">{post.caption}</p>
                        {post.hashtags && post.hashtags.length > 0 && (
                          <p className="text-xs text-primary-light flex items-center gap-1 mb-1">
                            <Hash className="w-3 h-3" />
                            {post.hashtags.map(h => h.startsWith('#') ? h : `#${h}`).join(' ')}
                          </p>
                        )}
                        {post.cta && (
                          <p className="text-xs text-accent flex items-center gap-1">
                            <MousePointerClick className="w-3 h-3" /> {post.cta}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Supervisor Notes */}
      {isComplete && status?.supervisor_notes && (
        <div className="mt-6 glass rounded-2xl p-6 animate-fade-in">
          <h3 className="text-lg font-semibold text-text-primary mb-2 flex items-center gap-2">🧑‍💼 Supervisor Review</h3>
          <p className="text-sm text-text-secondary whitespace-pre-line">{status.supervisor_notes}</p>
        </div>
      )}

      {/* Logs Panel */}
      {logs.length > 0 && (
        <div className="mt-6 glass rounded-2xl p-6 animate-fade-in">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Agent Logs</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {logs.map((log, i) => (
              <div key={i} className="flex items-start gap-3 text-sm">
                <span className={`status-dot ${log.status} mt-1.5 shrink-0`} />
                <div>
                  <span className="font-medium text-text-primary">{log.agent_name}</span>
                  <span className="text-text-muted mx-2">—</span>
                  <span className="text-text-secondary">{log.message}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No restaurant selected */}
      {!restaurantId && (
        <div className="text-center py-16 animate-fade-in">
          <div className="w-20 h-20 rounded-2xl gradient-primary mx-auto mb-4 flex items-center justify-center opacity-30">
            <Activity className="w-10 h-10 text-white" />
          </div>
          <p className="text-text-muted">Go to Onboarding and launch a campaign to see agents in action</p>
          <button onClick={() => navigate('/')} className="btn-secondary mt-4">
            Go to Onboarding
          </button>
        </div>
      )}
    </div>
  );
}
