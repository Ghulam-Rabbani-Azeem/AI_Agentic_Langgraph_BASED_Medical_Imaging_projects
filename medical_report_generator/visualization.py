def display_report_summary(report):
    print("\n📋 Report Summary")
    print("="*40)
    print(f"File: {report['metadata']['image_filename']}")
    print(f"Findings: {report['clinical_report']['findings'][:100]}...")
    print(f"AI Primary Findings: {', '.join(report['ai_analysis']['primary_findings'])}")
    print("Recommendations:")
    for r in report['summary']['recommendations']:
        print(f" - {r}")
