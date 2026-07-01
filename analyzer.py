import requests
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

def analyze_document(text, retry=False):
    print(f"[Analyzer] Sending document to local Ollama ({MODEL_NAME}) for analysis...")
    
    if text.startswith("Error"):
        return get_default_response()

    VALID_DOC_TYPES = ["Court Notice", "FIR", "Bail Order", "Affidavit", "Agreement", "Other"]
    
    base_prompt = f'''
You are an expert legal AI assistant. Your task is to analyze the following court document text and extract specific details.
You MUST respond with ONLY a valid JSON object. Do not include any markdown formatting, code blocks, or introductory text. Just the raw JSON.

CRITICAL RULES:
1. For "document_type", you MUST pick exactly ONE of these exact strings: "Court Notice", "FIR", "Bail Order", "Affidavit", "Agreement", or "Other". Do not return a list or combination.
2. For "case_number", look for common Indian case number patterns such as "Case No.", "SLP(C) No.", "Crl.A. No.", "W.P. No.", "CNR", etc. Extract it exactly as written. If there is truly no case number, return null. Do NOT return "UnknownCase".

Example Correct JSON Response:
{{
  "document_type": "Court Notice",
  "case_number": "SLP(C) No. 1234 of 2023",
  "court_name": "Supreme Court of India",
  "judge": "Hon'ble Mr. Justice A.B. Smith",
  "hearing_date": "2023-10-15",
  "required_documents": "Vakalatnama, Counter Affidavit",
  "next_action": "File counter affidavit before the next hearing",
  "summary": "This is a notice regarding a special leave petition filed against the high court order."
}}

The JSON MUST have exactly these fields:
{{
  "document_type": "Court Notice / FIR / Bail Order / Affidavit / Agreement / Other",
  "case_number": "extracted string or null",
  "court_name": "extracted string or null",
  "judge": "extracted string or null",
  "hearing_date": "YYYY-MM-DD format or null",
  "required_documents": "comma separated string or null",
  "next_action": "plain language string of what the user needs to do next",
  "summary": "2-3 sentence plain language summary of the document"
}}

Here is the document text:
{text}
'''

    prompt = base_prompt
    if retry:
        prompt += "\n\nCRITICAL REMINDER: Your previous response was invalid. You MUST ensure 'document_type' is exactly ONE of: Court Notice, FIR, Bail Order, Affidavit, Agreement, Other. Do NOT return multiple types."

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result_text = response.json().get("response", "")
        print("[Analyzer] Received response from Ollama.")
        
        try:
             cleaned_text = re.sub(r'<think>.*?</think>\s*', '', result_text, flags=re.DOTALL)
             cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
             cleaned_text = re.sub(r'```\s*', '', cleaned_text)
             parsed_json = json.loads(cleaned_text)
             
             doc_type = parsed_json.get("document_type")
             if doc_type not in VALID_DOC_TYPES:
                 if not retry:
                     print(f"[Analyzer] Invalid document_type returned: {doc_type} — retrying...")
                     return analyze_document(text, retry=True)
                 else:
                     print(f"[Analyzer] Invalid document_type returned again: {doc_type} — falling back to 'Other'.")
                     parsed_json["document_type"] = "Other"
                     
             if parsed_json.get("case_number") == "UnknownCase":
                 parsed_json["case_number"] = None
                 
             return parsed_json
             
        except json.JSONDecodeError:
             if not retry:
                 print("[Analyzer] Error: Model output was not valid JSON — retrying...")
                 return analyze_document(text, retry=True)
             else:
                 print("[Analyzer] Error: Model output was not valid JSON after retry.")
                 return get_default_response()

    except Exception as e:
        print(f"[Analyzer] Failed to connect to Ollama: {e}")
        return get_default_response()

def get_default_response():
    return {
        "document_type": "Other",
        "case_number": "Manual review needed",
        "court_name": "Manual review needed",
        "judge": "Manual review needed",
        "hearing_date": "Manual review needed",
        "required_documents": "Manual review needed",
        "next_action": "Manual review needed",
        "summary": "Manual review needed due to analysis failure."
    }
