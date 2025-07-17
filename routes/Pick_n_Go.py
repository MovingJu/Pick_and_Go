from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter(
    tags=["Pick and Go main services"]
)

class Input_info(BaseModel):
    user_location: str
    user_tour_lists: list['User_tour_list']

class User_tour_list(BaseModel):
    addr1: str
    addr2: str | None = None
    zipcode: int | None = None
    areacode: int | None = None
    cat1: str | None = None
    cat2: str | None = None
    cat3: str | None = None
    contentid: int
    contenttypeid: int
    createdtime: str | None = None
    dist: float | None = None
    firstimage: str | None = None
    firstimage2: str | None
    cpyrhtDivCd: str | None = None
    mapx: float
    mapy: float
    mlevel: int | None = None
    modifiedtime: str | None = None
    sigungucode: int
    tel: str | None = None
    title: str
    lDongRegnCd: int
    lDongSignguCd: int
    lclsSystm1: str
    lclsSystm2: str
    lclsSystm3: str

@router.post("/input_test")
async def input_test(item: Input_info):
    return {"return test" : f"{item.user_location}, {item.user_tour_lists[0].title}"}