from fastapi import APIRouter
import json, pandas as pd
import modules, routes

router = APIRouter(
    prefix="/calendar",
    tags=["Pick and Go Calendar service"]
)

@router.post("/")
async def post_calendar(item: modules.CalendarData, date: int = 3, food_day: int = 3, tour_day: int = 3):

    selected_tours = item.selectedTour.items

    requ_tour = date * tour_day - len(selected_tours)

    # 최신 CSV 불러오기
    df = pd.read_csv("./data/user_tours.csv", encoding="utf-8")

    # 특정 user_id 불러오기 (예: 123)
    user_id = 123
    if user_id in df["user_id"].values:
        saved_tours = json.loads(df.loc[df["user_id"] == user_id, "tours"].values[0])
    else:
        saved_tours = []

    # 새로운 선택과 합치기
    full_tour = selected_tours + saved_tours

    full_food = await routes.post_food_list(item, date * food_day)
    full_hotel = await routes.post_hotel_list(item, 5)

    print(f"len food : {len(full_food)}, len hotel : {len(full_hotel)}")

    schedules = [
        {
            "food" : full_food["data"][i * food_day : (i + 1) * food_day],
            "tour_list" : full_tour[i * tour_day : (i + 1) * tour_day]
        }
        for i in range(date)
    ]

    result = {
        "accomodations" : full_hotel.get("data", [None])[0],
        "schedule" : schedules
    }

    return result

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
            "tour" : [
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