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

ServerData_EXAMPLE = {
    "user_info": {
        "user_id": 4369726722,
        "user_name": "홍성학",
        "user_sex": 1,
        "user_age": 0
        },
    "interTour": {
        "count": 4,
        "items": [
        {
            "contentid": "1594500",
            "contenttypeid": "12",
            "addr1": "전북특별자치도 전주시 완산구 전주천동로 46",
            "title": "전주목판서화체험관",
            "mapx": 127.1556500663,
            "mapy": 35.8115147404,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image3_1.jpg",
            "lDongRegnCd": "52",
            "lDongSignguCd": "111",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX01",
            "lclsSystm3": "EX010100"
        },
        {
            "contentid": "2469437",
            "contenttypeid": "12",
            "addr1": "전라남도 순천시 상사면 상사호길 555",
            "title": "주암댐 물 문화관",
            "mapx": 127.4143799419,
            "mapy": 34.9493972551,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX06",
            "lclsSystm3": "EX061000"
        },
        {
            "contentid": "2643070",
            "contenttypeid": "39",
            "addr1": "서울특별시 중구 명동8가길 52",
            "title": "씨태번",
            "mapx": 126.9879897343,
            "mapy": 37.5618132993,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
            "lDongRegnCd": "11",
            "lDongSignguCd": "140",
            "lclsSystm1": "FD",
            "lclsSystm2": "FD02",
            "lclsSystm3": "FD020300"
        },
        {
            "contentid": "2670494",
            "contenttypeid": "39",
            "addr1": "전라남도 순천시 비봉길 73",
            "title": "큰집한우촌",
            "mapx": 127.520486865,
            "mapy": 34.9660361015,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "FD",
            "lclsSystm2": "FD01",
            "lclsSystm3": "FD010100"
        }
        ]
    },
    "visitedTour": {
        "count": 1,
        "items": [
        {
            "contentid": "1957444",
            "contenttypeid": "12",
            "addr1": "전라남도 순천시 공마당1길 64",
            "title": "용강서원(순천)",
            "mapx": 127.4761854654,
            "mapy": 34.9556198416,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image3_1.JPG",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "HS",
            "lclsSystm2": "HS01",
            "lclsSystm3": "HS010900"
        }
        ]
    },
    "etcData": {
        "location": [
        "전라남도 순천",
        "서울시 송파구"
        ],
        "numofPeople": 4
    }
}

CalendarData_EXAMPLE = {
    "user_info": {
        "user_id": 4369726722,
        "user_name": "홍성학",
        "user_sex": 1,
        "user_age": 0
        },
    "selectedTour": {
        "count" : 3,
        "items": [
            {
            "addr1": "전라남도 순천시 상사면 상사호길 555",
            "addr2": "",
            "areacode": "38",
            "cat1": "A02",
            "cat2": "A0204",
            "cat3": "A02040800",
            "contentid": "2469437",
            "contenttypeid": "12",
            "createdtime": "20161223235224",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
            "cpyrhtDivCd": "Type3",
            "mapx": "127.4143799419",
            "mapy": "34.9493972551",
            "mlevel": "6",
            "modifiedtime": "20250317125453",
            "sigungucode": "11",
            "tel": "",
            "title": "주암댐 물 문화관",
            "zipcode": "57919",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX06",
            "lclsSystm3": "EX061000"
            },
            {
            "addr1": "서울특별시 송파구 오금로 1 (신천동)",
            "addr2": "",
            "areacode": "1",
            "cat1": "A02",
            "cat2": "A0206",
            "cat3": "A02061000",
            "contentid": "2606740",
            "contenttypeid": "14",
            "createdtime": "20190615011829",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/38/3498038_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/38/3498038_image3_1.jpg",
            "cpyrhtDivCd": "Type1",
            "mapx": "117.9925662504",
            "mapy": "19.6944274800",
            "mlevel": "6",
            "modifiedtime": "20250617094233",
            "sigungucode": "18",
            "tel": "",
            "title": "서울책보고",
            "zipcode": "05507",
            "lDongRegnCd": "11",
            "lDongSignguCd": "710",
            "lclsSystm1": "VE",
            "lclsSystm2": "VE12",
            "lclsSystm3": "VE120100"
            },
            {
            "addr1": "전라남도 순천시 비례골길 24",
            "addr2": "",
            "areacode": "38",
            "cat1": "A02",
            "cat2": "A0204",
            "cat3": "A02040800",
            "contentid": "2469439",
            "contenttypeid": "12",
            "createdtime": "20161223235820",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/58/3079158_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/58/3079158_image3_1.jpg",
            "cpyrhtDivCd": "Type3",
            "mapx": "127.5378466518",
            "mapy": "34.9581872833",
            "mlevel": "6",
            "modifiedtime": "20250711100858",
            "sigungucode": "11",
            "tel": "",
            "title": "순천 드라마촬영장",
            "zipcode": "57972",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX06",
            "lclsSystm3": "EX061000"
            },
            {
            "addr1": "전라남도 순천시 금곡길 43 (금곡동)",
            "addr2": "",
            "areacode": "38",
            "cat1": "A02",
            "cat2": "A0203",
            "cat3": "A02030400",
            "contentid": "3062188",
            "contenttypeid": "12",
            "createdtime": "20231122152313",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/77/3062177_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/77/3062177_image3_1.jpg",
            "cpyrhtDivCd": "Type3",
            "mapx": "127.4803712332",
            "mapy": "34.9546616880",
            "mlevel": "6",
            "modifiedtime": "20250528105103",
            "sigungucode": "11",
            "tel": "",
            "title": "장안 창작마당",
            "zipcode": "57941",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "VE",
            "lclsSystm2": "VE12",
            "lclsSystm3": "VE120300"
            },
            {
            "addr1": "전라남도 순천시 국가정원1호길 152-55",
            "addr2": "(풍덕동)",
            "areacode": "38",
            "cat1": "A02",
            "cat2": "A0201",
            "cat3": "A02010300",
            "contentid": "2791413",
            "contenttypeid": "12",
            "createdtime": "20211210024601",
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/18/2791418_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/18/2791418_image3_1.JPG",
            "cpyrhtDivCd": "Type3",
            "mapx": "127.5095637484",
            "mapy": "34.9297372147",
            "mlevel": "6",
            "modifiedtime": "20250108151858",
            "sigungucode": "11",
            "tel": "",
            "title": "순천만국가정원 지구동문",
            "zipcode": "58000",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "HS",
            "lclsSystm2": "HS01",
            "lclsSystm3": "HS010300"
            }
        ]
    },
    "interTour": {
        "count": 4,
        "items": [
        {
            "contentid": "1594500",
            "contenttypeid": "12",
            "addr1": "전북특별자치도 전주시 완산구 전주천동로 46",
            "title": "전주목판서화체험관",
            "mapx": 127.1556500663,
            "mapy": 35.8115147404,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/17/3064017_image3_1.jpg",
            "lDongRegnCd": "52",
            "lDongSignguCd": "111",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX01",
            "lclsSystm3": "EX010100"
        },
        {
            "contentid": "2469437",
            "contenttypeid": "12",
            "addr1": "전라남도 순천시 상사면 상사호길 555",
            "title": "주암댐 물 문화관",
            "mapx": 127.4143799419,
            "mapy": 34.9493972551,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3370726_image3_1.JPG",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "EX",
            "lclsSystm2": "EX06",
            "lclsSystm3": "EX061000"
        },
        {
            "contentid": "2643070",
            "contenttypeid": "39",
            "addr1": "서울특별시 중구 명동8가길 52",
            "title": "씨태번",
            "mapx": 126.9879897343,
            "mapy": 37.5618132993,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/25/2655025_image2_1.jpg",
            "lDongRegnCd": "11",
            "lDongSignguCd": "140",
            "lclsSystm1": "FD",
            "lclsSystm2": "FD02",
            "lclsSystm3": "FD020300"
        },
        {
            "contentid": "2670494",
            "contenttypeid": "39",
            "addr1": "전라남도 순천시 비봉길 73",
            "title": "큰집한우촌",
            "mapx": 127.520486865,
            "mapy": 34.9660361015,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/20/2666620_image2_1.jpg",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "FD",
            "lclsSystm2": "FD01",
            "lclsSystm3": "FD010100"
        }
        ]
    },
    "visitedTour": {
        "count": 1,
        "items": [
        {
            "contentid": "1957444",
            "contenttypeid": "12",
            "addr1": "전라남도 순천시 공마당1길 64",
            "title": "용강서원(순천)",
            "mapx": 127.4761854654,
            "mapy": 34.9556198416,
            "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image2_1.JPG",
            "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3370716_image3_1.JPG",
            "lDongRegnCd": "46",
            "lDongSignguCd": "150",
            "lclsSystm1": "HS",
            "lclsSystm2": "HS01",
            "lclsSystm3": "HS010900"
        }
        ]
    },
    "etcData": {
        "location": [
        "전라남도 순천",
        "서울시 송파구"
        ],
        "numofPeople": 4
    }
}

class SelectedTour(BaseModel):
    count: int
    items: list[dict[str, str]]

class ServerData(BaseModel):
    user_info: UserInfo
    interTour: InterTour
    visitedTour: VisitedTour
    etcData: EtcData | Modified_EtcData
    class Config:
        json_schema_extra = {"example" : ServerData_EXAMPLE}

class CalendarData(BaseModel):
    user_info: UserInfo
    interTour: InterTour
    visitedTour: VisitedTour
    etcData: EtcData | Modified_EtcData
    selectedTour: SelectedTour
    class Config:
        json_schema_extra = {"example" : CalendarData_EXAMPLE}



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