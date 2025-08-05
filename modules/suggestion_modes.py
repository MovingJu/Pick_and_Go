def Count_model(item, local_data):
    
    return

def Image_based_model(item, local_data):
    
    
    
    
    return


import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO
import numpy as np
class Image_comparison:
    

    @staticmethod
    def get_feature_extractor():
        model = models.resnet50(pretrained=True)
        feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        feature_extractor.eval()
        return feature_extractor

    @staticmethod
    def extract_features(image_url, feature_extractor):

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data).convert("RGB")

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
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

if __name__ == "__main__":

    import json

    
    features = Image_comparison.extract_features(
        "http://tong.visitkorea.or.kr/cms/resource/21/3497121_image3_1.jpg",
        Image_comparison.get_feature_extractor()
    )
    features1 = Image_comparison.extract_features(
        "http://tong.visitkorea.or.kr/cms/resource/88/3082988_image2_1.jpg",
        Image_comparison.get_feature_extractor()
    )

    print(
        Image_comparison.cosine_similarity(
            features, features1
        )
    )

    # print(
    #     json.dumps(
    #         features.tolist(),
    #         indent=3
    #     ),
    #     len(features)
    # )


