from fastapi import FastAPI, Request
import httpx
import pandas as pd
import random
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from urllib import parse #혹시나 사진 키워드 검색 해야하면 사용
#parse.quote('한글') - 인코딩
#parse.unquote('(%EA%B5%AC)%EA%B0%80%EC%9E%85%EC%9E%90%EB%B2%88%ED%98%B8') - 디코딩

app = FastAPI()

TOUR_API_SERVICE_KEY='qqUQuEEzgQ3bWYFK7f%2FLK%2FgoBk7qNm%2Fa6VpfpsW4m%2BX9V4WPiuHDIoWb%2FSrtmb3zD97gF4d0ghmgRGHB6xxXZQ%3D%3D'

signgu_df=pd.read_excel("./한국관광공사_TourAPI_관광지_시군구_코드정보_v1.0.xlsx", engine="openpyxl")
user_area_input="경기도"
user_signgu_input="수원시 영통구"

area_code_row = signgu_df[signgu_df['areaNm'] == user_area_input]
sigungu_code_row = signgu_df[(signgu_df['areaNm'] == user_area_input) & (signgu_df['sigunguNm'] == user_signgu_input)]

@app.get("/tour-attractions")
async def get_tour_attractions():
    TOUR_API_BASE_URL = "http://apis.data.go.kr/B551011/LocgoHubTarService1/areaBasedList1"

    pageNo_1=1
    numOfRows_1=500
    baseYm_1=202506
    areaCd_1 = area_code_row['areaCd'].iloc[0]
    signguCd_1 = sigungu_code_row['sigunguCd'].iloc[0]

    async with httpx.AsyncClient() as client:
        response = await client.get(TOUR_API_BASE_URL+"?serviceKey="+TOUR_API_SERVICE_KEY+f"&pageNo={pageNo_1}&numOfRows={numOfRows_1}&MobileOS=AND&MobileApp=AppTest&baseYm={baseYm_1}&areaCd={areaCd_1}&signguCd={signguCd_1}&_type=json")

    response.raise_for_status()
    api_data = response.json()

    tourSpotsNm_list=[]
    hubCtgryMclsNm_list=[]

    for i in api_data['response']['body']['items']['item']:
        tourSpotsNm_list.append(i['hubTatsNm'])
        hubCtgryMclsNm_list.append(i['hubCtgryMclsNm'])

    return tourSpotsNm_list


URL_list=[] #URL 10개 들어가있음
galTitle_list=[]
imageDictList=[]
@app.get("/tour-images")
async def get_images():
    TOUR_API_BASE_URL = "https://apis.data.go.kr/B551011/PhotoGalleryService1/galleryList1"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TOUR_API_BASE_URL}?serviceKey={TOUR_API_SERVICE_KEY}&numOfRows=6000&pageNo=1&MobileOS=AND&MobileApp=AppTest&arrange=A&_type=json")

    response.raise_for_status()
    api_data = response.json()

    imageData_list=api_data['response']['body']['items']['item'] #이미지데이터들이 딕셔너리 형태로 들어가있는 리스트
    imageNum=len(imageData_list) #아마도 5800
    random_numbers = random.sample(range(0, imageNum), 10) #랜덤숫자 10개가 리스트에

    global URL_list
    global galTitle_list
    global imageDictList
    # 새로운 데이터를 채우기 전에 기존 리스트를 비웁니다.
    URL_list.clear()
    galTitle_list.clear()
    imageDictList.clear()

    keyWord_list=[] #(10,n)의 2중리스트
    for i in random_numbers:
        URL_list.append(imageData_list[i]['galWebImageUrl'])
        keyWord_list_iteration = imageData_list[i]['galSearchKeyword'].split(',')
        keyWord_list.append(keyWord_list_iteration)
        galTitle_list.append(imageData_list[i]['galTitle'])

        imageDict={'galTitle':imageData_list[i]['galTitle'], 'URL_list':imageData_list[i]['galWebImageUrl'], 'keyWord_list':keyWord_list_iteration}
        imageDictList.append(imageDict)

    return imageDictList



templates = Jinja2Templates(directory="templates")

@app.get("/images-show", response_class=HTMLResponse)
async def read_gallery(request: Request):
    await get_images()
    return templates.TemplateResponse(
        "tour_image.html", {"request": request, "images_data": imageDictList}
    )

# class tourSpot:
#     def __init__(self, _baseYm, _mapX, _mapY, _areaCd, _areaNm, _signguCd, _signguNm, _hubTatsCd, _hubTatsNm, _hubCtgryLclsNm, _hubCtgryMclsNm, _hubRank):
#         self.baseYm=_baseYm
#         self.mapX=_mapX
#         self.mapY=_mapY
#         self.areaCd=_areaCd
#         self.areaNm=_areaNm
#         self.signguCd=_signguCd
#         self.signguNm=_signguNm
#         self.hubTatsCd=_hubTatsCd
#         self.hubTatsNm=_hubTatsNm
#         self.hubCtgryLclsNm=_hubCtgryLclsNm
#         self.hubCtgryMclsNm=_hubCtgryMclsNm
#         self.hubRank=_hubRank


# class imageData:
#     def __init__(self,_galContentId,_galContentTypeId,_galTitle,_galWebImageUrl,_galCreatedtime,_galPhotographyMonth,_galPhotographyLocation,_galPhotographer,_galSearchKeyword):
#         self.galContentId=_galContentId
#         self.galContentTypeId=_galContentTypeId
#         self.galTitle=_galTitle
#         self.galWebImageUrl=_galWebImageUrl
#         self.galCreatedtime=_galCreatedtime
#         self.galModifiedtime=_galCreatedtime
#         self.galPhotographyMonth=_galPhotographyMonth
#         self.galPhotographyLocation=_galPhotographyLocation
#         self.galPhotographer=_galPhotographer
#         self.galSearchKeyword=_galSearchKeyword