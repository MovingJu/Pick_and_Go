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

    df = pd.read_csv("./data/user_tours.csv", encoding="utf-8")

    user_id = item.user_info.user_id
    if user_id in df["user_id"].values:
        saved_tours = json.loads(df.loc[df["user_id"] == user_id, "tours"].values[0])
    else:
        saved_tours = []

    full_tour = selected_tours + saved_tours
    if (len(full_tour) < 100):
        temp = await routes.post_tour_list(item, 10000)
        full_tour += temp["data"]

    full_food = await routes.post_food_list(item, 100000)
    full_hotel = await routes.post_hotel_list(item, 100000)


    await routes.get_related(item)

    # 순서 매겨야함
    food = full_food["data"]
    tour = full_tour

    print(f"len food : {len(food)}, len tour : {len(tour)}")


    schedules = [
        {
            "food" : food[i * food_day : (i + 1) * food_day],
            "tour_list" : tour[i * tour_day : (i + 1) * tour_day]
        }
        for i in range(date)
    ]

    result = {
        "accomodations" : full_hotel.get("data", [None])[0],
        "schedule" : schedules
    }

    return result
