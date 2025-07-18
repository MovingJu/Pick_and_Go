from fastapi import APIRouter

import modules

router = APIRouter(
    tags=["Pick and Go main services"]
)


class Service():
    def __init__(self) -> None:
        self.user_tour_lists: list['modules.User_tour_loc'] = []

# @router.post("/input_test")
# async def input_test(item: modules.User_info):
#     return {"return test" : f"{item.user_location}, {item.user_tour_list[0].title}"}

@router.get("/")
async def index():
    return {"Still" : "working"}