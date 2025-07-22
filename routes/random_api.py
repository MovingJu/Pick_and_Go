from fastapi import APIRouter
import httpx, random, asyncio

router = APIRouter(
    prefix="/random",
    tags=["랜덤 사진 제공 엔드포인트임"]
)

TOUR_API_SERVICE_KEY = "n9U5t0ZqsIP9s2Cp/jQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4/si+a8zxGLAnannZbWx1li1aV6EoJ0vg=="
TOUR_API_BASE_URL = "http://apis.data.go.kr/B551011/KorService2/areaBasedList2"
MOBILE_OS = "AND"
MOBILE_APP = "PIGO"
NUM_OF_ROWS = 4
MAX_PAGE = 12642
TARGET_COUNT = 15


async def fetch_random_attraction(client: httpx.AsyncClient) -> dict | None:
    page = random.randint(1, MAX_PAGE)

    params = {
        "serviceKey": TOUR_API_SERVICE_KEY,
        "numOfRows": NUM_OF_ROWS,
        "pageNo": page,
        "MobileOS": MOBILE_OS,
        "MobileApp": MOBILE_APP,
        "_type": "json",
        "arrange": "C",
    }

    try:
        response = await client.get(TOUR_API_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        if not items:
            return None

        random_item = random.choice(items)
        if random_item.get("firstimage"):
            return random_item

    except Exception as e:
        print(f"Error: {e}")
        return None

@router.get("/get_tour_attractions")
async def get_tour_attractions():
    results = []
    images = []

    async with httpx.AsyncClient() as client:
        while len(results) < TARGET_COUNT:
            tasks = [fetch_random_attraction(client) for _ in range(TARGET_COUNT)]
            items = await asyncio.gather(*tasks)

            for item in items:
                if item and item["firstimage"] not in images:
                    results.append(item)
                    images.append(item["firstimage"])
                    if len(results) == TARGET_COUNT:
                        break

    return {"data": results, "images": images}