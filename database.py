import sqlite3
from datetime import date

DB_PATH = 'caseflow.db'

def init_db():
    """Initializes the database and creates the cases table if it doesn't exist."""
    print("[Database] Initializing database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            case_number TEXT,
            court_name TEXT,
            judge TEXT,
            hearing_date TEXT,
            document_type TEXT,
            required_documents TEXT,
            next_action TEXT,
            summary TEXT,
            created_at DATE DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()
    print("[Database] Database initialized successfully.")

def save_case(data, filename):
    """Saves a parsed case into the database."""
    print(f"[Database] Saving case details for {filename}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO cases (
            filename, case_number, court_name, judge, hearing_date,
            document_type, required_documents, next_action, summary, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        data.get("case_number"),
        data.get("court_name"),
        data.get("judge"),
        data.get("hearing_date"),
        data.get("document_type"),
        data.get("required_documents"),
        data.get("next_action"),
        data.get("summary"),
        date.today().isoformat()
    ))
    conn.commit()
    conn.close()
    print(f"[Database] Saved {filename} to database.")

def get_todays_hearings():
    """Retrieves cases that have a hearing date matching today."""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT case_number, court_name, next_action FROM cases WHERE hearing_date = ?', (today,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_cases_today():
    """Retrieves all cases added today for the evening report."""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT case_number, document_type, next_action, summary FROM cases WHERE created_at = ?', (today,))
    results = cursor.fetchall()
    conn.close()
    return results
