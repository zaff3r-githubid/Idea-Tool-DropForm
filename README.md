# 🧠 AI Intelligence Stack — Idea Drop Form

> A serverless AI-powered idea collection and evaluation system built for AI Practitioners.

[![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-orange)](https://https://zaff3r-githubid.github.io/Idea-Tool-DropForm/)
[![Make.com](https://img.shields.io/badge/Automation-Make.com-purple)](https://make.com)
[![Claude AI](https://img.shields.io/badge/AI-Claude%20Sonnet-blue)](https://anthropic.com)
[![Notion](https://img.shields.io/badge/Database-Notion-black)](https://notion.so)

---

## 📌 What It Does

Students and practitioners submit AI tool ideas through a web form. Each submission is automatically:

1. **Evaluated by Claude AI** — scores the idea on feasibility, value, innovation, and efficiency
2. **Logged to Notion** — stored with full AI analysis and token usage data
3. **Tracked for cost** — token usage and API costs displayed in real-time on the form
4. **Monitored via LangSmith** — full AI observability and run tracking

---

## ✨ Features

- 📝 **Idea submission form** — title, category, description, impact, resources, file attachments
- 🤖 **AI evaluation** — automatic scoring (0-100) with detailed breakdown
- 📊 **AI Observability widget** — tracks token usage and API costs per submission
- 💾 **Notion database** — all ideas stored with scores, tags, difficulty ratings
- 📎 **File attachments** — uploads to Dropbox, linked in Notion
- 🔄 **Success overlay** — animated confirmation with auto-reset
- 🔍 **LangSmith monitoring** — full AI pipeline observability

---

## 🏗️ Architecture

```
Web Form (GitHub Pages)
    │
    ▼
Make.com Webhook
    │
    ├── Claude API (claude-sonnet-4-6)
    │       └── Evaluates idea → returns JSON scores
    │
    ├── LangSmith (HTTP)
    │       └── Logs AI run for observability
    │
    └── Router
            ├── Has Attachments → Dropbox → Notion
            └── No Attachments  → Notion
                    └── Returns token usage to webform
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Hosting | GitHub Pages |
| Automation | Make.com |
| AI Model | Claude Sonnet (Anthropic) |
| Database | Notion |
| File Storage | Dropbox |
| Observability | LangSmith |
| Cost Tracking | Python + localStorage |

---

## 🚀 Getting Started

### Prerequisites

- [Make.com](https://make.com) account (free tier)
- [Notion](https://notion.so) account with API integration
- [Anthropic API](https://console.anthropic.com) key
- [LangSmith](https://smith.langchain.com) account (optional)
- [Dropbox](https://dropbox.com) account (for file attachments)
- Python 3.8+ (for local cost tracker)

---

### 1. Fork & Deploy the Form

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/IDEA-TOOL-DROPFORM.git
cd IDEA-TOOL-DROPFORM

# Deploy to GitHub Pages
# Go to Settings → Pages → Deploy from main branch
```

---

### 2. Setup Make.com Scenario

Import or recreate the following modules:

| Module | Service | Purpose |
|--------|---------|---------|
| 1 | Webhooks | Receive form submissions |
| 9 | HTTP | Call Claude API for evaluation |
| 7 | JSON | Parse Claude's JSON response |
| 26 | HTTP | Log run to LangSmith |
| 19 | Router | Split attachment/no-attachment paths |
| 27 | Dropbox | Upload attached file |
| 28 | Dropbox | Create shareable link |
| 8/31 | Notion | Create database entry |

---

### 3. Configure Notion Database

Create a Notion database with these properties:

| Property | Type |
|----------|------|
| Title | Title |
| Category | Select |
| Description | Text |
| Submitted By | Text |
| Expected Impact | Select |
| Resources Needed | Text |
| Potential Score | Number |
| Difficulty | Select |
| Summary | Text |
| Input Tokens | Number |
| Output Tokens | Number |
| Total Tokens | Formula: `prop("Input Tokens") + prop("Output Tokens")` |
| Estimated Cost | Formula: `(prop("Input Tokens") * 0.000003) + (prop("Output Tokens") * 0.000015)` |

---

### 4. Setup Local Cost Tracker (Optional)

The cost tracker runs locally and connects to Notion to display detailed analytics.

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your actual keys

# Run one-time report
python cost_tracker.py

# Run in watch mode (auto-detects new submissions)
python cost_tracker.py --watch
```

---

## 🔐 Security

This project follows these security practices:

- ✅ **No API keys in the repo** — all credentials in Make.com or `.env`
- ✅ **Webhook URLs are public by design** — they're endpoints, not credentials
- ✅ **`.env` is gitignored** — never committed to the repo
- ✅ **Cost tracking uses localStorage** — no backend needed, no data exposed
- ✅ **Notion API stays server-side** — only accessed through Make.com

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Where to Get It |
|----------|-------------|-----------------|
| `NOTION_API_KEY` | Notion integration token | [notion.so/my-integrations](https://notion.so/my-integrations) |
| `DATABASE_ID` | Your Notion database ID | From your database URL |

---

## 💰 AI Cost Tracking

The form includes a built-in **AI Observability widget** that tracks:

- Total ideas evaluated
- Total tokens used (input + output)
- Total API cost
- Average cost per idea
- Last submission breakdown

**How it works:**
1. Make.com returns token data in the webhook response
2. Browser stores cumulative totals in `localStorage`
3. Widget updates automatically after each submission
4. Data persists across page loads

**No additional API calls or Make.com operations required!**

---

## 📊 Claude Pricing Reference

| Token Type | Rate |
|-----------|------|
| Input tokens | $3.00 / 1M tokens |
| Output tokens | $15.00 / 1M tokens |
| Avg per submission | ~$0.017 |

---

## 📁 Project Structure

```
IDEA-TOOL-DROPFORM/
├── index.html          # Main web form
├── cost_tracker.py     # Local AI cost analytics script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Protects sensitive files
├── README.md           # This file
├── LICENSE             # License
└── Walkthrough/        # Setup guides and documentation
```

---

## 🔧 Troubleshooting

**Form submits but nothing appears in Notion**
- Check Make.com scenario is turned ON
- Verify webhook URL in `index.html` matches Make.com
- Check Make.com execution history for errors

**Cost widget shows 0**
- Make sure Webhook Response modules are added to both Notion paths in Make.com
- Check browser console for errors
- Verify Make.com returns `input_tokens` and `output_tokens` in response

**Cost tracker shows "NOTION_API_KEY not set"**
- Create `.env` file from `.env.example`
- Fill in your actual Notion API key and Database ID
- Run `pip install -r requirements.txt` first

**File attachments not working**
- Verify Dropbox connection in Make.com
- Check file size is under 10MB
- Supported formats: PDF, PPT, PPTX, DOC, DOCX, JPG, PNG, GIF

---

## 📧 Daily Email Digest

An optional Make.com scenario sends a daily digest at 5 AM with:
- Ideas submitted in the last 24 hours
- Token usage summary
- Cost breakdown
- All-time totals

Setup guide available in the `Walkthrough/` folder.

---

## 🎓 About

Built as part of the **AI Practitioner Class** to demonstrate:
- Serverless AI pipeline architecture
- LLM API integration
- Workflow automation with Make.com
- AI observability and cost tracking
- Secure deployment practices

---

## 📄 License

See [LICENSE](LICENSE) for details.
