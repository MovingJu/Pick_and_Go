from fastapi import APIRouter, encoders
import json, pandas as pd
import modules, routes

router = APIRouter(
    prefix="/calendar",
    tags=["Pick and Go Calendar service"]
)

@router.post("/")
async def post_calendar(item: modules.CalendarData, date: int = 3, food_day: int = 3, tour_day: int = 3):

    cached_tours = pd.read_csv("./data/user_tours.csv")
    cached_tours = json.loads(
            str(cached_tours[cached_tours.iloc[:, 0] == item.user_info.user_id].iloc[0, 1])
        )

    tour = (item.selectedTour.items + cached_tours)[:400]

    food = await routes.post_food_list(item, 100000)
    hotel = await routes.post_hotel_list(item, 10)

    food = food["data"]
    hotel = hotel["data"]


    # temp = encoders.jsonable_encoder({
    #     "food" : food,
    #     "tour" : tour,
    #     "hotel" : hotel
    # })
    # with open("./result_sample.json", "w") as file:
    #     file.write(
    #         json.dumps(
    #             temp,
    #             indent=4,
    #             ensure_ascii=False
    #         )
    #     )

    # print(f"len food : {len(food)}, len tour : {len(tour)}")


    schedules = [
        {
            "food" : food[i * food_day : (i + 1) * food_day],
            "tour_list" : tour[i * tour_day : (i + 1) * tour_day]
        }
        for i in range(date)
    ]

    result = {
        "accomodations" : hotel[0],
        "schedule" : schedules
    }


    return result
