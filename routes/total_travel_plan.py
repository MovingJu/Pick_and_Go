from fastapi import APIRouter, encoders
import json, pandas as pd
import modules, routes

from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
import numpy as np
import math, json

import httpx

router = APIRouter(
    prefix="/calendar",
    tags=["Pick and Go Calendar service"]
)

def distance(center: tuple[float, float], arr: np.ndarray):
    return np.sqrt((arr[:, 0] - center[0])**2 + (arr[:, 1] - center[1])**2)

@router.post("/")
async def post_calendar(item: modules.CalendarData, date: int = 3, food_day: int = 3, tour_day: int = 3):

    cached_tours = pd.read_csv("./data/user_tours.csv")

    # 여기 또한 마찬가지이다. 내가 짠 코드는 보통 내가 알지만 이 임포트 문제는 귀도 반 로섬도 모를게 분명하다...
    import json
    cached_tours = json.loads(
            str(cached_tours[cached_tours.iloc[:, 0] == item.user_info.user_id].iloc[0, 1])
        )

    tour: list[modules.schema.TourItem | dict[str, str]] = (item.selectedTour.items + cached_tours)[:100]

    food1 = await routes.post_food_list(item, 100)
    hotel = await routes.post_hotel_list(item, 10)

    food: list[dict[str, str]] = food1["data"]
    hotel = hotel["data"]
    
    gps = []
    for idx, val in enumerate(tour):
        if not isinstance(val, dict):
            val = val.model_dump()
        if float(val["mapx"]) < 120 or float(val["mapx"]) > 130:
            continue
        if float(val["mapy"]) < 30 or float(val["mapy"]) > 40:
            continue

        gps.append(
            (
                float(val["mapx"]), float(val["mapy"]), idx
            )
        )

    gps = np.array(gps)

    kmean = KMeans(
        n_clusters=date, 
        random_state=42
    ).fit(gps)


    labeled_gps = [[] for _ in range(date)]
    for idx, label in enumerate(kmean.labels_):
        labeled_gps[label].append(gps[idx])

    labeled_gps = [
        np.array(labeled_gps[i])
        for i in range(date)
    ]
    
    centerized_labeled_gps = []
    for idx, elem in enumerate(labeled_gps):
        temp = elem[np.argsort(distance(kmean.cluster_centers_[idx], elem))][:tour_day]
        centerized_labeled_gps.append(temp)

    modified_tour = []
    for sub_list in centerized_labeled_gps:
        temp = []
        for elem in sub_list:
            temp.append(
                tour[int(elem[2])]
            )
        modified_tour.append(temp)


    gps = []
    for idx, val in enumerate(food):
        if float(val["mapx"]) < 120 or float(val["mapx"]) > 130:
            continue
        if float(val["mapy"]) < 30 or float(val["mapy"]) > 40:
            continue

        gps.append(
            (
                float(val["mapx"]), float(val["mapy"]), idx
            )
        )
    gps = np.array(gps)

    centerized_gps = []
    for idx in range(date):
        temp = gps[np.argsort(distance(kmean.cluster_centers_[idx], gps))][:food_day]
        centerized_gps.append(temp)

    modified_food = []
    for sub_list in centerized_gps:
        temp = []
        for elem in sub_list:
            temp.append(
                tour[int(elem[2])]
            )
        modified_food.append(temp)

    schedules = [
        {
            "food" : modified_food[i],
            "tour_list" : modified_tour[i]
        }
        for i in range(date)
    ]

    result = {
        "accomodations" : hotel[0],
        "schedule" : schedules
    }


    # Main server에 랜덤 이미지 데이터 쏴주는 코드

    client_data = []
    for elem in hotel[:5]:
        client_data.append(elem)
    for sub_list in modified_food:
        client_data += sub_list
    for sub_list in modified_tour:
        client_data += sub_list

    server_data = "Server isn't turned on."
    response = {}
    try:
        from dotenv import load_dotenv
        import os
        response = {"data": client_data}
        load_dotenv()
        url_reciever = os.getenv("SEND_RANDOM_ENDPOINT") or ""

        # async with httpx.AsyncClient(cert=("./certifications/server.crt", "./certifications/server.key"), verify="./certifications/main_server.crt") as client:
        # async with httpx.AsyncClient(verify="./certifications/main_server1.crt") as client:
        async with httpx.AsyncClient(verify=False) as client:
            import json
            reciever_respond = await client.post(url_reciever, json=response)
        try:
            server_data = reciever_respond.json()
        except Exception:
            server_data = json.loads(reciever_respond.text)
    except Exception as e:
        print(f"error! : {e}")

    result["server response"] = server_data

    return result
