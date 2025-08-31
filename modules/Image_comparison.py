from PIL import Image
from io import BytesIO
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import httpx, requests, os, asyncio, numpy as np

import modules

# 시스템 쓰레드 수 기반으로 동시 요청 수 계산
MAX_CONCURRENT_REQUESTS = (os.cpu_count() or 4) * 2  # fallback to 4 if None

class Image_comparison:

    def __init__(self) -> None:
        self.feature_extractor = Image_comparison.get_feature_extractor()
        self.output_dim: int = 512

    @staticmethod
    def get_feature_extractor():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        feature_extractor.to(device)
        feature_extractor.eval()
        return feature_extractor
    
    async def fetch_image(self, image_url: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore):

        if image_url == "":
            return np.zeros(self.output_dim)
        
        async with semaphore:
            response = await client.get(image_url)

            pil_image = Image.open(BytesIO(response.content)).convert("RGB")

            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            image_tensor = preprocess(pil_image).unsqueeze(0) # type: ignore

            with torch.no_grad():
                features = self.feature_extractor(image_tensor)
                features = features.squeeze().numpy()
            return features

    @modules.tools.timer
    async def extract_features_list(self, item: list[str]):

        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_image(url, client, semaphore) for url in item]
            results = await asyncio.gather(*tasks)

        return results


    @staticmethod
    def cosine_similarity(vec1, vec2):
        if vec1 is None or vec2 is None:
            print("cosine_similarity: One of the vectors is None")
            return -1
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
