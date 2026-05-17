# TakhleeqX — AI-Powered Marketing Automation Platform

## Architecture

TakhleeqX is a **LangGraph-powered multi-agent marketing automation platform** that orchestrates five specialized AI agents through a stateful directed graph:

1. **Trend Scout** — GPT-4o + Web Search → discovers Pakistani & global viral trends
2. **Strategy Planner** — GPT-4o → creates campaign strategy with content pillars
3. **Content Writer** — GPT-4o → generates captions, hashtags, CTAs per pillar
4. **Visual Designer** — DALL-E 3 → creates hero images for each post
5. **Campaign Publisher** — SQLAlchemy → persists posts to simulated social feed

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **AI Framework**: LangGraph (StateGraph) + LangChain + OpenAI
- **Frontend**: React + Vite + Tailwind CSS v4
- **Auth**: JWT + bcrypt
- **Real-time**: SSE (Server-Sent Events) for live agent monitoring

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173** in your browser.

## API Keys Required

| Key | Required | Source |
|-----|----------|--------|
| `OPENAI_API_KEY` | Yes | Already in `.env` |
| `JWT_SECRET` | Yes | Already in `.env` |

## Demo Flow

1. Register/Login → Create account
2. Onboarding → Add restaurant profile (name, cuisine, city, tone)
3. Launch Campaign → Triggers the 5-agent pipeline
4. Agent Monitor → Watch agents work in real-time
5. Campaign → View generated strategy and content pillars
6. Social Feed → See published posts in Instagram-style layout
7. Analytics → Mock performance metrics
