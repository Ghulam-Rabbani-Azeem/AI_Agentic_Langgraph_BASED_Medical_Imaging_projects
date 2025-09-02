from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil, os, pandas as pd, uuid
from medical_report_generator import config, report_generator

app = FastAPI(title="Medical Imaging Report Generator", version="1.0")

projections_df = pd.read_csv(config.PROJECTIONS_CSV).astype(str)
reports_df = pd.read_csv(config.REPORTS_CSV).astype(str)
UPLOAD_DIR = os.path.join(config.BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        report = report_generator.create_comprehensive_report(file_path, projections_df, reports_df)
        return JSONResponse(content=report)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
