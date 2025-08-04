from fastapi import APIRouter, Request
from pydantic import BaseModel
import modules

router = APIRouter(
    tags=["Pick and Go main services"]
)

@router.get("/")
async def index():
    return {"To see descriptions" : "go to /docs"}


class Inter_tour(BaseModel):
    user_id: str
    total_count: int
    tours: list[dict[str, str]]
@router.post("/get_tour_list")
async def post_tour_list(item: Inter_tour):
    """Still testing. DO NOT USE THIS."""
    
    Local_tour = await modules.Picked_sigungu.create(userid=item.user_id)

    return


if __name__ == "__main__":
    
    inter_tour = {
        "user_id" : 1,
        "total_count" : 2,
        "tours" : [
            {
                "addr1": "서울특별시 중구 세종대로11길 35",
                "contentid": "232229",
                "mapx": "126.9739382319",
                "mapy": "37.5619935812",
                "title": "강서면옥",
                "lDongRegnCd": "11",
                "lDongSignguCd": "140",
                "lclsSystm1": "FD",
                "lclsSystm2": "FD01",
                "lclsSystm3": "FD010100"
            },
            {
                "addr1": "서울특별시 중구 서소문로11길 1",
                "contentid": "133854",
                "mapx": "126.9728938549",
                "mapy": "37.5629906688",
                "title": "고려삼계탕",
                "lDongRegnCd": "11",
                "lDongSignguCd": "140",
                "lclsSystm1": "FD",
                "lclsSystm2": "FD01",
                "lclsSystm3": "FD010100"
            }
        ]
    }