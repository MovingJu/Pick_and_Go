from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/detail",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)

@router.get("/{contentId}")
async def get_info(contentId: str):

    detail_url_base_list=['detailCommon2','detailIntro2','detailInfo2','detailPetTour2']
    detail_url_list=[]
    for i in detail_url_base_list:
        detail_url_list.append(modules.Url(i, contentId=contentId))
    api_client = await modules.TourAPI.create(*detail_url_list)
    data = await api_client.fetch_async()

    

    return data