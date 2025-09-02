import os, json
import pandas as pd
from medical_report_generator import config, report_generator, visualization

def main():
    projections_df = pd.read_csv(config.PROJECTIONS_CSV).astype(str)
    reports_df = pd.read_csv(config.REPORTS_CSV).astype(str)

    image_files = [f for f in os.listdir(config.IMAGE_DIR) if f.endswith(".png")][:3]
    all_reports = []

    for img in image_files:
        path = os.path.join(config.IMAGE_DIR, img)
        report = report_generator.create_comprehensive_report(path, projections_df, reports_df)
        visualization.display_report_summary(report)
        all_reports.append(report)

    with open(config.OUTPUT_FILE, "w") as f:
        json.dump(all_reports, f, indent=2)
    print(f"\n✅ Reports saved to {config.OUTPUT_FILE}")

if __name__ == "__main__":
    main()
