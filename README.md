# CaseFlow AI ⚖️🤖

CaseFlow AI is a robust, fully offline automation project designed as a core feature for the **CaseWatch** civic-tech platform. It serves to help citizens automatically organize court documents, understand legal language, and keep track of hearings, all running safely and securely on your local hardware.

With 50.6 million pending court cases in India, CaseFlow AI is built to drastically simplify document management by automating the extraction, analysis, and organization of legal PDFs like Court Notices, FIRs, and Bail Orders using local AI.

## Key Features
* **Fully Offline AI Processing**: Uses the `llama3.2:3b` model running locally via Ollama, ensuring legal documents never leave your machine.
* **Automated Document Watcher**: Simply drop legal PDFs into the `inbox/` folder, and the app automatically picks them up, reads them, and moves them to organized subfolders.
* **Smart Data Extraction**: Parses complex legal texts into structured data (Case Number, Court Name, Judge, Hearing Date, Required Documents, Next Actions, and a summary).
* **Excel & SQLite Syncing**: Automatically saves processed data to a local SQLite database for CaseWatch backend integration, and appends the extracted data to an easy-to-read Excel file (`data/extracted_data.xlsx`).
* **Background Scheduler**: 
  * Checks for upcoming hearings daily at 8:00 AM.
  * Generates a comprehensive text summary report of all documents processed today at 8:00 PM.

## Architecture
- `main.py`: Entry point that ensures folders exist and starts the background jobs.
- `watcher.py`: Uses `watchdog` to monitor the `inbox/` folder for new PDFs.
- `extractor.py`: Uses `PyMuPDF` to extract text from the PDF.
- `analyzer.py`: Sends the text to the local Ollama API to enforce structured JSON output.
- `database.py` & `excel_export.py`: Handles saving the structured data into SQLite and Excel.
- `organizer.py`: Renames the PDF and moves it to the correct `organized/` subfolder based on the document type.
- `scheduler.py`: Uses `APScheduler` to run the 8:00 AM hearing checks and 8:00 PM reporting jobs.

## How to Run This Project

### Prerequisites
1. **Python 3.10+** installed on your system.
2. **Ollama** installed on your system with the `llama3.2:3b` model downloaded.

### Step-by-Step Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nihal81788/CaseFlow-AI.git
   cd CaseFlow-AI
   ```

2. **Start Ollama:**
   Ensure Ollama is running the AI model in the background:
   ```bash
   ollama run llama3.2:3b
   ```

3. **Install Dependencies:**
   Create a virtual environment and install the required Python packages:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python main.py
   ```

5. **Test the Automation:**
   Once running, you will notice an `inbox/` directory gets created. Just drop a PDF document inside that folder and watch the terminal logs as CaseFlow AI automatically processes and organizes it!
