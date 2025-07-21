from fastapi import APIRouter

router = APIRouter(
    prefix="/random",
    tags=["랜덤 사진 제공 엔드포인트임"]
)

@router.get("/")
async def read_item():
    """랜덤 사진 주는 코드~~~"""

    

    return {"result": result}
