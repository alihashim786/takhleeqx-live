/**
 * PostCard — Instagram-style post card for the simulated social feed.
 */
import { Heart, MessageCircle, Send, Bookmark, MoreHorizontal } from 'lucide-react';
import { useState } from 'react';

export default function PostCard({ post, restaurantName = 'TakhleeqX Restaurant' }) {
  const [liked, setLiked] = useState(false);
  const [saved, setSaved] = useState(false);
  // Default to image if it exists, otherwise video
  const [viewMode, setViewMode] = useState(post.image_url ? 'image' : 'video');

  const formattedTime = post.published_at 
    ? new Date(post.published_at).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })
    : 'Scheduled';

  return (
    <div className="card p-0 overflow-hidden animate-fade-in">
      {/* Post Header */}
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full gradient-primary flex items-center justify-center text-xs font-bold text-white">
            {restaurantName[0]}
          </div>
          <div>
            <p className="text-sm font-semibold text-text-primary">{restaurantName}</p>
            <p className="text-xs text-text-muted">{post.platform || 'Instagram'} • Scheduled for {formattedTime}</p>
          </div>
        </div>
        <MoreHorizontal className="w-5 h-5 text-text-muted" />
      </div>

      {/* Media (Video or Image) */}
      <div className="relative aspect-square bg-surface-light group">
        {/* Toggle buttons if both exist */}
        {post.video_url && post.image_url && (
          <div className="absolute top-2 right-2 z-10 flex gap-1 bg-black/50 backdrop-blur-md p-1 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => setViewMode('image')}
              className={`px-2 py-1 text-xs font-medium rounded ${viewMode === 'image' ? 'bg-white text-black' : 'text-white hover:bg-white/20'}`}
            >
              Image
            </button>
            <button
              onClick={() => setViewMode('video')}
              className={`px-2 py-1 text-xs font-medium rounded ${viewMode === 'video' ? 'bg-white text-black' : 'text-white hover:bg-white/20'}`}
            >
              Reel
            </button>
          </div>
        )}

        <div className="w-full h-full">
          {viewMode === 'image' && post.image_url && (
            <img
              src={post.image_url}
              alt={post.alt_text || 'Post image'}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          )}
          {viewMode === 'video' && post.video_url && (
            <video
              src={post.video_url}
              className="w-full h-full object-cover"
              autoPlay
              loop
              muted
              playsInline
            />
          )}
          
          {(!post.image_url && !post.video_url) && (
            <div className="w-full h-full flex items-center justify-center text-text-muted">
              <div className="text-center">
                <div className="w-16 h-16 rounded-2xl gradient-primary mx-auto mb-3 flex items-center justify-center opacity-40">
                  <span className="text-2xl">🎨</span>
                </div>
                <p className="text-sm">AI-Generated Media</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="px-4 py-3">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-4">
            <button onClick={() => setLiked(!liked)} className="transition-transform hover:scale-110">
              <Heart className={`w-6 h-6 ${liked ? 'fill-red-500 text-red-500' : 'text-text-primary'}`} />
            </button>
            <MessageCircle className="w-6 h-6 text-text-primary hover:text-text-secondary transition-colors cursor-pointer" />
            <Send className="w-6 h-6 text-text-primary hover:text-text-secondary transition-colors cursor-pointer" />
          </div>
          <button onClick={() => setSaved(!saved)} className="transition-transform hover:scale-110">
            <Bookmark className={`w-6 h-6 ${saved ? 'fill-white text-white' : 'text-text-primary'}`} />
          </button>
        </div>

        {/* Likes count */}
        <p className="text-sm font-semibold text-text-primary mb-2">
          {liked ? '1,248' : '1,247'} likes
        </p>

        {/* Caption */}
        <div className="text-sm text-text-primary mb-2">
          <span className="font-semibold mr-1">{restaurantName.toLowerCase().replace(/\s/g, '')}</span>
          {post.caption}
        </div>

        {/* Hashtags */}
        {post.hashtags && post.hashtags.length > 0 && (
          <p className="text-sm text-primary-light">
            {post.hashtags.map(h => h.startsWith('#') ? h : `#${h}`).join(' ')}
          </p>
        )}

        {/* CTA */}
        {post.cta && (
          <p className="text-xs text-accent mt-2 font-medium">{post.cta}</p>
        )}
      </div>
    </div>
  );
}

function formatTimeAgo(date) {
  const now = new Date();
  const diff = Math.floor((now - date) / 1000);
  if (diff < 60) return 'Just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}
