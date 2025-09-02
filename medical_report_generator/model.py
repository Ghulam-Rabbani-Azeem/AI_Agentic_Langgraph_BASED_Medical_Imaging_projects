import torch
import torchxrayvision as xrv

def load_model():
    model = xrv.models.DenseNet(weights="densenet121-res224-chex")
    model.eval()
    return model

def run_inference(model, img_tensor):
    with torch.no_grad():
        output = model(img_tensor)
    pathologies = model.pathologies
    scores = output[0].detach().numpy()
    return {p: float(scores[i]) for i, p in enumerate(pathologies) if p and p.strip()}
