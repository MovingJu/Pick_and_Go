from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/info",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)


class InputData(BaseModel):
    contentId: str


@router.get("/")
def get_info(item: InputData):
    return