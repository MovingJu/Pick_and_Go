from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from modules import db_structure, schema  # db_structure = SQLAlchemy, schemas = Pydantic
from modules.db_load import get_db  # db 세션 종속성

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)


@router.post("/user_regist")
async def user_regist(item: schema.User_info, db: Session = Depends(get_db)):
    # 1. 동일 user_id 유무 확인
    existing_user = db.query(db_structure.User).filter_by(name=item.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 2. 유저 생성
    new_user = db_structure.User(
        name=item.user_id,
        location=item.user_location
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. tour_list 항목들 추가
    for tour in item.user_tour_list:
        new_tour = db_structure.Tour_place(
            user_id=new_user.id,
            addr1=tour.addr1,
            areacode=tour.areacode,
            contentid=tour.contentid,
            contenttypeid=tour.contenttypeid,
            firstimage=tour.firstimage,
            firstimage2=tour.firstimage2,
            lDongRegnCd=tour.lDongRegnCd,
            lDongSignguCd=tour.lDongSignguCd,
            lclsSystm1=tour.lclsSystm1,
            lclsSystm2=tour.lclsSystm2,
            lclsSystm3=tour.lclsSystm3
        )
        db.add(new_tour)

    db.commit()

    return {"message": "User and tour list registered successfully", "user_id": new_user.id}
