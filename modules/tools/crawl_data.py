import httpx

async def get_data():
    END_POINT = "http://apis.data.go.kr/B551011/KorService2"
    SERVICE_TYPE = "lclsSystmCode2"
    SERVICE_KEY = "n9U5t0ZqsIP9s2Cp%2FjQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4%2Fsi%2Ba8zxGLAnannZbWx1li1aV6EoJ0vg%3D%3D"
    NUM_OF_ROWS = 250

    url = f"{END_POINT}/{SERVICE_TYPE}?serviceKey={SERVICE_KEY}&numOfRows={NUM_OF_ROWS}&pageNo=1&MobileOS=ETC&MobileApp=App&_type=json&lclsSystmListYn=Y"
    
    result: list[tuple[str, str, str]] = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        
        PARENT_CODES: set[str] = set()
        for datas in data["response"]["body"]["items"]["item"]:
            PARENT_CODES.add(datas["lclsSystm2Cd"])
        print(PARENT_CODES)

        for PARENT_CODE in PARENT_CODES:
            for datas in data["response"]["body"]["items"]["item"]:
                if (datas["lclsSystm2Cd"] == PARENT_CODE):
                    code = datas["lclsSystm3Cd"]
                    name = datas["lclsSystm3Nm"]
                    print(code, name)
                    result.append((code, name, PARENT_CODE))
    except httpx.ConnectError as e:
        print("Connection Error:", e)
    
    return result