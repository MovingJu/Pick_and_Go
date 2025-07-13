import httpx
import asyncio

async def fetch():
    url = "http://apis.data.go.kr/B551011/KorService2/areaCode2?serviceKey=n9U5t0ZqsIP9s2Cp%2FjQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4%2Fsi%2Ba8zxGLAnannZbWx1li1aV6EoJ0vg%3D%3D&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        for i in data["response"]["body"]["items"]["item"]:
            print(i["code"], i["name"]) 
    except httpx.ConnectError as e:
        print(e)

asyncio.run(fetch())