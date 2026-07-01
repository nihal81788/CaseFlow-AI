import os
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import date

import database

REPORTS_DIR = "reports"

def check_morning_hearings():
    """Checks for today's hearings and logs them to the console."""
    print("[Scheduler] Checking today's hearings...")
    hearings = database.get_todays_hearings()
    
    if not hearings:
        print("[Scheduler] No hearings scheduled for today.")
        return
        
    print(f"[Scheduler] Found {len(hearings)} hearings for today:")
    for case in hearings:
        case_number, court_name, next_action = case
        print(f"  - Case: {case_number} | Court: {court_name} | Action: {next_action}")

def generate_evening_report():
    """Generates a text report of all cases processed today."""
    print("[Scheduler] Running evening report job...")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    cases_today = database.get_all_cases_today()
    today_str = date.today().isoformat()
    report_path = os.path.join(REPORTS_DIR, f"report_{today_str}.txt")
    
    with open(report_path, "w") as f:
        f.write(f"--- CaseFlow AI Daily Report : {today_str} ---\n\n")
        f.write(f"Total documents processed today: {len(cases_today)}\n\n")
        
        for idx, case in enumerate(cases_today, 1):
            case_number, doc_type, next_action, summary = case
            f.write(f"{idx}. Case: {case_number} ({doc_type})\n")
            f.write(f"   Summary: {summary}\n")
            f.write(f"   Next Action: {next_action}\n")
            f.write("-" * 40 + "\n")
            
    print(f"[Scheduler] Evening report saved to {report_path}")

def start_scheduler():
    """Initializes and starts the APScheduler."""
    scheduler = BackgroundScheduler()
    
    # Morning job at 8:00 AM
    scheduler.add_job(check_morning_hearings, 'cron', hour=8, minute=0)
    
    # Evening job at 8:00 PM
    scheduler.add_job(generate_evening_report, 'cron', hour=20, minute=0)
    
    scheduler.start()
    print("[Scheduler] Scheduler started. Morning hearing checks at 8 AM, Evening reports at 8 PM.")
    return scheduler
