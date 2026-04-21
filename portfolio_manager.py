import json
import os
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ✅ CORRECT FUNCTION SIGNATURE: data: dict (not just  dict)
def save_report(report_name: str, report_type: str, org_type: str, data: dict):
    """Save report data and metadata as JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{report_name.replace(' ', '_').replace('/', '_')}.json"
    filepath = REPORTS_DIR / filename
    
    metadata = {
        "id": timestamp,
        "name": report_name,
        "type": report_type,
        "org_type": org_type,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": filename,
        "data": data  # ✅ Now 'data' is defined as a parameter
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return filepath

def load_all_reports():
    """Load all reports sorted by creation date (newest first)"""
    reports = []
    if not REPORTS_DIR.exists():
        return reports
        
    for file in sorted(REPORTS_DIR.glob("*.json"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                reports.append(json.load(f))
        except Exception:
            continue
    return reports

def get_report_data(filename: str):
    """Retrieve specific report data for download"""
    filepath = REPORTS_DIR / filename
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)