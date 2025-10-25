from fastapi import APIRouter
import httpx, random, asyncio, logging
import modules

router = APIRouter(
    prefix="/random",
    tags=["랜덤 사진 제공 엔드포인트임"]
)

NUM_OF_ROWS = 5
MAX_PAGE = 50540 // NUM_OF_ROWS
TARGET_COUNT = 15 // NUM_OF_ROWS

async def fetch_random_attraction():
    
    page = random.randint(1, MAX_PAGE)
    urls = modules.Url("areaBasedList2", numOfRows=NUM_OF_ROWS, pageNo=page, arrange="Q")
    tour = await modules.TourAPI.create(urls)
    data = await tour.fetch_url()
    
    return data


@router.get("/get_tourlist")
@modules.tools.timer
async def get_tour_test():
    results = []
    images = []
    registered = []

    while len(images) < 15:
        tasks = [fetch_random_attraction() for _ in range(3)]
        items: list[dict] = await asyncio.gather(*tasks)

        respond: list[dict] = []
        for i in items:
            respond += i["items"]

        respond = modules.Filter.tour_filter({"items" : respond}).get("items", {})

        print(f"length {len(respond)}")

        for elem in respond:
            if not elem.get("firstimage"):
                continue
            if elem["contentid"] in registered:
                continue
            results.append(elem)
            images.append(elem["firstimage"])
            if len(images) >= 15:
                break
                    
    # Main server에 랜덤 이미지 데이터 쏴주는 코드
    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        response = {
            "counts" : len(images), 
            "data": results, 
            "images": images
        }
        url_reciever = os.getenv("SEND_RANDOM_ENDPOINT") or ""


        # async with httpx.AsyncClient(cert=("./certifications/server.crt", "./certifications/server.key"), verify="./certifications/main_server.crt") as client:
        # async with httpx.AsyncClient(verify="./certifications/main_server1.crt") as client:
        async with httpx.AsyncClient(verify=False) as client:
            import json
            reciever_respond = await client.post(url_reciever, json=response)
        try:
            server_data = reciever_respond.json()
        except Exception:
            server_data = json.loads(reciever_respond.text)
    except Exception as e:
        logging.error("Error occured : ", e)
    
    logging.info(f"[200] : Send data to user.")
    return {
        "main_server_respond": server_data,
        "data": response
    }

