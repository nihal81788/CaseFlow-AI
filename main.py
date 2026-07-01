import time
import os

import database
import watcher
import scheduler

def ensure_base_folders():
    """Create all necessary base directories before starting."""
    for folder in ["inbox", "organized", "reports", "data"]:
        os.makedirs(folder, exist_ok=True)

def main():
    print("="*50)
    print(" Starting CaseFlow AI - Civic-Tech Legal Assistant ")
    print("="*50)
    
    # 1. Ensure folders exist
    ensure_base_folders()
    
    # 2. Initialize DB
    database.init_db()
    
    # 3. Start scheduler (background)
    sched = scheduler.start_scheduler()
    
    # 4. Start folder watcher (background)
    observer = watcher.start_watching()
    
    print("\n[System] CaseFlow AI is now running.")
    print("[System] Drop PDF files into the 'inbox/' folder to process them.")
    print("[System] Press Ctrl+C to stop.\n")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[System] Stopping CaseFlow AI...")
        observer.stop()
        sched.shutdown()
        print("[System] CaseFlow AI stopped successfully.")
    
    observer.join()

if __name__ == "__main__":
    main()
