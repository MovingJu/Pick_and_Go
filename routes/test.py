from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/test",
    tags=["테스트 전용 엔드포인트임"]
)


@router.get("/image_compare")
async def image_compare():
    return {"To see descriptions" : "go to /docs"}