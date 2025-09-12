from fastapi import APIRouter
import modules


router = APIRouter(
    prefix="/detail",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)


@router.get("/{contentId}")
async def get_info(contentId: str):

    # 개빠르게 조회하는 기능
    attraction_detail_url = modules.Url(
            "detailCommon2", 
            contentId="126128",
            numOfRows=1
        )
    api_client = await modules.TourAPI.create(attraction_detail_url)
    data = await api_client.fetch_async()

    print(data)

    # 조회한 데이터 함치는 기능


    return {"Message" : contentId}