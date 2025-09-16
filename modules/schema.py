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
    items: list[TourItem]

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


OUTPUT_EXAMPLE = {
  "accomodations": {
    "addr1": "울산광역시 중구 종가로 66",
    "addr2": "(태화동)",
    "areacode": "7",
    "cat1": "A03",
    "cat2": "A0302",
    "cat3": "A03021700",
    "contentid": "2730148",
    "contenttypeid": "28",
    "createdtime": "20210803233249",
    "firstimage": "http://tong.visitkorea.or.kr/cms/resource/33/2730533_image2_1.jpg",
    "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/33/2730533_image2_1.jpg",
    "cpyrhtDivCd": "Type3",
    "mapx": "129.2855552089",
    "mapy": "35.5625953030",
    "mlevel": "6",
    "modifiedtime": "20240510144034",
    "sigungucode": "1",
    "tel": "",
    "title": "태화연오토캠핑장",
    "zipcode": "44535",
    "lDongRegnCd": "31",
    "lDongSignguCd": "110",
    "lclsSystm1": "AC",
    "lclsSystm2": "AC05",
    "lclsSystm3": "AC050200"
  },
  "schedule": [
    {
      "food": [
        {
          "addr1": "울산광역시 중구 종가1길 14",
          "addr2": "1층",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020200",
          "contentid": "2848922",
          "contenttypeid": "39",
          "createdtime": "20220905113341",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/34/2848834_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/34/2848834_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.2940406835",
          "mapy": "35.5588903231",
          "mlevel": "6",
          "modifiedtime": "20250116161742",
          "sigungucode": "1",
          "tel": "",
          "title": "리코파스토 우정혁신본점",
          "zipcode": "44539",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD02",
          "lclsSystm3": "FD020300"
        },
        {
          "addr1": "울산광역시 중구 손골2길 17-6",
          "addr2": "(복산동,동덕아파트) 상가동",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020200",
          "contentid": "2785278",
          "contenttypeid": "39",
          "createdtime": "20211202224252",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/14/2785314_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/14/2785314_image2_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3255377425",
          "mapy": "35.5657234810",
          "mlevel": "6",
          "modifiedtime": "20241016090807",
          "sigungucode": "1",
          "tel": "",
          "title": "복산돈까스",
          "zipcode": "44430",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD02",
          "lclsSystm3": "FD020300"
        },
        {
          "addr1": "울산광역시 남구 정동로20번길 15",
          "addr2": "",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020100",
          "contentid": "2844775",
          "contenttypeid": "39",
          "createdtime": "20220829103814",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/73/2844773_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/73/2844773_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3456451682",
          "mapy": "35.5357022349",
          "mlevel": "6",
          "modifiedtime": "20240226152437",
          "sigungucode": "2",
          "tel": "",
          "title": "촌놈밥집",
          "zipcode": "44717",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD01",
          "lclsSystm3": "FD010100"
        }
      ],
      "tour_list": [
        {
          "addr1": "울산광역시 중구 원유곡길 106-1 (유곡동)",
          "addr2": "",
          "areacode": "7",
          "cat1": "A02",
          "cat2": "A0206",
          "cat3": "A02060200",
          "contentid": "3080895",
          "contenttypeid": "14",
          "createdtime": "20240112145052",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/45/3510545_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/45/3510545_image3_1.jpg",
          "cpyrhtDivCd": "Type1",
          "mapx": "129.2911601656",
          "mapy": "35.5664866370",
          "mlevel": "6",
          "modifiedtime": "20250722164316",
          "sigungucode": "1",
          "tel": "",
          "title": "수운최제우유허지 동학관",
          "zipcode": "44413",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "VE",
          "lclsSystm2": "VE07",
          "lclsSystm3": "VE070200"
        },
        {
          "addr1": "울산광역시 남구 문수로217번길 15",
          "addr2": "",
          "areacode": "7",
          "cat1": "A02",
          "cat2": "A0201",
          "cat3": "A02010800",
          "contentid": "2783743",
          "contenttypeid": "12",
          "createdtime": "20211130224056",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/12/3510812_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/12/3510812_image3_1.jpg",
          "cpyrhtDivCd": "Type1",
          "mapx": "129.2776509914",
          "mapy": "35.5395727427",
          "mlevel": "6",
          "modifiedtime": "20250729102634",
          "sigungucode": "2",
          "tel": "",
          "title": "정토사(울산)",
          "zipcode": "44642",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "HS",
          "lclsSystm2": "HS03",
          "lclsSystm3": "HS030100"
        },
        {
          "addr1": "울산광역시 중구 동헌길 167",
          "addr2": "(북정동)",
          "areacode": "7",
          "cat1": "A02",
          "cat2": "A0201",
          "cat3": "A02010100",
          "contentid": "2502612",
          "contenttypeid": "12",
          "createdtime": "20170808221303",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/21/3341921_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/21/3341921_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3202856482",
          "mapy": "35.5577409465",
          "mlevel": "6",
          "modifiedtime": "20250313140836",
          "sigungucode": "1",
          "tel": "",
          "title": "울산동헌 및 내아",
          "zipcode": "44468",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "HS",
          "lclsSystm2": "HS01",
          "lclsSystm3": "HS010100"
        }
      ]
    },
    {
      "food": [
        {
          "addr1": "울산광역시 남구 돋질로312번길 7",
          "addr2": "",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020200",
          "contentid": "2844809",
          "contenttypeid": "39",
          "createdtime": "20220829110215",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/07/2844807_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/07/2844807_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3389816591",
          "mapy": "35.5428457506",
          "mlevel": "6",
          "modifiedtime": "20240220142213",
          "sigungucode": "2",
          "tel": "",
          "title": "헤이다이닝",
          "zipcode": "44705",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD02",
          "lclsSystm3": "FD020300"
        },
        {
          "addr1": "울산광역시 중구 종가6길 22",
          "addr2": "",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020900",
          "contentid": "2871606",
          "contenttypeid": "39",
          "createdtime": "20221020130607",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/05/2871605_image2_1.JPG",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/05/2871605_image3_1.JPG",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3117890113",
          "mapy": "35.5632790528",
          "mlevel": "6",
          "modifiedtime": "20250114143254",
          "sigungucode": "1",
          "tel": "",
          "title": "스컹크웍스 우정점",
          "zipcode": "44542",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD05",
          "lclsSystm3": "FD050100"
        },
        {
          "addr1": "울산광역시 남구 삼산중로 24",
          "addr2": "1층",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020100",
          "contentid": "2841581",
          "contenttypeid": "39",
          "createdtime": "20220823115721",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/76/2841576_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/76/2841576_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3366737266",
          "mapy": "35.5357742796",
          "mlevel": "6",
          "modifiedtime": "20240624113503",
          "sigungucode": "2",
          "tel": "",
          "title": "착한물고기",
          "zipcode": "44720",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD01",
          "lclsSystm3": "FD010100"
        }
      ],
      "tour_list": [
        {
          "addr1": "울산광역시 중구 중앙1길 9",
          "addr2": "(성남동)",
          "areacode": "7",
          "cat1": "A02",
          "cat2": "A0206",
          "cat3": "A02060300",
          "contentid": "2795251",
          "contenttypeid": "14",
          "createdtime": "20211214190349",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/54/2795254_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/54/2795254_image2_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3197857306",
          "mapy": "35.5563549816",
          "mlevel": "6",
          "modifiedtime": "20250326102145",
          "sigungucode": "1",
          "tel": "",
          "title": "고복수음악관",
          "zipcode": "44529",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "VE",
          "lclsSystm2": "VE07",
          "lclsSystm3": "VE070300"
        },
        {
          "addr1": "울산광역시 중구 병영성11길 25 (서동)",
          "addr2": "",
          "areacode": "7",
          "cat1": "A02",
          "cat2": "A0201",
          "cat3": "A02010700",
          "contentid": "1624486",
          "contenttypeid": "12",
          "createdtime": "20120508035528",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/20/1588320_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/20/1588320_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3453246242",
          "mapy": "35.5756394057",
          "mlevel": "6",
          "modifiedtime": "20250805103639",
          "sigungucode": "1",
          "tel": "",
          "title": "삼일사",
          "zipcode": "44485",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "HS",
          "lclsSystm2": "HS01",
          "lclsSystm3": "HS010900"
        }
      ]
    },
    {
      "food": [
        {
          "addr1": "울산광역시 남구 남중로94번길 13 (삼산동)",
          "addr2": "",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020100",
          "contentid": "2871338",
          "contenttypeid": "39",
          "createdtime": "20221020103341",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/20/2871320_image2_1.JPG",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/20/2871320_image3_1.JPG",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3497223891",
          "mapy": "35.5428376209",
          "mlevel": "6",
          "modifiedtime": "20250903100721",
          "sigungucode": "2",
          "tel": "",
          "title": "완도참전복",
          "zipcode": "44712",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD01",
          "lclsSystm3": "FD010100"
        },
        {
          "addr1": "울산광역시 남구 월평로 205",
          "addr2": "",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020100",
          "contentid": "2927027",
          "contenttypeid": "39",
          "createdtime": "20221201161632",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/31/2926931_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/31/2926931_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3274186805",
          "mapy": "35.5463479177",
          "mlevel": "6",
          "modifiedtime": "20250604161332",
          "sigungucode": "2",
          "tel": "",
          "title": "울산언양불고기",
          "zipcode": "44696",
          "lDongRegnCd": "31",
          "lDongSignguCd": "140",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD01",
          "lclsSystm3": "FD010100"
        },
        {
          "addr1": "울산광역시 중구 중앙길 171-1",
          "addr2": "1층",
          "areacode": "7",
          "cat1": "A05",
          "cat2": "A0502",
          "cat3": "A05020900",
          "contentid": "2868021",
          "contenttypeid": "39",
          "createdtime": "20221017132140",
          "firstimage": "http://tong.visitkorea.or.kr/cms/resource/15/2868015_image2_1.jpg",
          "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/15/2868015_image3_1.jpg",
          "cpyrhtDivCd": "Type3",
          "mapx": "129.3227604570",
          "mapy": "35.5568633137",
          "mlevel": "6",
          "modifiedtime": "20250114133021",
          "sigungucode": "1",
          "tel": "",
          "title": "샬로우커피 성남점",
          "zipcode": "44530",
          "lDongRegnCd": "31",
          "lDongSignguCd": "110",
          "lclsSystm1": "FD",
          "lclsSystm2": "FD05",
          "lclsSystm3": "FD050100"
        }
      ],
      "tour_list": []
    }
  ]
}