import fitz  # PyMuPDF
import os

def extract_text(pdf_path):
    """
    Extracts text from a given PDF file.
    Returns plain string or an error message if unreadable.
    """
    print(f"[Extractor] Extracting text from {os.path.basename(pdf_path)}...")
    text = ""
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        # Loop through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        
        if not text.strip():
             print("[Extractor] Warning: No text found in PDF (might be an image-based PDF).")
             return "Error: No text found."
        
        print("[Extractor] Text extraction successful.")
        return text
    except Exception as e:
        print(f"[Extractor] Failed to extract text: {e}")
        return "Error: Could not read PDF."
