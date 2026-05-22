#!/usr/bin/env python3
"""
AI Intelligence Stack - Cost Tracker
Automatically tracks token usage and costs from Notion database
Run once: python cost_tracker.py
Watch mode: python cost_tracker.py --watch
"""

#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# CONFIGURATION - Set these in your .env file!
# ============================================================
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID    = os.getenv("DATABASE_ID")

# Claude Sonnet 4 Pricing
INPUT_TOKEN_PRICE  = 0.000003   # $3.00 per 1M input tokens
OUTPUT_TOKEN_PRICE = 0.000015   # $15.00 per 1M output tokens
# ============================================================

# Validate config
if not NOTION_API_KEY or NOTION_API_KEY == "your_notion_key_here":
    print("❌ NOTION_API_KEY not set! Add it to your .env file.")
    exit(1)

if not DATABASE_ID or DATABASE_ID == "your_notion_database_id_here":
    print("❌ DATABASE_ID not set! Add it to your .env file.")
    exit(1)

try:
    from notion_client import Client
    notion = Client(auth=NOTION_API_KEY)
except ImportError:
    print("❌ Missing dependency. Run: pip install notion-client")
    exit(1)


def get_all_ideas():
    """Fetch all ideas from Notion database"""
    results = []
    cursor = None

    while True:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            start_cursor=cursor,
            sorts=[{"timestamp": "created_time", "direction": "descending"}]
        )
        results.extend(response["results"])
        if not response["has_more"]:
            break
        cursor = response["next_cursor"]

    return results


def parse_idea(page):
    """Extract fields from a Notion page"""
    props = page["properties"]

    def get_title(prop):
        if prop and prop.get("title"):
            texts = prop["title"]
            return texts[0]["plain_text"] if texts else "Untitled"
        return "Untitled"

    def get_number(prop):
        if prop and prop.get("number") is not None:
            return float(prop["number"])
        return 0.0

    def get_select(prop):
        if prop and prop.get("select"):
            return prop["select"]["name"]
        return "Unknown"

    def get_rich_text(prop):
        if prop and prop.get("rich_text"):
            texts = prop["rich_text"]
            return texts[0]["plain_text"] if texts else ""
        return ""

    input_tokens  = get_number(props.get("Input Tokens", {}))
    output_tokens = get_number(props.get("Output Tokens", {}))

    # Recalculate cost locally in case Notion formula hasn't updated
    calculated_cost = (input_tokens * INPUT_TOKEN_PRICE) + (output_tokens * OUTPUT_TOKEN_PRICE)
    notion_cost = get_number(props.get("Estimated Cost", {}))
    final_cost = notion_cost if notion_cost > 0 else calculated_cost

    return {
        "title":          get_title(props.get("Title", {})),
        "category":       get_select(props.get("Category", {})),
        "submitted_by":   get_rich_text(props.get("Submitted By", {})),
        "input_tokens":   int(input_tokens),
        "output_tokens":  int(output_tokens),
        "total_tokens":   int(input_tokens + output_tokens),
        "estimated_cost": final_cost,
        "submitted_at":   page.get("created_time", ""),
        "page_id":        page["id"]
    }


def calculate_totals(ideas):
    """Calculate aggregate stats"""
    ideas_with_tokens = [i for i in ideas if i["total_tokens"] > 0]

    total_input   = sum(i["input_tokens"]  for i in ideas_with_tokens)
    total_output  = sum(i["output_tokens"] for i in ideas_with_tokens)
    total_tokens  = total_input + total_output
    total_cost    = sum(i["estimated_cost"] for i in ideas_with_tokens)
    avg_cost      = total_cost / len(ideas_with_tokens) if ideas_with_tokens else 0

    return {
        "total_ideas":        len(ideas),
        "ideas_with_tokens":  len(ideas_with_tokens),
        "total_input_tokens": total_input,
        "total_output_tokens":total_output,
        "total_tokens":       total_tokens,
        "total_cost":         total_cost,
        "avg_cost":           avg_cost
    }


def display_report(ideas, totals, last_idea=None, new_submission=False):
    """Print a formatted cost report"""
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

    print("\n" + "="*58)
    print(f"{BOLD}{CYAN}      💰 AI INTELLIGENCE STACK — COST TRACKER{RESET}")
    print("="*58)
    print(f"  🕐  {datetime.now().strftime('%A, %B %d %Y  %I:%M:%S %p')}")
    print("-"*58)

    if last_idea and new_submission:
        print(f"\n{BOLD}  🆕 NEW SUBMISSION DETECTED!{RESET}")
        print(f"  {'Title':<16}: {last_idea['title']}")
        print(f"  {'Category':<16}: {last_idea['category']}")
        print(f"  {'Submitted By':<16}: {last_idea['submitted_by']}")
        print(f"  {'Input Tokens':<16}: {last_idea['input_tokens']:,}")
        print(f"  {'Output Tokens':<16}: {last_idea['output_tokens']:,}")
        print(f"  {'Total Tokens':<16}: {last_idea['total_tokens']:,}")
        print(f"  {'This Idea Cost':<16}: {GREEN}${last_idea['estimated_cost']:.4f}{RESET}")
        print("-"*58)

    elif last_idea:
        print(f"\n{BOLD}  📝 LATEST IDEA:{RESET}")
        print(f"  {'Title':<16}: {last_idea['title']}")
        print(f"  {'Tokens':<16}: {last_idea['total_tokens']:,}")
        print(f"  {'Cost':<16}: {GREEN}${last_idea['estimated_cost']:.4f}{RESET}")
        print("-"*58)

    print(f"\n{BOLD}  📊 CUMULATIVE TOTALS:{RESET}")
    print(f"  {'Total Ideas':<20}: {totals['total_ideas']}")
    print(f"  {'Ideas Evaluated':<20}: {totals['ideas_with_tokens']}")
    print(f"  {'Input Tokens':<20}: {totals['total_input_tokens']:,}")
    print(f"  {'Output Tokens':<20}: {totals['total_output_tokens']:,}")
    print(f"  {'Total Tokens':<20}: {YELLOW}{totals['total_tokens']:,}{RESET}")
    print(f"  {'Total Cost':<20}: {GREEN}${totals['total_cost']:.4f}{RESET}")
    print(f"  {'Avg Cost / Idea':<20}: ${totals['avg_cost']:.4f}")
    print("-"*58)

    # Budget projections
    avg = totals["avg_cost"]
    print(f"\n{BOLD}  📈 MONTHLY PROJECTIONS:{RESET}")
    print(f"  {'20 ideas/month':<22}: ${avg * 20:.2f}")
    print(f"  {'50 ideas/month':<22}: ${avg * 50:.2f}")
    print(f"  {'100 ideas/month':<22}: ${avg * 100:.2f}")

    # Token budget warning
    if totals["total_cost"] > 5.00:
        print(f"\n  {RED}⚠️  Total spend exceeds $5.00{RESET}")
    elif totals["total_cost"] > 2.00:
        print(f"\n  {YELLOW}ℹ️  Total spend approaching $5.00 threshold{RESET}")

    print("="*58 + "\n")


def save_log(totals, ideas):
    """Save results to local JSON log file"""
    log_data = {
        "last_updated": datetime.now().isoformat(),
        "summary": totals,
        "recent_submissions": [
            {
                "title":       i["title"],
                "category":    i["category"],
                "tokens":      i["total_tokens"],
                "cost":        round(i["estimated_cost"], 4),
                "submitted_at":i["submitted_at"]
            }
            for i in ideas[:20]
        ]
    }
    with open(COST_LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)


def watch_mode(interval=60):
    """Watch Notion for new idea submissions"""
    CYAN  = "\033[96m"
    RESET = "\033[0m"

    print(f"\n{CYAN}🔍 Watching for new submissions every {interval} seconds...{RESET}")
    print("Press Ctrl+C to stop\n")

    last_count = -1

    while True:
        try:
            raw    = get_all_ideas()
            ideas  = [parse_idea(p) for p in raw]
            totals = calculate_totals(ideas)
            count  = totals["total_ideas"]

            if last_count == -1:
                # First run
                print(f"✅ Connected! Found {count} ideas in Notion.")
                display_report(ideas, totals, ideas[0] if ideas else None)
                save_log(totals, ideas)
                last_count = count

            elif count > last_count:
                # New submission detected!
                new_idea = ideas[0] if ideas else None
                display_report(ideas, totals, new_idea, new_submission=True)
                save_log(totals, ideas)
                last_count = count

            else:
                print(f"⏳ [{datetime.now().strftime('%H:%M:%S')}] "
                      f"No new ideas. Total: {count} | "
                      f"Cost so far: ${totals['total_cost']:.4f}", end="\r")

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n👋 Cost tracker stopped. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(interval)


def one_time_report():
    """Run a single cost report"""
    print("\n⏳ Fetching data from Notion...")
    try:
        raw    = get_all_ideas()
        ideas  = [parse_idea(p) for p in raw]
        totals = calculate_totals(ideas)

        display_report(ideas, totals, ideas[0] if ideas else None)
        save_log(totals, ideas)
        print(f"✅ Report saved to {COST_LOG_FILE}\n")

    except Exception as e:
        print(f"\n❌ Error connecting to Notion: {e}")
        print("Check your NOTION_API_KEY and DATABASE_ID in the script.\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        watch_mode(interval=interval)
    else:
        one_time_report()
