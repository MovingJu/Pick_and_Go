from pydantic import BaseModel

class User_info(BaseModel):
    """서버에 들어오는 유저 데이터 인풋을 정의"""
    user_id: str | None = None
    user_location: str
    user_tour_list: list['User_tour_loc']

class User_tour_loc_ess(BaseModel):
    """한국관광공사_국문 관광정보 서비스_GW를 활용할 수 있게 데이터 구조 중 필수적인 것들 정의"""
    addr1: str
    areacode: int | None = None
    contentid: int
    contenttypeid: int
    firstimage: str | None = None
    firstimage2: str | None
    lDongRegnCd: int
    lDongSignguCd: int
    lclsSystm1: str
    lclsSystm2: str
    lclsSystm3: str

class User_tour_loc(User_tour_loc_ess):
    """한국관광공사_국문 관광정보 서비스_GW를 활용할 수 있게 데이터 구조 정의"""
    addr2: str | None = None
    zipcode: int | None = None
    cat1: str | None = None
    cat2: str | None = None
    cat3: str | None = None
    createdtime: str | None = None
    dist: float | None = None
    cpyrhtDivCd: str | None = None
    mapx: float
    mapy: float
    mlevel: int | None = None
    modifiedtime: str | None = None
    sigungucode: int
    tel: str | None = None
    title: str

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