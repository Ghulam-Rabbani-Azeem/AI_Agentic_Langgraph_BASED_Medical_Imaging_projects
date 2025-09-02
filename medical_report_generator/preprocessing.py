import re
import numpy as np
import torch
import PIL.Image as Image
import torchxrayvision as xrv

def extract_section(text, section_name):
    if not text or text.strip() == '':
        return f"No {section_name} available"
    patterns = [
        rf'{section_name}[:]?(.*?)(?:\n\n|\n[A-Z]{{3,}}:|$)',
        rf'{section_name.upper()}[:]?(.*?)(?:\n\n|\n[A-Z]{{3,}}:|$)',
        rf'{section_name.lower()}[:]?(.*?)(?:\n\n|\n[A-Z]{{3,}}:|$)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            extracted = match.group(1).strip()
            if extracted and len(extracted) > 10:
                return extracted
    return f"No {section_name} section found"

def clean_report_text(text):
    if not text or text.strip() == '':
        return "No report available"
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\b\d{2,}[/-]\d{2,}[/-]\d{2,4}\b', '[DATE]', text)
    text = re.sub(r'\b[A-Z]{2,}\d+\b', '[ID]', text)
    return text.strip()

def preprocess_image_correctly(image_path):
    try:
        img = xrv.utils.load_image(image_path)
        img_tensor = torch.from_numpy(img).float().unsqueeze(0)
        if img_tensor.shape[2] != 224 or img_tensor.shape[3] != 224:
            img_tensor = torch.nn.functional.interpolate(
                img_tensor, size=(224, 224), mode='bilinear', align_corners=False
            )
        return (img_tensor - 0.5) / 0.5
    except Exception:
        img = Image.open(image_path).convert("L")
        img_array = np.array(img).astype(np.float32)
        img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min() + 1e-6)
        img_tensor = torch.from_numpy(img_array).float().unsqueeze(0).unsqueeze(0)
        img_tensor = torch.nn.functional.interpolate(img_tensor, size=(224, 224), mode='bilinear')
        return (img_tensor - 0.5) / 0.5
