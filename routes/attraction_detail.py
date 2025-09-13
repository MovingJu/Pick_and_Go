from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/detail",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)

@router.get("/{contentId}")
async def get_info(contentId: str):

    base = ["detailCommon2", "detailIntro2", "detailInfo2"]

    # 개빠르게 조회하는 기능
    urls = []
    for i in base:
        urls.append(modules.Url(i, ))
    
    api_client = await modules.TourAPI.create(*urls)
    data = await api_client.fetch_async()

    # 조회한 데이터 함치는 기능

    return data