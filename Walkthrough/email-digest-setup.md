# Email Digest Setup - Make.com
# Daily AI Intelligence Stack Summary

## Overview
Sends a daily email at 5 AM with:
- All ideas submitted in the last 24 hours
- Token usage summary
- Cost breakdown
- Top scoring ideas

---

## Part 1: Create the Scenario

1. Go to Make.com
2. Click "Create a new scenario"
3. Name it: "Daily Email Digest"
4. Click "Create"

---

## Part 2: Add the Modules

### Module 1: Schedule Trigger

1. Click "+"
2. Search: "Schedule"
3. Select: "Every day"
4. Time: 05:00 AM (or your preferred time)
5. Timezone: Select your timezone
6. Click "OK"

---

### Module 2: Notion - Search Objects (Last 24 Hours)

1. Click "+"
2. Search: "Notion"
3. Select: "Search Objects"
4. Connection: Your Notion connection
5. Database: "AI Tools"
6. Filter: Click "Add filter"
   - Property: "Created time"
   - Condition: "is on or after"
   - Value: Click field → Search "addHours" →
     `{{addHours(now; -24)}}`
7. Sort: "Created time" - Descending
8. Limit: 100
9. Click "OK"

---

### Module 3: Notion - Search Objects (All Time, for totals)

1. Click "+"
2. Search: "Notion"
3. Select: "Search Objects"
4. Connection: Your Notion connection
5. Database: "AI Tools"
6. No filters (gets everything)
7. Limit: 1000
8. Click "OK"

---

### Module 4: Tools - Set Variable (Daily Stats)

1. Click "+"
2. Search: "Tools"
3. Select: "Set multiple variables"

Add these variables:

Variable 1:
- Name: `dailyCount`
- Value: `{{length(2.array)}}`

Variable 2:
- Name: `dailyTokens`
- Value: `{{add(sum(2.array; "Input Tokens"); sum(2.array; "Output Tokens"))}}`

Variable 3:
- Name: `dailyCost`
- Value: `{{sum(2.array; "Estimated Cost")}}`

5. Click "OK"

---

### Module 5: Tools - Set Variable (All Time Stats)

1. Click "+"
2. Select: "Set multiple variables"

Add these variables:

Variable 1:
- Name: `totalIdeas`
- Value: `{{length(3.array)}}`

Variable 2:
- Name: `totalTokens`
- Value: `{{add(sum(3.array; "Input Tokens"); sum(3.array; "Output Tokens"))}}`

Variable 3:
- Name: `totalCost`
- Value: `{{sum(3.array; "Estimated Cost")}}`

Variable 4:
- Name: `avgCost`
- Value: `{{if(length(3.array) > 0; divide(sum(3.array; "Estimated Cost"); length(3.array)); 0)}}`

5. Click "OK"

---

### Module 6: Email (Gmail or SMTP)

**Option A: Gmail**
1. Click "+"
2. Search: "Gmail"
3. Select: "Send an email"
4. Connect your Gmail account

**Option B: SMTP (any email)**
1. Click "+"
2. Search: "Email"
3. Select: "Send an email (SMTP)"
4. Configure your email settings

---

### Module 6: Configure the Email

**To:** your@email.com (or instructor's email)

**Subject:**
```
📊 AI Intelligence Stack - Daily Digest {{formatDate(now; "MMM DD, YYYY")}}
```

**Content type:** HTML

**Body (HTML):**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
    .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .header { background: linear-gradient(135deg, #f59e0b, #d97706); padding: 32px 24px; text-align: center; }
    .header h1 { color: white; margin: 0; font-size: 24px; }
    .header p { color: rgba(255,255,255,0.85); margin: 8px 0 0; font-size: 14px; }
    .section { padding: 24px; border-bottom: 1px solid #f0f0f0; }
    .section h2 { color: #333; font-size: 16px; margin: 0 0 16px; text-transform: uppercase; letter-spacing: 1px; }
    .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    .stat-card { background: #fafafa; border-radius: 8px; padding: 16px; text-align: center; border: 1px solid #e5e5e5; }
    .stat-value { font-size: 28px; font-weight: bold; color: #f59e0b; }
    .stat-label { font-size: 12px; color: #888; text-transform: uppercase; margin-top: 4px; }
    .idea-row { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
    .idea-row:last-child { border-bottom: none; }
    .idea-title { font-weight: bold; color: #333; font-size: 14px; }
    .idea-meta { font-size: 12px; color: #888; margin-top: 4px; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-orange { background: #fff3e0; color: #f59e0b; }
    .badge-green { background: #e8f5e9; color: #4caf50; }
    .footer { padding: 20px 24px; text-align: center; background: #fafafa; }
    .footer p { color: #888; font-size: 12px; margin: 0; }
    .no-ideas { text-align: center; padding: 40px 20px; color: #888; }
    .no-ideas p { font-size: 14px; }
  </style>
</head>
<body>
  <div class="container">

    <!-- Header -->
    <div class="header">
      <h1>📊 AI Intelligence Stack</h1>
      <p>Daily Digest — {{formatDate(now; "dddd, MMMM D, YYYY")}}</p>
    </div>

    <!-- Today's Stats -->
    <div class="section">
      <h2>📅 Last 24 Hours</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{4.dailyCount}}</div>
          <div class="stat-label">Ideas Submitted</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{formatNumber(4.dailyTokens; 0)}}</div>
          <div class="stat-label">Tokens Used</div>
        </div>
        <div class="stat-card" style="grid-column: span 2;">
          <div class="stat-value">${{formatNumber(4.dailyCost; 4)}}</div>
          <div class="stat-label">Today's AI Cost</div>
        </div>
      </div>
    </div>

    <!-- Today's Ideas -->
    <div class="section">
      <h2>💡 Ideas Submitted Today</h2>
      {{#if 4.dailyCount > 0}}
        {{#each 2.array}}
        <div class="idea-row">
          <div class="idea-title">{{this.properties.Title.title.[0].plain_text}}</div>
          <div class="idea-meta">
            <span class="badge badge-orange">{{this.properties.Category.select.name}}</span>
            &nbsp;by {{this.properties["Submitted By"].rich_text.[0].plain_text}}
            &nbsp;·&nbsp;Score: {{this.properties["Potential Score"].number}}
            &nbsp;·&nbsp;Cost: ${{formatNumber(this.properties["Estimated Cost"].formula.number; 4)}}
          </div>
        </div>
        {{/each}}
      {{else}}
        <div class="no-ideas">
          <p>😴 No ideas submitted in the last 24 hours.</p>
        </div>
      {{/if}}
    </div>

    <!-- All Time Stats -->
    <div class="section">
      <h2>📈 All-Time Totals</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{5.totalIdeas}}</div>
          <div class="stat-label">Total Ideas</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${{formatNumber(5.totalCost; 2)}}</div>
          <div class="stat-label">Total Spent</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{formatNumber(5.totalTokens; 0)}}</div>
          <div class="stat-label">Total Tokens</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${{formatNumber(5.avgCost; 4)}}</div>
          <div class="stat-label">Avg Cost / Idea</div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>🤖 AI Intelligence Stack — AI Practitioner Class</p>
      <p style="margin-top: 6px;">This digest is generated automatically every morning at 5 AM</p>
    </div>

  </div>
</body>
</html>
```

---

## Part 3: Save & Activate

1. Click "Save" (bottom left)
2. Turn the scenario ON (toggle at bottom)
3. **Test it manually:**
   - Click "Run once"
   - Check your inbox!

---

## Part 4: Verify Email Arrives

**Check for:**
- ✅ Subject line with today's date
- ✅ Today's submission count
- ✅ List of ideas submitted
- ✅ Token usage and costs
- ✅ All-time totals

---

## Troubleshooting

**Email not arriving:**
- Check spam folder
- Verify Gmail connection is authorized
- Check "Run once" shows green checkmarks

**Ideas not showing:**
- Check Notion filter date formula
- Verify Notion connection has access to database
- Make sure ideas were submitted in last 24 hours

**Costs showing as 0:**
- Make sure Input/Output Token columns are mapped in main scenario
- Verify "Estimated Cost" formula is set up in Notion

---

## Optional: Send to Multiple Recipients

In the email module:
- Add multiple email addresses separated by commas
- Or create a distribution list

## Optional: Change Digest Time

In Module 1 (Schedule):
- Change time to whatever works for your class
- Consider 7 AM before class starts
- Or Sunday evening for weekly digest

## Optional: Weekly Digest Instead

Change Module 1 from "Every day" to "Every week":
- Day: Monday
- Time: 8:00 AM

