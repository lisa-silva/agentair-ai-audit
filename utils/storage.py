import json
import os
from datetime import datetime
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_audit(business_name, url, score, recommendations):
    """Save audit results to a JSON file."""
    timestamp = datetime.now().isoformat()
    
    # Create a safe filename from business name
    safe_name = "".join(c for c in business_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_').lower()
    filename = f"{safe_name}_{timestamp[:10]}.json"
    filepath = DATA_DIR / filename
    
    audit_data = {
        "business_name": business_name,
        "url": url,
        "score": score,
        "recommendations": recommendations,
        "timestamp": timestamp,
        "id": filename
    }
    
    with open(filepath, 'w') as f:
        json.dump(audit_data, f, indent=2)
    
    return str(filepath)

def load_all_audits():
    """Load all saved audits."""
    audits = []
    if DATA_DIR.exists():
        for filepath in DATA_DIR.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    audit = json.load(f)
                    audits.append(audit)
            except:
                continue
    
    # Sort by timestamp, newest first
    audits.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return audits

def get_audit_by_id(audit_id):
    """Load a specific audit by ID."""
    filepath = DATA_DIR / audit_id
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return None
