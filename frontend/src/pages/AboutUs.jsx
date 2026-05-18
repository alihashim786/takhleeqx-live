/**
 * About Us Page — Project documentation and developer profiles.
 */
import { Mail, Sparkles, Bot, Rocket, Code2, Cpu, Phone } from 'lucide-react';

const GithubIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.24c3-.34 6-1.53 6-6.76a5.2 5.2 0 0 0-1.39-3.6 5 5 0 0 0-.12-3.53s-1.13-.36-3.7 1.38a12.9 12.9 0 0 0-7 0C5.13 3.44 4 3.8 4 3.8a5 5 0 0 0-.12 3.53A5.2 5.2 0 0 0 2.5 11c0 5.22 3 6.42 6 6.76a4.8 4.8 0 0 0-1 3.24v4" />
  </svg>
);

const LinkedinIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect width="4" height="12" x="2" y="9" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

const developers = [
  {
    name: 'Ali Hashim',
    role: 'Lead Developer & Architect',
    email: 'muhammadalihashim514@gmail.com',
    linkedin: 'https://www.linkedin.com/in/alihashimraza',
    github: 'https://github.com/alihashim786',
    description: 'Designed the core multi-agent LLM pipeline and full-stack architecture for TakhleeqX.',
    avatar: 'A'
  },
  {
    name: 'Ayyan Ahmad',
    role: 'AI & Backend Developer',
    email: 'ayan18709@gmail.com',
    linkedin: 'https://www.linkedin.com/in/ayyan-ahmad-087211387',
    github: 'https://github.com/',
    description: 'Developed the LLM prompts, agent state management, and integrated external generative APIs.',
    avatar: 'A'
  },
  {
    name: 'Hamza Jaffer',
    role: 'Frontend & UX Developer',
    email: 'hamzajaffer49@gmail.com',
    linkedin: 'https://www.linkedin.com/in/hamza-jaffer-37a02a23b/',
    github: 'http://github.com/hamzajaffer',
    description: 'Built the stunning, responsive user interface and implemented real-time agent monitoring.',
    avatar: 'H'
  }
];

export default function AboutUs() {
  return (
    <div className="max-w-5xl mx-auto space-y-12 pb-12 animate-fade-in">
      
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl font-bold text-text-primary tracking-tight">About TakhleeqX</h1>
        <p className="text-lg text-text-secondary max-w-2xl mx-auto leading-relaxed">
          The ultimate AI-powered marketing automation platform. Designed to empower Pakistani restaurants by generating agency-quality social media campaigns in minutes.
        </p>
      </div>

      {/* The Architecture */}
      <div className="glass p-8 rounded-3xl">
        <h2 className="text-2xl font-bold text-text-primary flex items-center gap-3 mb-6">
          <Cpu className="w-6 h-6 text-primary" />
          The Multi-Agent Architecture
        </h2>
        <p className="text-text-secondary leading-relaxed mb-8">
          TakhleeqX isn't just a standard wrapper around an AI model. It operates as a sophisticated <strong>Multi-Agent Pipeline</strong> (built with LangGraph and FastAPI), where specialized, autonomous AI agents collaborate to build your campaign from scratch.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-surface-light p-5 rounded-2xl border border-border/50">
            <Bot className="w-6 h-6 text-primary mb-3" />
            <h3 className="font-semibold text-text-primary mb-2">Trend Scout</h3>
            <p className="text-xs text-text-muted">Searches the web for real-time local Pakistani trends and global viral formats.</p>
          </div>
          <div className="bg-surface-light p-5 rounded-2xl border border-border/50">
            <Rocket className="w-6 h-6 text-accent mb-3" />
            <h3 className="font-semibold text-text-primary mb-2">Strategy Planner</h3>
            <p className="text-xs text-text-muted">Analyzes trends and your restaurant profile to build a highly targeted content strategy.</p>
          </div>
          <div className="bg-surface-light p-5 rounded-2xl border border-border/50">
            <Code2 className="w-6 h-6 text-success mb-3" />
            <h3 className="font-semibold text-text-primary mb-2">Generative Agents</h3>
            <p className="text-xs text-text-muted">The Content Writer, Visual Designer (DALL-E 3), and Reel Producer work in parallel.</p>
          </div>
          <div className="bg-surface-light p-5 rounded-2xl border border-border/50">
            <Sparkles className="w-6 h-6 text-purple-500 mb-3" />
            <h3 className="font-semibold text-text-primary mb-2">Supervisor</h3>
            <p className="text-xs text-text-muted">Evaluates the entire pipeline output, assigning a quality score before publishing.</p>
          </div>
        </div>
      </div>

      {/* The Team */}
      <div>
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4 bg-primary/10 border border-primary/20 p-6 rounded-2xl">
          <div>
            <h2 className="text-2xl font-bold text-text-primary">Meet the Developers</h2>
            <p className="text-text-muted mt-1">The team behind TakhleeqX</p>
          </div>
          <div className="flex items-center gap-4 bg-surface-card px-5 py-3 rounded-xl border border-border">
            <div className="w-10 h-10 rounded-full gradient-accent flex items-center justify-center">
              <Phone className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-xs font-semibold text-text-muted uppercase tracking-wider">Restaurant Onboarding & Help</p>
              <p className="text-sm font-bold text-text-primary">Call at: <span className="text-primary-light">+923215017784</span> or <span className="text-primary-light">+923259515626</span></p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {developers.map((dev, i) => (
            <div key={i} className="card hover:-translate-y-1 transition-transform duration-300">
              <div className="w-16 h-16 rounded-full gradient-primary flex items-center justify-center text-2xl font-bold text-white mb-4 mx-auto shadow-md">
                {dev.avatar}
              </div>
              <h3 className="text-lg font-bold text-text-primary text-center">{dev.name}</h3>
              <p className="text-sm font-medium text-primary text-center mb-4">{dev.role}</p>
              <p className="text-sm text-text-secondary text-center mb-6 leading-relaxed flex-grow">
                {dev.description}
              </p>
              
              <div className="flex items-center justify-center gap-3 pt-4 border-t border-border/50">
                <a 
                  href={`https://mail.google.com/mail/?view=cm&fs=1&to=${dev.email}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  title="Email via Gmail"
                  className="w-10 h-10 rounded-full bg-surface-light flex items-center justify-center text-text-muted hover:text-primary hover:bg-primary/10 transition-all duration-200"
                >
                  <Mail className="w-5 h-5" />
                </a>
                <a 
                  href={dev.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  title="LinkedIn"
                  className="w-10 h-10 rounded-full bg-surface-light flex items-center justify-center text-text-muted hover:text-blue-500 hover:bg-blue-500/10 transition-all duration-200"
                >
                  <LinkedinIcon className="w-5 h-5" />
                </a>
                <a 
                  href={dev.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  title="GitHub"
                  className="w-10 h-10 rounded-full bg-surface-light flex items-center justify-center text-text-muted hover:text-white hover:bg-white/10 transition-all duration-200"
                >
                  <GithubIcon className="w-5 h-5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Final Note */}
      <div className="text-center pt-8 border-t border-border">
        <p className="text-sm text-text-muted">
          Built with passion as a Final Year Project.<br/>
          TakhleeqX © {new Date().getFullYear()}
        </p>
      </div>

    </div>
  );
}
