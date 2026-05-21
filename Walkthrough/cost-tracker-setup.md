# AI Cost Tracker - Setup Guide

## Step 1: Install Python Dependencies

```bash
pip install notion-client
```

## Step 2: Get Your Notion API Key

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name: "AI Cost Tracker"
4. Click "Submit"
5. Copy the "Internal Integration Token" (starts with ntn_...)  

## Step 3: Get Your Database ID

1. Open your "AI Tools" Notion database
2. Look at the URL:
   https://www.notion.so/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=...
   └─────────────────────────────────┘
            This is your Database ID
3. Copy the 32-character string

## Step 4: Share Database with Integration

1. In your Notion database, click "..."
2. Click "Connections"
3. Search for "AI Cost Tracker"
4. Click "Connect"

## Step 5: Update the Script

Open cost_tracker.py and update these lines:

```python
NOTION_API_KEY = "ntn_your_key_here"
DATABASE_ID    = "your_database_id_here"
```

## Step 6: Run It!

### One-time report:
```bash
python cost_tracker.py
```

### Watch mode (auto-detects new submissions):
```bash
python cost_tracker.py --watch
```

### Watch with custom interval (30 seconds):
```bash
python cost_tracker.py --watch 30
```

## What You'll See

### One-time report:
```
==========================================================
       💰 AI INTELLIGENCE STACK — COST TRACKER
==========================================================
  🕐  Monday, May 18 2026  11:30:00 PM
----------------------------------------------------------
  📝 LATEST IDEA:
  Title           : Replit
  Tokens          : 1,789
  Cost            : $0.0167

  📊 CUMULATIVE TOTALS:
  Total Ideas          : 5
  Ideas Evaluated      : 5
  Input Tokens         : 4,295
  Output Tokens        : 4,650
  Total Tokens         : 8,945
  Total Cost           : $0.0828
  Avg Cost / Idea      : $0.0166

  📈 MONTHLY PROJECTIONS:
  20 ideas/month       : $0.33
  50 ideas/month       : $0.83
  100 ideas/month      : $1.66
==========================================================
```

### Watch mode - new submission detected:
```
🆕 NEW SUBMISSION DETECTED!
  Title           : My New AI Idea
  Category        : AI Application
  Submitted By    : Zafar
  Input Tokens    : 859
  Output Tokens   : 930
  Total Tokens    : 1,789
  This Idea Cost  : $0.0167
```

## Log File

Every run saves `ai_cost_log.json` with:
- Last updated timestamp
- Summary totals
- Last 20 submissions with costs

## Troubleshooting

**"notion-client not found"**
Run: pip install notion-client

**"Could not find database"**
- Check your Database ID is correct
- Make sure you connected the integration (Step 4)

**"Unauthorized"**
- Check your NOTION_API_KEY is correct
- Make sure it starts with "ntn_"

**Tokens showing as 0**
- The ideas haven't been evaluated yet
- Or the Make.com scenario hasn't mapped Input/Output Tokens yet
