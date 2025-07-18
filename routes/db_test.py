from fastapi import APIRouter

import modules

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)

@router.post("/user_regist")
async def user_regist(item: "modules.User_info"):
    return 