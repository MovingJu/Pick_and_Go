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
    contentid: int
    contenttypeid: int
    dist: float | None = None
    firstimage: str | None = None
    firstimage2: str | None
    mapx: float
    mapy: float
    modifiedtime: str | None = None
    sigungucode: int
    tel: str | None = None
    title: str
    lDongRegnCd: int
    lDongSignguCd: int
    lclsSystm1: str
    lclsSystm2: str
    lclsSystm3: str

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}

@router.post("/input_test")
def input_test(item: Input_info):
    return {"return test" : f"{item.user_location}, {item.user_tour_lists[0].title}"}