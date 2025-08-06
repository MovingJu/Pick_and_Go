
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
import numpy as np

class Image_comparison:
    
    @staticmethod
    def extract_features(image_url):

        def get_feature_extractor():
            model = models.resnet18(pretrained=True)
            feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
            feature_extractor.eval()
            return feature_extractor
        
        feature_extractor = get_feature_extractor()

        if not image_url:
            return None

        try:
            pil_image = Image.open(requests.get(image_url, stream=True, timeout=5).raw).convert("RGB") # pyright: ignore[reportArgumentType]
        except Exception as e:
            print(f"[Image Error] {image_url} → {e}")
            return None

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = preprocess(pil_image).unsqueeze(0) # type: ignore

        with torch.no_grad():
            features = feature_extractor(image_tensor)
            features = features.squeeze().numpy()
        return features

    @staticmethod
    def cosine_similarity(vec1, vec2):
        if vec1 is None or vec2 is None:
            print("cosine_similarity: One of the vectors is None")
            return -1
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
