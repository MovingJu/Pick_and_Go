from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/info",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)


class InputData(BaseModel):
    contentId: str


@router.get("/")
async def get_info(item: InputData):

    # 개빠르게 조회하는 기능
    # 조회한 데이터 함치는 기능


    return