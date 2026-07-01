import os
import shutil

ORGANIZED_DIR = "organized"

def ensure_folders_exist():
    """Creates the necessary subfolders inside organized/ if they don't exist."""
    folders = [
        "court_notices",
        "fir",
        "bail_orders",
        "affidavits",
        "agreements",
        "unsorted"
    ]
    for folder in folders:
        path = os.path.join(ORGANIZED_DIR, folder)
        os.makedirs(path, exist_ok=True)

def get_subfolder_for_type(doc_type):
    """Maps the document_type from AI to a specific folder name."""
    doc_type = doc_type.lower()
    if "notice" in doc_type: return "court_notices"
    if "fir" in doc_type: return "fir"
    if "bail" in doc_type: return "bail_orders"
    if "affidavit" in doc_type: return "affidavits"
    if "agreement" in doc_type: return "agreements"
    return "unsorted"

def organize_file(original_path, data):
    """
    Renames and moves the PDF to the correct subfolder based on its data.
    Format: DocumentType_CaseNumber_HearingDate.pdf
    """
    ensure_folders_exist()
    print(f"[Organizer] Organizing {os.path.basename(original_path)}...")
    
    doc_type_raw = data.get("document_type", "Unknown").replace("/", "-").strip()
    case_number = data.get("case_number", "UnknownCase")
    # Clean case number for filename
    case_number = str(case_number).replace("/", "-").replace("\\", "-").strip() if case_number else "UnknownCase"
    
    hearing_date = data.get("hearing_date", "NoDate")
    hearing_date = str(hearing_date).replace("/", "-").strip() if hearing_date else "NoDate"
    
    subfolder = get_subfolder_for_type(doc_type_raw)
    
    # Construct new filename
    new_filename = f"{doc_type_raw}_{case_number}_{hearing_date}.pdf".replace(" ", "_")
    new_path = os.path.join(ORGANIZED_DIR, subfolder, new_filename)
    
    # If a file with the same name exists, add a suffix
    counter = 1
    base_name, ext = os.path.splitext(new_path)
    while os.path.exists(new_path):
        new_path = f"{base_name}_{counter}{ext}"
        counter += 1
        
    try:
        shutil.move(original_path, new_path)
        print(f"[Organizer] Moved file to: {new_path}")
        return new_path
    except Exception as e:
        print(f"[Organizer] Failed to move file: {e}")
        return original_path
