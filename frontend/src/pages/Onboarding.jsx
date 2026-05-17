/**
 * Onboarding Page — Restaurant profile form + pipeline trigger.
 * Shows campaign summary with approve button before launching.
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import { Store, Utensils, MapPin, Palette, Calendar, FileText, Star, Rocket, Image, Film, CheckCircle2, X } from 'lucide-react';

const toneOptions = ['Fun & Playful', 'Elegant & Premium', 'Bold & Edgy', 'Warm & Family', 'Trendy & Young', 'Classic & Traditional'];
const frequencyOptions = ['Daily', '3x/week', '5x/week', 'Weekdays Only', 'Weekends Only'];

// Frequency → display mapping vs actual demo generation logic
const FREQUENCY_MAP = {
  'Daily': { 
    displayPosts: 30, displayImages: 21, displayReels: 9, 
    posts: 7, images: 5, reels: 2, 
    schedule: '7 days a week, 1 post/day' 
  },
  '3x/week': { 
    displayPosts: 12, displayImages: 8, displayReels: 4, 
    posts: 3, images: 2, reels: 1, 
    schedule: 'Monday, Wednesday, Friday' 
  },
  '5x/week': { 
    displayPosts: 20, displayImages: 14, displayReels: 6, 
    posts: 5, images: 3, reels: 2, 
    schedule: 'Monday through Friday' 
  },
  'Weekdays Only': { 
    displayPosts: 20, displayImages: 14, displayReels: 6, 
    posts: 5, images: 3, reels: 2, 
    schedule: 'Monday through Friday' 
  },
  'Weekends Only': { 
    displayPosts: 24, displayImages: 16, displayReels: 8, 
    posts: 6, images: 4, reels: 2, 
    schedule: 'Saturday and Sunday (3 posts each day)' 
  },
};

export default function Onboarding() {
  const navigate = useNavigate();
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [triggering, setTriggering] = useState(false);
  const [confirmModal, setConfirmModal] = useState(null); // restaurant object to confirm
  const [form, setForm] = useState({
    name: '',
    cuisine_type: '',
    target_city: '',
    brand_tone: '',
    posting_frequency: '',
    description: '',
    specialties: '',
  });

  useEffect(() => {
    loadRestaurants();
  }, []);

  const loadRestaurants = async () => {
    try {
      const res = await api.get('/restaurants/');
      setRestaurants(res.data);
    } catch (err) {
      console.error('Failed to load restaurants:', err);
    }
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await api.post('/restaurants/', form);
      setRestaurants([...restaurants, res.data]);
      setForm({ name: '', cuisine_type: '', target_city: '', brand_tone: '', posting_frequency: '', description: '', specialties: '' });
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create restaurant');
    } finally {
      setSubmitting(false);
    }
  };

  const openConfirmModal = (restaurant) => {
    setConfirmModal(restaurant);
  };

  const triggerPipeline = async (restaurantId) => {
    setTriggering(true);
    setConfirmModal(null);
    try {
      await api.post('/campaigns/trigger', { restaurant_id: restaurantId });
      navigate('/agents?restaurant=' + restaurantId);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to start pipeline');
    } finally {
      setTriggering(false);
    }
  };

  const freqInfo = confirmModal ? FREQUENCY_MAP[confirmModal.posting_frequency] || FREQUENCY_MAP['Daily'] : null;

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-text-primary flex items-center gap-3">
          <Store className="w-8 h-8 text-primary" />
          Restaurant Onboarding
        </h1>
        <p className="text-text-muted mt-2">Set up your restaurant profile to generate AI-powered marketing campaigns</p>
      </div>

      {/* Existing Restaurants */}
      {restaurants.length > 0 && (
        <div className="mb-10 animate-fade-in" style={{ animationDelay: '100ms' }}>
          <h2 className="text-lg font-semibold text-text-primary mb-4">Your Restaurants</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {restaurants.map((r) => (
              <div key={r.id} className="card flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-text-primary">{r.name}</h3>
                  <p className="text-sm text-text-muted">{r.cuisine_type} • {r.target_city}</p>
                  <p className="text-xs text-text-muted mt-1">{r.brand_tone} tone • {r.posting_frequency}</p>
                </div>
                <button
                  onClick={() => openConfirmModal(r)}
                  disabled={triggering}
                  className="btn-primary text-sm"
                >
                  <Rocket className="w-4 h-4" />
                  {triggering ? 'Starting...' : 'Launch Campaign'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Campaign Confirmation Modal ── */}
      {confirmModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass rounded-2xl p-8 max-w-lg w-full mx-4 relative">
            <button onClick={() => setConfirmModal(null)} className="absolute top-4 right-4 text-text-muted hover:text-text-primary">
              <X className="w-5 h-5" />
            </button>

            <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
              <Rocket className="w-6 h-6 text-primary" /> Campaign Summary
            </h2>

            {/* Restaurant Info */}
            <div className="space-y-3 mb-6">
              <div className="flex justify-between text-sm">
                <span className="text-text-muted">Restaurant</span>
                <span className="font-semibold text-text-primary">{confirmModal.name}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-text-muted">Cuisine</span>
                <span className="text-text-secondary">{confirmModal.cuisine_type}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-text-muted">City</span>
                <span className="text-text-secondary">{confirmModal.target_city}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-text-muted">Brand Tone</span>
                <span className="text-text-secondary">{confirmModal.brand_tone}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-text-muted">Frequency</span>
                <span className="text-text-secondary">{confirmModal.posting_frequency}</span>
              </div>
            </div>

            {/* What will be produced */}
            <div className="bg-surface-light rounded-xl p-4 mb-6">
              <h3 className="text-sm font-semibold text-text-primary mb-3">What will be produced (Monthly):</h3>
              <div className="grid grid-cols-3 gap-3">
                <div className="text-center">
                  <div className="w-10 h-10 rounded-lg bg-primary/15 flex items-center justify-center mx-auto mb-1">
                    <FileText className="w-5 h-5 text-primary" />
                  </div>
                  <p className="text-lg font-bold text-text-primary">{freqInfo?.displayPosts || 30}</p>
                  <p className="text-xs text-text-muted">Total Posts</p>
                </div>
                <div className="text-center">
                  <div className="w-10 h-10 rounded-lg bg-accent/15 flex items-center justify-center mx-auto mb-1">
                    <Image className="w-5 h-5 text-accent" />
                  </div>
                  <p className="text-lg font-bold text-text-primary">{freqInfo?.displayImages || 21}</p>
                  <p className="text-xs text-text-muted">Images</p>
                </div>
                <div className="text-center">
                  <div className="w-10 h-10 rounded-lg bg-success/15 flex items-center justify-center mx-auto mb-1">
                    <Film className="w-5 h-5 text-success" />
                  </div>
                  <p className="text-lg font-bold text-text-primary">{freqInfo?.displayReels || 9}</p>
                  <p className="text-xs text-text-muted">Reels</p>
                </div>
              </div>
              <p className="text-xs text-accent mt-3 text-center font-medium bg-accent/10 py-1.5 rounded-md">
                Demo will generate 1 week ({freqInfo?.posts || 7} posts)
              </p>
              <p className="text-xs text-text-muted mt-2 text-center">
                Schedule: {freqInfo?.schedule || 'Custom schedule'}
              </p>
            </div>

            {/* Approve Button */}
            <button
              onClick={() => triggerPipeline(confirmModal.id)}
              className="btn-primary w-full text-base"
            >
              <CheckCircle2 className="w-5 h-5" />
              Approve & Launch Campaign
            </button>
          </div>
        </div>
      )}

      {/* Onboarding Form */}
      <div className="glass rounded-2xl p-8 animate-fade-in" style={{ animationDelay: '200ms' }}>
        <h2 className="text-xl font-semibold text-text-primary mb-6 flex items-center gap-2">
          <Utensils className="w-5 h-5 text-accent" />
          Add New Restaurant
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Restaurant Name */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <Store className="w-4 h-4" /> Restaurant Name
              </label>
              <input name="name" value={form.name} onChange={handleChange} className="input-field" placeholder="e.g., Karachi Biryani House" required />
            </div>

            {/* Cuisine Type */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <Utensils className="w-4 h-4" /> Cuisine Type
              </label>
              <input name="cuisine_type" value={form.cuisine_type} onChange={handleChange} className="input-field" placeholder="e.g., Pakistani, BBQ, Fast Food" required />
            </div>

            {/* Target City */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <MapPin className="w-4 h-4" /> Target City
              </label>
              <input name="target_city" value={form.target_city} onChange={handleChange} className="input-field" placeholder="e.g., Karachi, Lahore, Islamabad" required />
            </div>

            {/* Brand Tone */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <Palette className="w-4 h-4" /> Brand Tone
              </label>
              <select name="brand_tone" value={form.brand_tone} onChange={handleChange} className="input-field" required>
                <option value="">Select tone...</option>
                {toneOptions.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>

            {/* Posting Frequency */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <Calendar className="w-4 h-4" /> Posting Frequency
              </label>
              <select name="posting_frequency" value={form.posting_frequency} onChange={handleChange} className="input-field" required>
                <option value="">Select frequency...</option>
                {frequencyOptions.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>

            {/* Specialties */}
            <div>
              <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                <Star className="w-4 h-4" /> Specialties
              </label>
              <input name="specialties" value={form.specialties} onChange={handleChange} className="input-field" placeholder="e.g., Biryani, BBQ Platters, Naan" />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="flex items-center gap-2 text-sm text-text-secondary mb-2">
              <FileText className="w-4 h-4" /> Description
            </label>
            <textarea name="description" value={form.description} onChange={handleChange} className="input-field min-h-[100px] resize-y" placeholder="Tell us about your restaurant — what makes it special?" />
          </div>

          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <><Store className="w-4 h-4" />Add Restaurant</>}
          </button>
        </form>
      </div>
    </div>
  );
}
