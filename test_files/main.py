# calendar data flow test

import pandas as pd
import json

async def main():

    food_includes = pd.read_csv("./data/food_include.csv")["includings"]
    hotel_includes = pd.read_csv("./data/hotel_includes.csv")["includings"]
    tour_excludes = pd.read_csv("./data/tour_exclude.csv")["excludings"]

    datas = json.loads("./test/calendar_datas.json")

    result = [[] for _ in range(3)]
    for data in datas:
        for i in range(3):
            if (data.get(f"lclsSystm{i}", "") in food_includes):
                result[0].append(data)
                continue
            if (data.get(f"lclsSystm{i}", "") in hotel_includes):
                result[1].append(data)
                continue
            if (data.get(f"lclsSystm{i}", "") not in tour_excludes):
                result[2].append(data)
                continue


    return
    