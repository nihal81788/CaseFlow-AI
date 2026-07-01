import requests
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

def analyze_document(text):
    """
    Sends the extracted text to local Ollama API for analysis.
    Forces the output to be a structured JSON object.
    """
    print(f"[Analyzer] Sending document to local Ollama ({MODEL_NAME}) for analysis...")
    
    if text.startswith("Error"):
        return get_default_response()

    prompt = f'''
You are an expert legal AI assistant. Your task is to analyze the following court document text and extract specific details.
You MUST respond with ONLY a valid JSON object. Do not include any markdown formatting, code blocks, or introductory text. Just the raw JSON.

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
{text[:4000]}  # limit text length just in case it's too long
'''

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json" # Ollama supports JSON format enforcement
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        # Parse response
        result_text = response.json().get("response", "")
        print("[Analyzer] Received response from Ollama.")
        
        # Try to parse the output as JSON
        try:
             # Sometimes the model still outputs markdown blocks, try to clean it
             cleaned_text = re.sub(r'```json\s*', '', result_text)
             cleaned_text = re.sub(r'```\s*', '', cleaned_text)
             parsed_json = json.loads(cleaned_text)
             return parsed_json
        except json.JSONDecodeError:
             print("[Analyzer] Error: Model output was not valid JSON.")
             return get_default_response()

    except Exception as e:
        print(f"[Analyzer] Failed to connect to Ollama: {e}")
        return get_default_response()

def get_default_response():
    """Returns a fallback dictionary if analysis fails."""
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
