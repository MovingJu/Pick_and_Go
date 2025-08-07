from fastapi import APIRouter
import pandas as pd

import modules

router = APIRouter(
    tags=["Pick and Go main services"]
)

@router.get("/")
async def index():
    return {"To see descriptions" : "go to /docs"}

def preprocess_server_data(item: modules.ServerData):
    result: list[tuple[int, int]] = []
    table_sido = pd.read_csv("./data/sido.csv")
    table_sigungu = pd.read_csv("./data/sigungu.csv")
    for elem in item.etcData.location:
        elem = str(elem) # str임을 보장하기 위함 (타입 힌트)
        sido = elem[0:3] # 3자리면 시도 코드 파악 가능
        sigungu = elem[elem.find(' ')+1:]
        
        sido_index = -1
        for i in range(2):  # 박치기공룡이 이름 이상하게 줘도 가능하도록 예외처리
            sido_series = table_sido["city_id"][table_sido["city_name"].str.contains(sido)]
            if sido_series.empty: 
                sido = sido[0:3 - i - 1]
                continue
            sido_index: int = sido_series.values[0]

        sigungu_index = -1
        sigungu_series = table_sigungu[table_sigungu["parent_city_id"] == sido_index]
        sigungu_item: pd.Series = sigungu_series["city_id"][sigungu_series["city_name"].str.contains(sigungu)]
        if sigungu_item.empty:
            continue
        sigungu_index: int = sigungu_item.values[0]

        result.append((int(sido_index), int(sigungu_index)))
    return result

@router.post("/get_tour_list")
async def post_tour_list(item: modules.ServerData):
    """
    "관광지"만 추천하는 엔드포인트. 

    PageRank기반 복합 모델 작동중. 추후 자체 제작 모델로 교체 예정.
    
    작동 방식은 [링크](https://movingju06.com/research/2025/08/04/research-_pigo_backend) 참고.    
    """
    from time import time
    st = time()
    
    item.etcData.location = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(item.etcData.location)
    local_data = await tool.get_related()
    
    filtered_local_data = modules.Filter.tour_filter(local_data)

    try:
        suggested_data = await modules.Image_based_model(item, filtered_local_data)
    except:
        return {"message" : "관광지 없음"}

    return {"elapsed_time" : time() - st, "message" : suggested_data, "length" : len(suggested_data)} # type: ignore

@router.post("/get_food_list")
async def post_food_list(item: modules.ServerData):
    """
    음식점 관련 관광지만 추천하는 엔드포인트.   
    """
    from time import time
    st = time()
    
    item.etcData.location = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(item.etcData.location)
    local_data = await tool.get_related()
    
    filtered_local_data = modules.Filter.food_filter(local_data)

    try:
        suggested_data = await modules.Image_based_model(item, filtered_local_data)
    except:
        return {"message" : "관광지 없음"}

    return {"elapsed_time" : time() - st, "message" : suggested_data, "length" : len(suggested_data)} # type: ignore

