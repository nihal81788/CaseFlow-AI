import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import extractor
import analyzer
import database
import organizer
import excel_export

INBOX_DIR = "inbox"

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignore directories and non-pdf files
        if event.is_directory or not event.src_path.lower().endswith('.pdf'):
            return
            
        print(f"\n[Watcher] New PDF detected: {event.src_path}")
        
        # 1. Wait a moment to ensure the file has finished copying
        time.sleep(1)
        
        try:
            # 2. Extract Text
            text = extractor.extract_text(event.src_path)
            
            # 3. Analyze Document with AI
            data = analyzer.analyze_document(text)
            
            print("\n--- Extracted Data Summary ---")
            print(json.dumps(data, indent=2))
            print("------------------------------\n")
            
            # 4. Save to Excel
            excel_export.append_to_excel(data)
            
            # 5. Organize/Move file
            new_file_path = organizer.organize_file(event.src_path, data)
            
            # 6. Save to database
            # We save the new filename in DB
            new_filename = os.path.basename(new_file_path)
            database.save_case(data, new_filename)
            
        except Exception as e:
            print(f"[Watcher] Error processing {event.src_path}: {e}")

def start_watching():
    """Starts the folder watchdog on the inbox directory."""
    os.makedirs(INBOX_DIR, exist_ok=True)
    
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, INBOX_DIR, recursive=False)
    observer.start()
    print(f"[Watcher] Started monitoring '{INBOX_DIR}' for new PDFs.")
    
    return observer
