from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/calendar",
    tags=["Pick and Go Calendar service"]
)

@router.post("/")
async def post_calendar(item: modules.CalendarData, date: int = 3):

    return {"msg": "hellow world!"}

output_schema = \
{
    "accomodations" : [
        {
            "addr1": "전라남도 순천시 상사면 상사호길 555",
            "addr2": "",
            "areacode": "38",
            "cat1": "A02",
            "cat2": "A0204",
            "cat3": "A02040800",
            "contentid": "2469437",
            "contenttypeid": "12",
            "createdtime": "20161223235224",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
            "cpyrhtDivCd": "Type3",
            "mapx": "127.4143799419",
            "mapy": "34.9493972551",
            "mlevel": "6",
            "modifiedtime": "20250317125453",
            "sigungucode": "11",
            "tel": "",
            "title": "엄닭 3층",
            "zipcode": "57919",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX06",
            "lclsSystm3": "EX061000"
        },
        # ...
    ],
    "schedules" : [
        # 1일차 
        {
            "food" : [
                {
                    "addr1": "전라남도 순천시 상사면 상사호길 555",
                    "addr2": "",
                    "areacode": "38",
                    "cat1": "A02",
                    "cat2": "A0204",
                    "cat3": "A02040800",
                    "contentid": "2469437",
                    "contenttypeid": "12",
                    "createdtime": "20161223235224",
                    "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
                    "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
                    "cpyrhtDivCd": "Type3",
                    "mapx": "127.4143799419",
                    "mapy": "34.9493972551",
                    "mlevel": "6",
                    "modifiedtime": "20250317125453",
                    "sigungucode": "11",
                    "tel": "",
                    "title": "엄마닭",
                    "zipcode": "57919",
                    "lDongRegnCd": "46",
                    "lDongSignguCd": "150",
                    "lclsSystm1": "EX",
                    "lclsSystm2": "EX06",
                    "lclsSystm3": "EX061000"
                },
                # ...
            ],
            "tour_list" : [
                {
                    "addr1": "전라남도 순천시 상사면 상사호길 555",
                    "addr2": "",
                    "areacode": "38",
                    "cat1": "A02",
                    "cat2": "A0204",
                    "cat3": "A02040800",
                    "contentid": "2469437",
                    "contenttypeid": "12",
                    "createdtime": "20161223235224",
                    "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
                    "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
                    "cpyrhtDivCd": "Type3",
                    "mapx": "127.4143799419",
                    "mapy": "34.9493972551",
                    "mlevel": "6",
                    "modifiedtime": "20250317125453",
                    "sigungucode": "11",
                    "tel": "",
                    "title": "수원역 에반게리온 옷가게",
                    "zipcode": "57919",
                    "lDongRegnCd": "46",
                    "lDongSignguCd": "150",
                    "lclsSystm1": "EX",
                    "lclsSystm2": "EX06",
                    "lclsSystm3": "EX061000"
                },
                # ...
            ]
        },
        # 2일차, ...
    ]
}