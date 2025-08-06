from fastapi import APIRouter, Request
from pydantic import BaseModel
import modules

router = APIRouter(
    tags=["Pick and Go main services"]
)

@router.get("/")
async def index():
    return {"To see descriptions" : "go to /docs"}


@router.post("/get_tour_list")
async def post_tour_list(item: modules.ServerData):
    """PageRank기반 복합 모델 작동중. 최적화 이슈 존재함."""
    from time import time
    st = time()
    Local_tour = await modules.Picked_sigungu.create(userid="-1")
    local_data = await Local_tour.get_related()

    suggested_data = await modules.Image_based_model(item, local_data)

    return {"elapsed time" : time() - st, "message" : suggested_data, "length" : len(suggested_data)} # type: ignore


if __name__ == "__main__":
    
    sample_data = \
{
  "user_info": {
    "user_name": "홍성학",
    "user_sex": 1,
    "user_age": 0
  },
  "interTour": {
    "count": 4,
    "list": [
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
    "list": [
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
    "lDongRegnCd": "28",
    "lDongSignguCd": "110",
    "numofPeople": "5"
  }
}