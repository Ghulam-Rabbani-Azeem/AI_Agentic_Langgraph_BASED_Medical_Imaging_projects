import os
from datetime import datetime
from . import preprocessing, model, analysis

def create_comprehensive_report(image_path, projections_df, reports_df):
    filename = os.path.basename(image_path)
    image_id = filename.split('_')[0]

    report_match = reports_df[reports_df['uid'] == image_id]

    findings, impression, comparison = "No report available", "", ""
    if not report_match.empty:
        report_row = report_match.iloc[0]
        raw_text = str(report_row.get("findings", "")) + " " + str(report_row.get("impression", ""))
        cleaned = preprocessing.clean_report_text(raw_text)
        findings = preprocessing.extract_section(cleaned, "FINDINGS")
        impression = preprocessing.extract_section(cleaned, "IMPRESSION")
        comparison = preprocessing.extract_section(cleaned, "COMPARISON")

    img_tensor = preprocessing.preprocess_image_correctly(image_path)
    m = model.load_model()
    ai_results = model.run_inference(m, img_tensor)

    agreement = analysis.analyze_agreement(findings, ai_results)
    recs = analysis.generate_recommendations(agreement)

    return {
        "metadata": {"analysis_date": datetime.now().isoformat(), "image_filename": filename},
        "clinical_report": {"findings": findings, "impression": impression, "comparison": comparison},
        "ai_analysis": {"primary_findings": [p for p, s in ai_results.items() if s > 0.5]},
        "comparative_analysis": agreement,
        "summary": {"recommendations": recs}
    }
