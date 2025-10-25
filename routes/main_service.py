from fastapi import APIRouter
import re, httpx, pandas as pd, numpy as np
import logging

import modules

router = APIRouter(
    tags=["Pick and Go main services"]
)

@router.get("/")
async def index():
    return {"To see descriptions" : "go to /docs"}

def preprocess_server_data(item: modules.ServerData | modules.CalendarData):
    if type(item.etcData) == modules.schema.Modified_EtcData:
        return item.etcData.location
    
    result: list[tuple[int, int]] = []
    table_sido = pd.read_csv("./data/sido.csv")
    table_sigungu = pd.read_csv("./data/sigungu.csv")
    for elem in item.etcData.location: # type: ignore
        elem = str(elem) # str임을 보장하기 위함 (타입 힌트)
        sido = elem[0:3] # 3자리면 시도 코드 파악 가능
        sigungu = elem[elem.find(' ')+1:]
        
        sido_index = -1
        for i in range(2):  # 박치기공룡이 이름 이상하게 줘도 가능하도록 예외처리
            sido_series = table_sido["city_id"][table_sido["city_name"].str.contains(re.escape(sido))]
            if sido_series.empty: 
                sido = sido[0:3 - i - 1]
                continue
            sido_index: int = sido_series.values[0]

        sigungu_index = -1
        sigungu_series = table_sigungu[table_sigungu["parent_city_id"] == sido_index]
        sigungu_item: pd.Series = sigungu_series["city_id"][sigungu_series["city_name"].str.contains(re.escape(sigungu))]
        if sigungu_item.empty:
            continue
        sigungu_index: int = sigungu_item.values[0]

        result.append((int(sido_index), int(sigungu_index)))
    return result



@router.post("/get_tour_list")
async def post_tour_list(item: modules.ServerData | modules.schema.CalendarData, top_n: int = 5) -> dict:
    """
    "관광지"만 추천하는 엔드포인트. 

    PageRank기반 복합 모델 작동중. 추후 자체 제작 모델로 교체 예정.
    
    작동 방식은 [링크](https://movingju06.com/research/2025/08/04/research-_pigo_backend) 참고.    
    """
    from time import time
    st = time()
    
    locations = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(locations)
    local_data = await tool.get_related()

    filtered_local_data = modules.Filter.tour_filter(local_data)

    # 방문 관광지 걸러내는 부분
    if item.visitedTour != None:
        local_data_np = np.array(filtered_local_data["items"])
        local_data_ids = np.array([int(item["contentid"]) for item in local_data_np])
        visited_ids = np.array([int(item.contentid) for item in item.visitedTour.items]) # type: ignore

        diff_ids = np.setdiff1d(local_data_ids, visited_ids)
        print(f"length : {diff_ids}")

        # 다시 필터링된 dict 리스트로 복원
        filtered_local_data["items"] = [item for item in local_data_np if int(item["contentid"]) in diff_ids]
    

    try:
        suggested_data = await modules.Image_based_model(item, filtered_local_data)
    except Exception as e:
        logging.error("Some error occured while running Image based model.")
        return {"message" : "관광지 없음"}
    

    # db에 캐싱해놓는 코드
    df = pd.read_csv("./data/user_tours.csv", encoding="utf-8")

    # 이 부분을 전혀 이해할 수 없음. 이 부분이 없다면 바로 아래의 json.dumps에서 json을 전혀 인식하지 못함. 파이썬 임포트의 난해함은 그 궤가 다르다..
    import json 
    new_data = {
        "user_id" : item.user_info.user_id,
        "tours" : json.dumps(suggested_data, ensure_ascii=False)
    }
    if new_data["user_id"] in df["user_id"].values:
        df.loc[df["user_id"] == new_data["user_id"], "tours"] = new_data["tours"]
    else:
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    df.to_csv("./data/user_tours.csv", index=False, encoding="utf-8-sig")


    # Main server에 랜덤 이미지 데이터 쏴주는 코드
    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        response = {"data": suggested_data[:top_n]}
        load_dotenv()
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
        logging.warning("Cannot communicate with main server. Please check if server alive.")

    logging.info(f"[200] : Send data to {item.user_info.user_id}")

    return {
            "elapsed_time" : time() - st, 
            "data" : suggested_data[:top_n], 
            "length" : len(suggested_data),
            "server data" : server_data
        } # type: ignore



@router.post("/get_food_list")
async def post_food_list(item: modules.ServerData | modules.schema.CalendarData, top_n: int = 5):
    """
    음식점 관련 관광지만 추천하는 엔드포인트.   
    """
    from time import time
    st = time()
    
    locations = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(locations)
    local_data = await tool.get_related()
    
    filtered_local_data = modules.Filter.food_filter(local_data)

    # 방문 관광지 걸러내는 부분
    if item.visitedTour != None:
        local_data_np = np.array(filtered_local_data["items"])
        local_data_ids = np.array([int(item["contentid"]) for item in local_data_np])
        visited_ids = np.array([int(item.contentid) for item in item.visitedTour.items]) # type: ignore

        diff_ids = np.setdiff1d(local_data_ids, visited_ids)
        print(f"length : {diff_ids}")

        # 다시 필터링된 dict 리스트로 복원
        filtered_local_data["items"] = [item for item in local_data_np if int(item["contentid"]) in diff_ids]

    try:
        suggested_data = await modules.Image_based_model(item, filtered_local_data)
    except Exception as e:
        logging.error("Some error occured while running Image based model.")
        return {"message" : "관광지 없음", "data": []}
    

    # Main server에 랜덤 이미지 데이터 쏴주는 코드
    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        response = {"data": suggested_data[:top_n]}
        load_dotenv()
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
        logging.warning("Cannot communicate with main server. Please check if server alive.")

    logging.info(f"[200] : Send data to {item.user_info.user_id}")

    return {
            "elapsed_time" : time() - st, 
            "data" : suggested_data[:top_n], 
            "length" : len(suggested_data),
            "server data" : server_data
        } 



@router.post("/get_hotel_list")
async def post_hotel_list(item: modules.ServerData | modules.schema.CalendarData, top_n: int = 5):
    """
    숙소 관련 관광지만 추천하는 엔드포인트.   
    """
    from time import time
    st = time()
    
    locations = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(locations)
    local_data = await tool.get_related()
    
    filtered_local_data = modules.Filter.hotel_filter(local_data)

    # 방문 관광지 걸러내는 부분
    if item.visitedTour != None:
        local_data_np = np.array(filtered_local_data["items"])
        local_data_ids = np.array([int(item["contentid"]) for item in local_data_np])
        visited_ids = np.array([int(item.contentid) for item in item.visitedTour.items]) # type: ignore

        diff_ids = np.setdiff1d(local_data_ids, visited_ids)
        print(f"length : {diff_ids}")

        # 다시 필터링된 dict 리스트로 복원
        filtered_local_data["items"] = [item for item in local_data_np if int(item["contentid"]) in diff_ids]

    try:
        suggested_data = await modules.Image_based_model(item, filtered_local_data)
    except Exception as e:
        logging.error("Some error occured while running Image based model.")
        return {"message" : "관광지 없음"}
    
    # df = pd.read_csv("./data/user_hotels.csv", encoding="utf-8")
    # new_data = {
    #     "user_id" : item.user_info.user_id,
    #     "hotels" : json.dumps(suggested_data, ensure_ascii=False)
    # }
    # if new_data["user_id"] in df["user_id"].values:
    #     df.loc[df["user_id"] == new_data["user_id"], "hotels"] = new_data["hotels"]
    # else:
    #     df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    # df.to_csv("./data/user_hotels.csv", index=False, encoding="utf-8-sig")


    # Main server에 랜덤 이미지 데이터 쏴주는 코드
    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        response = {"data": suggested_data[:top_n]}
        load_dotenv()
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
        logging.warning("Cannot communicate with main server. Please check if server alive.")

    logging.info(f"[200] : Send data to {item.user_info.user_id}")

    return {
            "elapsed_time" : time() - st, 
            "data" : suggested_data[:top_n], 
            "length" : len(suggested_data),
            "server data" : server_data
        } # type: ignore

