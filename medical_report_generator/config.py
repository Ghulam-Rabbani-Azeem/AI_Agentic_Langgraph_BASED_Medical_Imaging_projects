import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
PROJECTIONS_CSV = os.path.join(DATA_DIR, "indiana_projections.csv")
REPORTS_CSV = os.path.join(DATA_DIR, "indiana_reports.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "structured_chest_xray_reports.json")
MODEL_NAME = "densenet121-res224-chex"
