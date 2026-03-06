"""Paths and constants for the chatbot (Ireland–UK scope)."""
import os
from pathlib import Path

# Load .env from project root if present
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass

# Project root (parent of chatbot/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths (relative to project root)
EXCEL_PATH = PROJECT_ROOT / "Post-Brexit Sector Based Model - Completed runs.xlsx"
PARAMETER_CSV_PATH = PROJECT_ROOT / "parameter_names_from_completed_runs_updated.csv"

# Excel schema (Completed runs sheet)
COMPLETED_RUNS_SHEET = "Completed runs"
HEADER_ROW_EXCEL = 2   # 1-based: row 2 in Excel
INPUT_COL_END = 158   # columns 0..158 = input (through SecurityCheckCost)
OUTPUT_COL_START = 159
OUTPUT_COL_END = 332

# LLM
OPENAI_MODEL = os.environ.get("OPENAI_CHATBOT_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
