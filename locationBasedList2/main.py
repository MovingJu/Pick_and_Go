from fastapi import FastAPI, Request
import httpx
import pandas as pd
import random
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

TOUR_API_SERVICE_KEY='qqUQuEEzgQ3bWYFK7f%2FLK%2FgoBk7qNm%2Fa6VpfpsW4m%2BX9V4WPiuHDIoWb%2FSrtmb3zD97gF4d0ghmgRGHB6xxXZQ%3D%3D'


randomData_list=[]
randomDataImage_list=[]
@app.get("/tour-attractions")
async def get_tour_attractions():
    global randomData_list
    global randomDataImage_list

    TOUR_API_BASE_URL = "https://apis.data.go.kr/B551011/KorService2/areaBasedList2"

    numOfRows=4

    while(len(randomData_list) != 15):
        randomPageNum=random.randrange(1, 12642)

        async with httpx.AsyncClient() as client:
            response = await client.get(TOUR_API_BASE_URL+"?serviceKey="+TOUR_API_SERVICE_KEY+f"&numOfRows={numOfRows}&pageNo={randomPageNum}&MobileOS=AND&MobileApp=PIGO&_type=json&arrange=C")

        response.raise_for_status()
        api_data = response.json()
        randomNum=random.randrange(4)

        iterateData_dict=api_data['response']['body']['items']['item'][randomNum]
        if(iterateData_dict['firstimage']):
            randomData_list.append(iterateData_dict)
            randomDataImage_list.append(iterateData_dict['firstimage'])

    return randomData_list, randomDataImage_list
