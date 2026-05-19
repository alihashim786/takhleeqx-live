# 🚀 TakhleeqX — Multi-Agent AI Marketing Automation

**TakhleeqX** is a cutting-edge B2B SaaS platform designed to automate the entire social media marketing workflow for restaurants. By leveraging a sophisticated **Multi-Agent AI Architecture**, TakhleeqX replaces traditional marketing teams by autonomously researching trends, formulating strategies, generating captions, designing images, rendering video reels, and publishing campaigns.

---

## 🧠 The Multi-Agent Architecture

TakhleeqX orchestrates a powerful stateful directed graph using **LangGraph**, routing data seamlessly between 6 specialized, autonomous AI agents:

1. 🕵️ **Trend Scout:** Uses web searching and LLMs to discover localized Pakistani trends and global viral formats.
2. 🗺️ **Strategy Planner:** Analyzes the restaurant's profile and current trends to formulate a targeted marketing strategy with concrete content pillars.
3. ✍️ **Content Writer:** Generates platform-specific, high-engaging captions, viral hashtags, and powerful CTAs.
4. 🎨 **Visual Designer:** Dynamically prompts image generation models (DALL-E) to create stunning, brand-aligned promotional graphics.
5. 🎬 **Reel Producer:** Generates voiceover scripts and on-screen text, then triggers the Creatomate API to render dynamic, meme-style MP4 video reels via code.
6. 🛡️ **Supervisor:** Acts as the final quality control layer, reviewing the entire campaign pipeline and assigning a quality score before approval and publishing.

---

## 🛠️ Technology Stack

TakhleeqX is built using a modern, scalable, and high-performance tech stack:

### Frontend (Client-Side)
* **React.js & Vite:** Component-based SPA architecture for lightning-fast, reactive user experiences.
* **Tailwind CSS:** Comprehensive styling utilizing modern glassmorphism, responsive grids, and premium B2B SaaS aesthetics.
* **Vercel:** Deployed on Vercel's edge network for rapid global delivery.

### Backend (Server-Side)
* **FastAPI (Python):** Asynchronous, high-performance REST API handling complex LLM pipeline execution.
* **SQLAlchemy & SQLite:** Robust ORM for secure persistence of user accounts, restaurant profiles, and campaign data.
* **Render:** 24/7 cloud hosting for the Python backend infrastructure.

### AI Engine & Integrations
* **LangGraph:** Core routing and state management for the multi-agent workflow.
* **OpenAI (GPT-4o & Image Models):** The foundational intelligence for strategic planning, text generation, and image synthesis.
* **Creatomate API:** Programmatic cloud rendering for dynamic video reels.
* **Resend API:** Secure, automated transactional email delivery for platform onboarding and alerts.

---

## 🎯 Key Features
* **Live Agent Monitor:** Watch the AI pipeline think, decide, and generate content in real-time.
* **Simulated Social Feed:** View generated posts and reels exactly as they would appear on Instagram or TikTok.
* **Graceful Fallbacks:** Built-in robustness ensures the platform safely falls back to high-quality stock assets if third-party generative APIs reach rate limits, ensuring zero downtime for users.
* **Comprehensive Analytics:** Predictive performance metrics estimating reach, engagement, and conversion for the generated campaigns.

---

## 💻 Quick Start (Development)

### Backend Setup
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the Vite development server
npm run dev
```

*Built as a comprehensive Final Year Project showcasing advanced Generative AI and Full-Stack Engineering.*
