from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

RESUME_FOLDER = BASE_DIR / "data" / "resumes"
JD_FOLDER = BASE_DIR / "data" / "job_descriptions"
VECTOR_DB_PATH = BASE_DIR / "vector_db"
REPORT_FOLDER = BASE_DIR / "reports"