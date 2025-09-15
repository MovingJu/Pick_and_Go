from fastapi import APIRouter
import json
import modules
import html2text

router = APIRouter(
    prefix="/detail",
    tags=["관광지 세부 정보 제공 엔드포인트임."]
)

@router.get("/{contentId}")
async def get_info(contentId: str):

    converter = html2text.HTML2Text()
    converter.ignore_links = True


    detail_url_base_list=['detailCommon2','detailPetTour2']
    detail_url_base_list2=['detailIntro2','detailInfo2']
    detail_url_base_list2_contentTypeId=[12,14,15,25,28,32,38,39]
    detail_url_list=[]
    for i in detail_url_base_list:
        detail_url_list.append(modules.Url(i, contentId=contentId))
    for i in detail_url_base_list2:
        for j in detail_url_base_list2_contentTypeId:
            detail_url_list.append(modules.Url(i, contentId=contentId, contentTypeId=j))
    api_client = await modules.TourAPI.create(*detail_url_list)
    fetched_data_temp = await api_client.fetch_async() #불러온 데이터
    fetched_data=[]

    #내용 없는 애들은 삭제
    for i in fetched_data_temp:
        if(i['data']['response']['body']['totalCount']!=0):
            fetched_data.append(i)
            

    extracted_data={} #추출된 데이터 넣는 곳

    detail_0_extract_list=['tel','homepage','overview','restdate','usetime','parking']
    detail_1_extract_list=['relaAcdntRiskMtr',"acmpyTypeCd","relaPosesFclty","relaFrnshPrdlst","etcAcmpyInfo","relaPurcPrdlst","acmpyPsblCpam","relaRntlPrdlst","acmpyNeedMtr"]
    detail_2_extract_list=['infoname']

    for i in fetched_data:
        for j in i['data']['response']['body']['items']['item']:
            for k_key, k_value in j.items():
                if(k_key in detail_0_extract_list and k_value):
                    extracted_data[k_key]=converter.handle(k_value).replace('\n','')
                elif(k_key in detail_1_extract_list and k_value):
                    if('pet_detail' not in extracted_data.keys()):
                        extracted_data['pet_detail']=converter.handle(k_value).replace('\n','')
                    else:
                        extracted_data['pet_detail']+=', '+converter.handle(k_value).replace('\n','')
                elif(k_key in detail_2_extract_list):
                    extracted_data[converter.handle(k_value).replace('\n','')]=converter.handle(j['infotext']).replace('\n','')
                else:
                    continue

    return extracted_data