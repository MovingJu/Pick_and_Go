from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from modules import User_info, User, Tour_place, engine, Base
from modules.db_load import get_async_session

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)

@router.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@router.post("/user_regist")
async def user_regist(
    item: User_info,
    session: AsyncSession = Depends(get_async_session)
):
    # 1. 사용자 중복 확인
    result = await session.execute(select(User).where(User.name == item.user_name))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 2. User 객체 생성
    new_user = User(
        name=item.user_name if (item.user_name) else "Unknown",
        location=item.user_location if (item.user_location) else ""
    )
    session.add(new_user)
    await session.flush()  # user.id 값을 가져오기 위해

    # 3. 각 관광지 정보 저장
    for tour_item in item.user_tour_list:
        tour = Tour_place(
            user_id=new_user.id,
            addr1=tour_item.addr1,
            areacode=tour_item.areacode,
            contentid=tour_item.contentid,
            contenttypeid=tour_item.contenttypeid,
            firstimage=tour_item.firstimage,
            firstimage2=tour_item.firstimage2,
            lDongRegnCd=tour_item.lDongRegnCd,
            lDongSignguCd=tour_item.lDongSignguCd,
            lclsSystm1=tour_item.lclsSystm1,
            lclsSystm2=tour_item.lclsSystm2,
            lclsSystm3=tour_item.lclsSystm3,
        )
        session.add(tour)

    await session.commit()

    return {"message": f"User '{new_user.name}' and {len(item.user_tour_list)} tour places registered successfully."}
