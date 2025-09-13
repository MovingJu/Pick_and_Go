from fastapi import APIRouter
import json
import modules

router = APIRouter(
    prefix="/detail",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)

@router.get("/{contentId}")
async def get_info(contentId: str):

    #detail_url_base_list=['detailCommon2','detailIntro2','detailInfo2','detailPetTour2']
    detail_url_base_list=['detailCommon2','detailPetTour2']
    detail_url_list=[]
    for i in detail_url_base_list:
        detail_url_list.append(modules.Url(i, contentId=contentId))
    api_client = await modules.TourAPI.create(*detail_url_list)
    fetched_data = await api_client.fetch_async()

    extracted_data={}

    fetched_data[0]=fetched_data[0]['data']['response']['body']['items']['item'][0]
    detail_0_extract_list=['tel','homepage','overview']
    for i in detail_0_extract_list:
        if(fetched_data[0][i]):
            extracted_data[i]=fetched_data[0][i]

    fetched_data[1]=fetched_data[1]['data']['response']['body']['items']['item'][0]
    detail_1_extract_list=['relaAcdntRiskMtr',"acmpyTypeCd","relaPosesFclty","relaFrnshPrdlst","etcAcmpyInfo","relaPurcPrdlst","acmpyPsblCpam","relaRntlPrdlst","acmpyNeedMtr"]
    for i in detail_1_extract_list:
        if(fetched_data[1][i]):
            if('pet_detail' not in extracted_data.keys()):
                extracted_data['pet_detail']=str(fetched_data[1][i])
            else:
                extracted_data['pet_detail']+=', '+str(fetched_data[1][i])

    return extracted_data