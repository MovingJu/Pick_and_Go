from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["테스트 전용 엔드포인트임"]
)


@router.get("/")
async def test():
    return {
        "status" : 200, 
        "message" : "매우 잘 작동중!"
    }