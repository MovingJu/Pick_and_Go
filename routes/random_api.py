from fastapi import APIRouter
import httpx, random, asyncio
import modules

router = APIRouter(
    prefix="/random",
    tags=["랜덤 사진 제공 엔드포인트임"]
)

NUM_OF_ROWS = 5
MAX_PAGE = 50540 // NUM_OF_ROWS
TARGET_COUNT = 15 // NUM_OF_ROWS

async def fetch_random_attraction(client: httpx.AsyncClient):
    
    page = random.randint(1, MAX_PAGE)
    urls = modules.Url("areaBasedList2", numOfRows=NUM_OF_ROWS, pageNo=page, arrange="Q")
    tour = await modules.TourAPI.create(urls)
    data = await tour.fetch_url()
    
    return data

@router.get("/get_tourlist")
async def get_tour_test():
    results = []
    images = []

    async with httpx.AsyncClient() as client:
        while len(images) < 15:
            tasks = [fetch_random_attraction(client) for _ in range(3)]  # 한번에 3페이지씩만 요청
            items = await asyncio.gather(*tasks)

            for i in items:
                for item in i["items"]:  # type: ignore
                    img = item.get("firstimage")
                    if img and img not in images:
                        results.append(item)
                        images.append(img)
                        results: list = modules.Filter.tour_filter({"items" : results})["items"]
                        if len(images) >= 15:
                            break
                if len(images) >= 15:
                    break
                    

    

    # Main server에 랜덤 이미지 데이터 쏴주는 코드
    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        response = {"counts" : len(images), "items": results, "images": images}
        load_dotenv()
        url_reciever = os.getenv("SEND_RANDOM_ENDPOINT") or ""
        async with httpx.AsyncClient() as client:
            reciever_respond = await client.post(url_reciever, json=response)
        import json
        try:
            server_data = reciever_respond.json()
        except Exception:
            server_data = json.loads(reciever_respond.text)
    except:
        pass
    

    return {
        "main_server_respond": server_data,
        "data": response
    }