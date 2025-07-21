# 🧠 JobScout AI — Real Jobs. Real Insights. Faster Interviews.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/jobscout-ai/ci.yml)](https://github.com/your-org/jobscout-ai/actions)
[![Open Issues](https://img.shields.io/github/issues/your-org/jobscout-ai)](https://github.com/your-org/jobscout-ai/issues)

JobScout AI helps job seekers cut through fake, expired, or ghosted job postings by providing AI-powered job authenticity scores, crowdsourced applicant signals, and personalized outreach assistance—all through a simple web app and Chrome extension.

---

## 🔍 Features

- ✅ **Job Authenticity Score** — AI and rule-based scoring of job listings for credibility
- 📡 **Crowdsourced Signals** — Feedback loop showing user outcomes (ghosted, interviewed, etc.)
- 🗂 **Application Tracker** — Dashboard to manage and tag job applications
- ✉️ **Outreach Assistant** — LLM-generated personalized outreach messages
- 🧩 **Chrome Extension** — Sidebar insights on LinkedIn, Indeed, etc.

---

## 🛠 Tech Stack

| Layer         | Technology             |
|---------------|------------------------|
| Frontend      | React + TailwindCSS    |
| Backend       | FastAPI (Python)       |
| Database      | PostgreSQL + SQLAlchemy|
| NLP/AI        | OpenAI API + LangChain |
| Browser Ext.  | Chrome Manifest V3     |
| Hosting       | Vercel / Railway       |

---

## 📦 Project Structure

```
jobscout-ai/
├── frontend/        # React + Tailwind web app
├── backend/         # FastAPI backend with models and APIs
├── docs/            # Product documentation
├── mockups/         # UI mockups and PRD references
└── README.md
```

---

## 🚀 Getting Started

### 🧰 Prerequisites
- Node.js + npm
- Python 3.10+
- PostgreSQL
- Chrome (for extension)

### ⚙️ Frontend
```bash
cd frontend
npm install
npm run dev
```

### 🖥 Backend
```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feat/some-feature`)
3. Commit your changes (`git commit -m 'add some feature'`)
4. Push to the branch (`git push origin feat/some-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
