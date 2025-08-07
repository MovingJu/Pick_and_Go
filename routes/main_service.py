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
    PageRank기반 복합 모델 작동중. 추후 자체 제작 모델로 교체 예정.
    
    작동 방식은 [링크](https://movingju06.com/research/2025/08/04/research-_pigo_backend) 참고.    
    """
    from time import time
    st = time()
    
    item.etcData.location = preprocess_server_data(item) # type: ignore

    tool = modules.Picked_sigungu(item.etcData.location)
    local_data = await tool.get_related()

    suggested_data = await modules.Image_based_model(item, local_data)

    return {"elapsed_time" : time() - st, "message" : suggested_data, "length" : len(suggested_data)} # type: ignore


if __name__ == "__main__":
    
    sample_data = \
{
  "user_info": {
    "user_id": 4369726722,
    "user_name": "홍성학",
    "user_sex": 1,
    "user_age": 0
    },
  "interTour": {
    "count": 4,
    "items": [
      {
        "contentid": "1594500",
        "contenttypeid": "12",
        "addr1": "전북특별자치도 전주시 완산구 전주천동로 46",
        "title": "전주목판서화체험관",
        "mapx": 127.1556500663,
        "mapy": 35.8115147404,
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image3_1.jpg",
        "lDongRegnCd": "52",
        "lDongSignguCd": "111",
        "lclsSystm1": "EX",
        "lclsSystm2": "EX01",
        "lclsSystm3": "EX010100"
      },
      {
        "contentid": "2469437",
        "contenttypeid": "12",
        "addr1": "전라남도 순천시 상사면 상사호길 555",
        "title": "주암댐 물 문화관",
        "mapx": 127.4143799419,
        "mapy": 34.9493972551,
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
        "lDongRegnCd": "46",
        "lDongSignguCd": "150",
        "lclsSystm1": "EX",
        "lclsSystm2": "EX06",
        "lclsSystm3": "EX061000"
      },
      {
        "contentid": "2643070",
        "contenttypeid": "39",
        "addr1": "서울특별시 중구 명동8가길 52",
        "title": "씨태번",
        "mapx": 126.9879897343,
        "mapy": 37.5618132993,
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
        "lDongRegnCd": "11",
        "lDongSignguCd": "140",
        "lclsSystm1": "FD",
        "lclsSystm2": "FD02",
        "lclsSystm3": "FD020300"
      },
      {
        "contentid": "2670494",
        "contenttypeid": "39",
        "addr1": "전라남도 순천시 비봉길 73",
        "title": "큰집한우촌",
        "mapx": 127.520486865,
        "mapy": 34.9660361015,
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
        "lDongRegnCd": "46",
        "lDongSignguCd": "150",
        "lclsSystm1": "FD",
        "lclsSystm2": "FD01",
        "lclsSystm3": "FD010100"
      }
    ]
  },
  "visitedTour": {
    "count": 1,
    "items": [
      {
        "contentid": "1957444",
        "contenttypeid": "12",
        "addr1": "전라남도 순천시 공마당1길 64",
        "title": "용강서원(순천)",
        "mapx": 127.4761854654,
        "mapy": 34.9556198416,
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image2_1.JPG",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image3_1.JPG",
        "lDongRegnCd": "46",
        "lDongSignguCd": "150",
        "lclsSystm1": "HS",
        "lclsSystm2": "HS01",
        "lclsSystm3": "HS010900"
      }
    ]
  },
  "etcData": {
    "location": [
      "전라남도 순천",
      "서울시 송파구"
    ],
    "numofPeople": 4
  }
}