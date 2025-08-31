from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/calendar",
    tags=["Pick and Go main services"]
)

@router.post("/")
async def post_calendar(item: modules.CalendarData, date: int = 3):

    return {"msg": "hellow world!"}