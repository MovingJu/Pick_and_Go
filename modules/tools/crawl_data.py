import httpx, asyncio

async def get_data():
    END_POINT = "http://apis.data.go.kr/B551011/KorService2"
    SERVICE_TYPE = "categoryCode2"
    SERVICE_KEY = "n9U5t0ZqsIP9s2Cp%2FjQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4%2Fsi%2Ba8zxGLAnannZbWx1li1aV6EoJ0vg%3D%3D"
    NUM_OF_ROWS = 50

    url = f"{END_POINT}/{SERVICE_TYPE}?serviceKey={SERVICE_KEY}&numOfRows={NUM_OF_ROWS}&pageNo=1&MobileOS=ETC&MobileApp=AppTest&contentTypeId=12&_type=json"
    
    HERIT_CODE1 = "&cat1="
    HERIT_CODE2 = "&cat2="

    result: list[tuple[str, str, str]] = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        
        PARENT_CODES: list[str] = []
        for datas in data["response"]["body"]["items"]["item"]:
            PARENT_CODES.append(datas["code"])
        print(PARENT_CODES)

        print("-----------------")

        TARGET_CODES = []
        for PARENT_CODE in PARENT_CODES:
            async with httpx.AsyncClient() as client:
                response = await client.get(url + HERIT_CODE1 + PARENT_CODE)
                data = response.json()

            for datas in data["response"]["body"]["items"]["item"]:
                print(datas["code"])
                TARGET_CODES.append(datas["code"])
        
        print("--------------------")

        for PARENT_CODE in TARGET_CODES:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url + HERIT_CODE1 + PARENT_CODE[0:3] + HERIT_CODE2 + PARENT_CODE)
                data = response.json()

            for datas in data["response"]["body"]["items"]["item"]:
                code = datas["code"]
                name = datas["name"]
                print(code, name)
                result.append((code, name, PARENT_CODE))

    except httpx.ConnectError as e:
        print("Connection Error:", e)
    
    return result

