Medical Imaging Report Generator (Agentic Pipeline)

Input: Medical image (X-ray, MRI, CT scan).

Agents:

Image Analysis Agent (uses a vision model like CLIP, SAM, or a fine-tuned ViT to detect abnormalities).

Report Drafting Agent (converts findings into a natural language medical report using LangGraph).

Consistency Checker Agent (verifies alignment between detected abnormalities and report text).

Output: Radiology-style structured report.
