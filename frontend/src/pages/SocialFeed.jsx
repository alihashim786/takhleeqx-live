/**
 * Social Feed Page — Simulated Instagram/Facebook feed.
 */
import { useState, useEffect } from 'react';
import api from '../api/client';
import PostCard from '../components/PostCard';
import { Rss, Grid, List, Camera } from 'lucide-react';

export default function SocialFeed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('feed'); // 'feed' or 'grid'

  useEffect(() => {
    loadFeed();
  }, []);

  const loadFeed = async () => {
    try {
      const res = await api.get('/feed/');
      setPosts(res.data);
    } catch (err) {
      console.error('Failed to load feed:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="space-y-4">
          {[1, 2, 3].map(i => <div key={i} className="shimmer h-96 rounded-2xl" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-8 animate-fade-in flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-text-primary flex items-center gap-3">
            <Camera className="w-8 h-8 text-pink-500" />
            Simulated Social Feed
          </h1>
          <p className="text-text-muted mt-2">Preview your AI-generated posts as they would appear on social media</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode('feed')}
            className={`p-2 rounded-lg transition-colors ${viewMode === 'feed' ? 'bg-primary text-white' : 'text-text-muted hover:bg-surface-hover'}`}
          >
            <List className="w-5 h-5" />
          </button>
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-primary text-white' : 'text-text-muted hover:bg-surface-hover'}`}
          >
            <Grid className="w-5 h-5" />
          </button>
        </div>
      </div>

      {posts.length === 0 ? (
        <div className="text-center py-16 animate-fade-in">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-pink-500 to-purple-500 mx-auto mb-4 flex items-center justify-center opacity-30">
            <Rss className="w-10 h-10 text-white" />
          </div>
          <p className="text-text-muted">No published posts yet. Run a campaign to see your feed!</p>
        </div>
      ) : viewMode === 'feed' ? (
        /* Feed View — Instagram-style */
        <div className="max-w-xl mx-auto space-y-6">
          {posts.map((post, i) => (
            <div key={post.id} style={{ animationDelay: `${i * 100}ms` }}>
              <PostCard post={post} />
            </div>
          ))}
        </div>
      ) : (
        /* Grid View — Instagram profile grid */
        <div className="grid grid-cols-3 gap-1 rounded-2xl overflow-hidden">
          {posts.map((post) => (
            <div key={post.id} className="aspect-square relative group cursor-pointer bg-surface-card animate-fade-in">
              {post.image_url ? (
                <img src={post.image_url} alt={post.alt_text} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center gradient-primary opacity-40">
                  <span className="text-4xl">🎨</span>
                </div>
              )}
              {/* Hover overlay */}
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-6">
                <div className="text-center text-white">
                  <p className="font-bold">❤ 1.2K</p>
                </div>
                <div className="text-center text-white">
                  <p className="font-bold">💬 48</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
