import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import extractor
import analyzer
import organizer
import excel_export

INBOX_DIR = "inbox"

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith('.pdf'):
            return
            
        print(f"\n[Watcher] New PDF detected: {event.src_path}")
        
        time.sleep(1)
        
        try:
            text = extractor.extract_text(event.src_path)
            
            data = analyzer.analyze_document(text)
            
            print("\n--- Extracted Data Summary ---")
            print(json.dumps(data, indent=2))
            print("------------------------------\n")
            
            excel_export.append_to_excel(data)
            
            new_file_path = organizer.organize_file(event.src_path, data)
            
        except Exception as e:
            print(f"[Watcher] Error processing {event.src_path}: {e}")

def start_watching():
    os.makedirs(INBOX_DIR, exist_ok=True)
    
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, INBOX_DIR, recursive=False)
    observer.start()
    print(f"[Watcher] Started monitoring '{INBOX_DIR}' for new PDFs.")
    
    return observer
