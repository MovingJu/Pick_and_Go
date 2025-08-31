from PIL import Image
from io import BytesIO
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import httpx, requests, os, asyncio

import modules



# 시스템 쓰레드 수 기반으로 동시 요청 수 계산
MAX_CONCURRENT_REQUESTS = (os.cpu_count() or 4) * 2  # fallback to 4 if None

async def fetch_image(image_url: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore):

    def get_feature_extractor():
            model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
            feature_extractor.eval()
            return feature_extractor
    
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
            features = get_feature_extractor()(image_tensor)
            features = features.squeeze().numpy()
        return features

@modules.tools.timer
async def Async():
    Local_tour = await modules.Picked_sigungu.create(userid="-1")
    local_data = await Local_tour.get_related()

    # 이미지 URL 필터링: 빈 값 제거 + 중복 제거
    image_urls = list({
        elem["firstimage"]
        for elem in local_data["items"]
        if elem.get("firstimage")
    })

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_image(url, client, semaphore) for url in image_urls]
        results = await asyncio.gather(*tasks)

    print(len([img for img in results if img is not None]))

    return 



@modules.tools.timer
async def sync():

    Local_tour = await modules.Picked_sigungu.create(userid="-1")
    local_data = await Local_tour.get_related()

    image_url = []
    for elem in local_data["items"]:
        image_url.append(elem["firstimage"]) # type: ignore

    pil_image = []
    for i in image_url:
        if not i:
            continue
        # try:
        pil_image.append(Image.open(requests.get(i, stream=True).raw).convert("RGB")) # pyright: ignore[reportArgumentType]
        # except Exception as e:
        #     print(f"[Image Error] {i} -> {e}")
        #     continue
    print(len(pil_image))

    return pil_image



if __name__ == "__main__":
    asyncio.run(Async())