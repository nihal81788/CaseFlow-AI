import time
import os

import watcher

def ensure_base_folders():
    for folder in ["inbox", "organized", "reports", "data"]:
        os.makedirs(folder, exist_ok=True)

def main():
    print("="*50)
    print(" Starting CaseFlow AI - Civic-Tech Legal Assistant ")
    print("="*50)
    
    ensure_base_folders()
    
    observer = watcher.start_watching()
    
    print("\n[System] CaseFlow AI is now running.")
    print("[System] Drop PDF files into the 'inbox/' folder to process them.")
    print("[System] Press Ctrl+C to stop.\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[System] Stopping CaseFlow AI...")
        observer.stop()
        print("[System] CaseFlow AI stopped successfully.")
    
    observer.join()

if __name__ == "__main__":
    main()
