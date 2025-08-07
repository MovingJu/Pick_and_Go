from pydantic import BaseModel

### 추천 API에 POST로 들어오는 데이터
class TourItem(BaseModel):
    contentid: str
    contenttypeid: str
    addr1: str
    title: str
    mapx: float
    mapy: float
    firstimage: str
    firstimage2: str
    lDongRegnCd: str
    lDongSignguCd: str
    lclsSystm1: str
    lclsSystm2: str
    lclsSystm3: str

class EtcData(BaseModel):
    location: list[str]
    class Config:
        extra = "allow"

class Modified_EtcData(BaseModel):
    location: list[tuple[int, int]]
    class Config:
        extra = "allow"

class InterTour(BaseModel):
    count: int
    items: list[TourItem]

class VisitedTour(BaseModel):
    count: int
    items: list[TourItem]

class UserInfo(BaseModel):
    user_id: int
    user_name: str
    user_sex: int | None
    user_age: int

class ServerData(BaseModel):
    user_info: UserInfo
    interTour: InterTour
    visitedTour: VisitedTour
    etcData: EtcData | Modified_EtcData


### DB 초기화를 위한 데이터 (이제 안씀)
DB_TABLE_SETUP_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250),
    location VARCHAR(500)
);
CREATE TABLE IF NOT EXISTS tour_places (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    addr1 VARCHAR(250) NOT NULL,
    areacode INT,
    contentid INT NOT NULL,
    contenttypeid INT NOT NULL,
    firstimage VARCHAR(500),
    firstimage2 VARCHAR(500),
    lDongRegnCd INT NOT NULL,
    lDongSignguCd INT NOT NULL,
    lclsSystm1 VARCHAR(20) NOT NULL,
    lclsSystm2 VARCHAR(20) NOT NULL,
    lclsSystm3 VARCHAR(20) NOT NULL
);
CREATE TABLE IF NOT EXISTS sigungu_sido (
    city_id INT NOT NULL,
    city_name VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS sigungu_sigungu (
    city_id INT NOT NULL,
    city_name VARCHAR(100),
    parent_city_id INT NOT NULL
);
"""