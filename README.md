# JobScout AI

AI-powered job authenticity scoring, crowdsourced applicant signals, and personalized outreach for job seekers.

JobScout AI helps you cut through fake, expired, or ghosted job postings by scoring every listing for credibility — then generates tailored outreach messages to help you land real interviews.

## Features

**Real Job Search** — Search and scrape real job listings from LinkedIn, Indeed, and Glassdoor directly from the dashboard. Filter by keywords, location, and remote. One-click "Apply Now" opens the posting and auto-tracks your application.

**Trust Score Engine** — Every job posting gets a 0-100 trust score computed from 4 signals:
- **Freshness** (25pts) — Newer postings score higher; stale/expired ones get flagged
- **Crowdsourced Feedback** (35pts) — User-reported outcomes: hired, interviewed, ghosted, fake
- **Company Verification** (15pts) — Company name, website presence
- **Posting Quality** (25pts) — Salary transparency, description depth, red flag detection

**Multi-LLM Outreach** — Generate personalized cover letters, recruiter messages, and follow-ups using Claude, OpenAI GPT-4o, Google Gemini, or local Ollama models.

**Chrome Extension** — See trust scores directly on LinkedIn, Indeed, and Glassdoor job postings. Submit quick feedback without leaving the page.

**Application Tracker** — Track every job you apply to. "Apply Now" opens the original posting and automatically logs the application with timestamp.

**Full-Stack Dashboard** — Search-first experience: find jobs, see trust scores, read crowd signals, generate outreach, track applications — all in one place.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + SQLAlchemy + PostgreSQL |
| AI/LLM | Claude, OpenAI, Gemini, Ollama (auto-detected) |
| Trust Score | 4-factor composite algorithm (16 unit tests) |
| Auth | JWT (bcrypt + python-jose) |
| Frontend | Next.js 14 + TypeScript + TailwindCSS |
| Extension | Chrome Manifest V3 |

## Project Structure

```
jobscout-ai/
├── backend/
│   ├── app/
│   │   ├── api/              # REST endpoints (auth, jobs, feedback, outreach, trust score)
│   │   ├── models/           # SQLAlchemy ORM (User, JobPosting, Application, Feedback, Outreach)
│   │   ├── schemas/          # Pydantic validation (enums, pagination, trust score detail)
│   │   ├── services/         # Business logic (auth, trust score engine, outreach generation)
│   │   ├── llm/              # Multi-LLM abstraction (provider, factory, prompts)
│   │   ├── config.py         # Centralized pydantic-settings config
│   │   └── dependencies.py   # Shared FastAPI dependencies (get_db, get_current_user)
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages (login, register, dashboard, job detail)
│       ├── components/       # UI components (TrustScoreBadge, JobCard, FeedbackForm, etc.)
│       ├── hooks/            # Auth provider
│       └── lib/              # API client, types, auth context
├── extension/
│   ├── manifest.json         # Chrome Manifest V3
│   ├── content.js            # Trust score overlay on LinkedIn/Indeed/Glassdoor
│   ├── background.js         # Service worker for API communication
│   └── popup/                # Extension popup with score + feedback form
└── README.md
```

## Quick Start (Docker)

```bash
docker-compose up
```

That's it. Opens:
- **Dashboard:** http://localhost:3000
- **API docs:** http://localhost:8000/docs

**Demo login:** `demo@jobscout.ai` / `demo1234`

Pre-loaded with 10 job postings, 27 community feedbacks, and computed trust scores so you can explore immediately.

## Manual Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (or SQLite for local dev)

### Backend

```bash
cd backend
cp .env.example .env        # Edit with your database URL and API keys
pip install -r requirements.txt
PYTHONPATH=. python seed.py  # Load demo data
PYTHONPATH=. uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Dashboard: http://localhost:3000

### Chrome Extension

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension/` directory
4. Navigate to any LinkedIn/Indeed/Glassdoor job posting

### LLM Configuration

JobScout AI auto-detects your LLM provider from environment variables:

| Provider | Variable | Default Model |
|----------|----------|---------------|
| Claude | `ANTHROPIC_API_KEY` | claude-sonnet-4-5 |
| OpenAI | `OPENAI_API_KEY` | gpt-4o |
| Gemini | `GOOGLE_API_KEY` | gemini-2.0-flash |
| Ollama | (none needed) | llama3.1 |

## Trust Score Algorithm

```
Total Score (0-100) = Freshness + Feedback + Company + Quality

Freshness (0-25):   Based on days since posted. 7 days = 25, 90+ days = 2, inactive = 0
Feedback  (0-35):   Weighted user outcomes. hired=+1.0, interviewed=+0.8, ghosted=-0.6, fake=-1.0
Company   (0-15):   Company name present (+5), URL present (+5), both validated (+5)
Quality   (0-25):   Salary shown (+8), title (+4), location (+3), description (+5), red flags (-3 each)

Confidence: high (10+ feedbacks), medium (3-9), low (<3)
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | No | Create account, get JWT |
| POST | /auth/login | No | Login, get JWT |
| GET | /auth/me | Yes | Get current user |
| GET | /job-postings | No | List jobs (paginated, searchable) |
| GET | /job-postings/{id} | No | Job detail |
| POST | /job-postings | Yes | Create job posting |
| PUT | /job-postings/{id} | Yes | Update job posting |
| DELETE | /job-postings/{id} | Yes | Delete job posting |
| GET | /trust-score/{job_id} | No | Get trust score breakdown |
| POST | /trust-score/{job_id}/refresh | No | Recompute trust score |
| POST | /job-feedbacks | Yes | Submit feedback (auto-recomputes score) |
| GET | /job-feedbacks | No | List feedbacks |
| GET | /job-feedbacks/aggregation/{job_id} | No | Aggregated outcomes |
| POST | /outreach/generate | Yes | Generate outreach message via LLM |
| GET | /outreach/templates | Yes | List saved messages |
| POST | /job-applications | Yes | Track an application |
| GET | /job-applications | Yes | List my applications |
| POST | /job-search/scrape | Yes | Scrape real jobs from LinkedIn/Indeed/Glassdoor |

## Testing

```bash
cd backend
PYTHONPATH=. pytest tests/ -v
```

## License

MIT
