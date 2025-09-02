def analyze_agreement(clinical_text, ai_predictions):
    agreement = {
        "strong_agreement": [], "partial_agreement": [],
        "disagreement": [], "ai_only_findings": [], "clinical_only_findings": []
    }
    common_findings = {
        'Atelectasis': ['atelectasis', 'collapse'],
        'Consolidation': ['consolidation', 'pneumonia'],
        'Effusion': ['effusion', 'pleural fluid'],
        'Cardiomegaly': ['cardiomegaly', 'enlarged heart'],
        'Nodule': ['nodule', 'mass', 'lesion']
    }
    text_lower = clinical_text.lower()
    for condition, keywords in common_findings.items():
        ai_score = ai_predictions.get(condition, 0)
        clinical_mention = any(k in text_lower for k in keywords)
        if clinical_mention and ai_score > 0.5:
            agreement["strong_agreement"].append(condition)
        elif clinical_mention and ai_score > 0.3:
            agreement["partial_agreement"].append(condition)
        elif not clinical_mention and ai_score > 0.5:
            agreement["ai_only_findings"].append(condition)
        elif clinical_mention and ai_score <= 0.3:
            agreement["clinical_only_findings"].append(condition)
    return agreement

def generate_recommendations(agreement):
    recs = []
    if agreement["ai_only_findings"]:
        recs.append("Review AI-only findings: " + ", ".join(agreement["ai_only_findings"]))
    if agreement["clinical_only_findings"]:
        recs.append("Verify clinical-only findings: " + ", ".join(agreement["clinical_only_findings"]))
    if agreement["strong_agreement"]:
        recs.append("Strong agreement on: " + ", ".join(agreement["strong_agreement"]))
    return recs or ["AI findings appear consistent with clinical report findings"]
