def Count_model(item, local_data):
    from collections import Counter
    
    user_preference_counts = Counter(tour["lclsSystm3"] for tour in item.tours)

    # 2. data의 관광지 코드를 기반으로 점수 계산
    scored_places = []
    for place in local_data["items"]:
        place_code = place["lclsSystm3"]
        # 사용자의 선호 코드가 data에 있으면 해당 빈도수를 점수로 추가, 없으면 0점
        score = user_preference_counts.get(place_code, 0)
        scored_places.append((place, score))

    # 3. 점수가 높은 순으로 정렬
    scored_places.sort(key=lambda x: x[1], reverse=True)
    scored_only_places = [scored_places[i][0] for i in range(len(scored_places))]
    # 4. 상위 5개 출력
    top_5_places = [place[0] for place in scored_places[:5]]

    # 결과 출력
    # print("사용자가 선호할 것 같은 관광지 상위 5개:")
    # for place in top_5_places:
    #     print(f"  - {place[1]} (분류코드: {place[2]}, 점수: {user_preference_counts.get(place[2], 0)})")

    return scored_only_places

def Image_based_model(item, local_data):
    
    data_url_feature=[] #(112,2048,0)
    for i in local_data["items"]:
        data_url_feature.append(Image_comparison.extract_features(i["firstimage"]))

    user_input_url_feature=[] #(7,2048,0)
    for i in item.tours:
        user_input_url_feature.append(Image_comparison.extract_features(i["firstimage"]))
    
    X=[]
    for i in data_url_feature:
        iter_list=[]
        for j in user_input_url_feature:
            iter_list.append(Image_comparison.cosine_similarity(i, j))
        X.append(iter_list)

    X=np.array(X) #(112, 7)
    X=X@X.T #(112, 112)

    column_sums = X.sum(axis=0, keepdims=True)
    num_rows = X.shape[0]
    column_sums[column_sums == 0] = 1
    X = X / column_sums

    init=[]
    for i in local_data["items"]:
        score=0
        for j in item.tours:
            if(i["firstimage"]==j["firstimage"]):
                score+=5
            elif(i["firstimage"][:-4]==j["firstimage"][:-4]):
                score+=3
            elif(i["firstimage"][:-6]==j["firstimage"][:-6]):
                score+=1
        init.append(score)
    init=np.array(init)

    while(init.all()!=(X@init).all()):
        init=X@init

    sorted_indices = np.argsort(init)
    top_5_indices = sorted_indices[::-1][:5]

    top_5 = []
    for i in top_5_indices:
        top_5.append(local_data["items"][i])
        print(local_data["items"][i])

    return top_5

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO
import numpy as np
class Image_comparison:
    
    @staticmethod
    def extract_features(image_url):

        def get_feature_extractor():
            model = models.resnet18(pretrained=True)
            feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
            feature_extractor.eval()
            return feature_extractor
        
        feature_extractor = get_feature_extractor()

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data).convert("RGB")

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = preprocess(pil_image).unsqueeze(0) # type: ignore

        with torch.no_grad():
            features = feature_extractor(image_tensor)
            features = features.squeeze().numpy()
        return features

    @staticmethod
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))



if __name__ == "__main__":

    Image_based_model(
        {
        "user_id" : "-1",
        "total_count" : 2,
        "tours" : [
            {
                "addr1": "서울특별시 중구 세종대로11길 35",
                "contentid": "232229",
                "mapx": "126.9739382319",
                "mapy": "37.5619935812",
                "title": "강서면옥",
                "firstimage" : "http://tong.visitkorea.or.kr/cms/resource/49/2675149_image2_1.jpg",
                "lDongRegnCd": "11",
                "lDongSignguCd": "140",
                "lclsSystm1": "FD",
                "lclsSystm2": "FD01",
                "lclsSystm3": "FD010100"
            },
            {
                "addr1": "서울특별시 중구 서소문로11길 1",
                "contentid": "133854",
                "mapx": "126.9728938549",
                "mapy": "37.5629906688",
                "title": "고려삼계탕",
                "firstimage" : "http://tong.visitkorea.or.kr/cms/resource/44/2675144_image2_1.jpg",
                "lDongRegnCd": "11",
                "lDongSignguCd": "140",
                "lclsSystm1": "FD",
                "lclsSystm2": "FD01",
                "lclsSystm3": "FD010100"
            }
        ]
    },
    {
   "totalCount": 169,
   "items": [
      {
         "addr1": "울산광역시 남구 장생포고래로 244 (매암동)",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0207",
         "cat3": "A02070200",
         "contentid": "553263",
         "contenttypeid": "15",
         "createdtime": "20130222021348",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/76/3513276_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/76/3513276_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3808374607",
         "mapy": "35.5032009945",
         "mlevel": "6",
         "modifiedtime": "20250804103501",
         "sigungucode": "2",
         "tel": "052-226-0028~9",
         "title": "울산고래축제",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EV",
         "lclsSystm2": "EV01",
         "lclsSystm3": "EV010500"
      },
      {
         "addr1": "울산광역시 남구 번영로 212",
         "addr2": "(달동)",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0206",
         "cat3": "A02060600",
         "contentid": "129732",
         "contenttypeid": "14",
         "createdtime": "20071106102725",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/03/1899503_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/03/1899503_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3265854644",
         "mapy": "35.5447647459",
         "mlevel": "6",
         "modifiedtime": "20250731163044",
         "sigungucode": "2",
         "tel": "",
         "title": "KBS 울산홀",
         "zipcode": "44702",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE06",
         "lclsSystm3": "VE060100"
      },
      {
         "addr1": "울산광역시 남구 테크노산업로55번길 49-20 (두왕동)",
         "addr2": "THE101 4층",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0206",
         "cat3": "A02060300",
         "contentid": "3116496",
         "contenttypeid": "14",
         "createdtime": "20240507155146",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/56/3116456_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/56/3116456_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3015747410",
         "mapy": "35.5098015389",
         "mlevel": "6",
         "modifiedtime": "20250730160419",
         "sigungucode": "2",
         "tel": "",
         "title": "더101 뮤지엄",
         "zipcode": "44776",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE07",
         "lclsSystm3": "VE070300"
      },
      {
         "addr1": "울산광역시 남구 장생포고래로 271-1",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030100",
         "contentid": "2381176",
         "contenttypeid": "12",
         "createdtime": "20160428200139",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/08/2658308_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/08/2658308_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3831649569",
         "mapy": "35.5059840591",
         "mlevel": "6",
         "modifiedtime": "20250730090430",
         "sigungucode": "2",
         "tel": "",
         "title": "장생포 고래문화마을",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE04",
         "lclsSystm3": "VE040200"
      },
      {
         "addr1": "울산광역시 남구 대공원로 94",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020600",
         "contentid": "2002486",
         "contenttypeid": "12",
         "createdtime": "20150511233748",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/07/3510807_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/07/3510807_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.2940414740",
         "mapy": "35.5308045918",
         "mlevel": "6",
         "modifiedtime": "20250729144631",
         "sigungucode": "2",
         "tel": "",
         "title": "울산대공원 동물원",
         "zipcode": "44660",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE02",
         "lclsSystm3": "VE020300"
      },
      {
         "addr1": "울산광역시 남구 선암동",
         "addr2": "769",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030400",
         "contentid": "2754494",
         "contenttypeid": "12",
         "createdtime": "20211007192818",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3510816_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3510816_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.3198284839",
         "mapy": "35.5176398904",
         "mlevel": "6",
         "modifiedtime": "20250729133616",
         "sigungucode": "2",
         "tel": "",
         "title": "선암호수공원 무지개놀이터",
         "zipcode": "44774",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EX",
         "lclsSystm2": "EX07",
         "lclsSystm3": "EX070200"
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
         "addr1": "울산광역시 남구 번영로 224",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0206",
         "cat3": "A02060700",
         "contentid": "130396",
         "contenttypeid": "14",
         "createdtime": "20071106105529",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/75/3510775_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/75/3510775_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.3255744272",
         "mapy": "35.5452785581",
         "mlevel": "6",
         "modifiedtime": "20250729102125",
         "sigungucode": "2",
         "tel": "",
         "title": "울산광역시남구문화원",
         "zipcode": "44702",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE09",
         "lclsSystm3": "VE090100"
      },
      {
         "addr1": "울산광역시 남구 문수로 44",
         "addr2": "(옥동)",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020700",
         "contentid": "129453",
         "contenttypeid": "12",
         "createdtime": "20070920090000",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/37/3510837_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/37/3510837_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.2595610237",
         "mapy": "35.5352867733",
         "mlevel": "6",
         "modifiedtime": "20250724104336",
         "sigungucode": "2",
         "tel": "",
         "title": "울산체육공원",
         "zipcode": "44659",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE03",
         "lclsSystm3": "VE030500"
      },
      {
         "addr1": "울산광역시 남구 남부순환도로 209",
         "addr2": "(옥동)",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020600",
         "contentid": "2778109",
         "contenttypeid": "12",
         "createdtime": "20211123201307",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/02/3510802_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/02/3510802_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.2719794985",
         "mapy": "35.5312346843",
         "mlevel": "6",
         "modifiedtime": "20250724104120",
         "sigungucode": "2",
         "tel": "",
         "title": "울산애견공원",
         "zipcode": "44660",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE02",
         "lclsSystm3": "VE020100"
      },
      {
         "addr1": "울산광역시 남구 삼산로 288 (삼산동)",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020600",
         "contentid": "3065279",
         "contenttypeid": "12",
         "createdtime": "20231211114418",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/64/3065264_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/64/3065264_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3387790086",
         "mapy": "35.5389628501",
         "mlevel": "6",
         "modifiedtime": "20250723134749",
         "sigungucode": "2",
         "tel": "",
         "title": "울산 롯데 그랜드 휠",
         "zipcode": "44719",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE02",
         "lclsSystm3": "VE020100"
      },
      {
         "addr1": "울산광역시 남구 장생포고래로 110 (장생포동)",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030400",
         "contentid": "3027519",
         "contenttypeid": "12",
         "createdtime": "20230925141347",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/88/3072288_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/88/3072288_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3673164077",
         "mapy": "35.5035257033",
         "mlevel": "6",
         "modifiedtime": "20250721153648",
         "sigungucode": "2",
         "tel": "",
         "title": "장생포 문화창고",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE12",
         "lclsSystm3": "VE120300"
      },
      {
         "addr1": "울산광역시 남구 남부순환도로 555 (신정동)",
         "addr2": "",
         "areacode": "7",
         "cat1": "A03",
         "cat2": "A0302",
         "cat3": "A03020200",
         "contentid": "3065312",
         "contenttypeid": "28",
         "createdtime": "20231211115337",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/96/3065296_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/96/3065296_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3009494625",
         "mapy": "35.5216474180",
         "mlevel": "6",
         "modifiedtime": "20250718162906",
         "sigungucode": "2",
         "tel": "",
         "title": "시립 문수 궁도장",
         "zipcode": "44668",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE10",
         "lclsSystm3": "VE100200"
      },
      {
         "addr1": "울산광역시 남구 두왕로 277",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0206",
         "cat3": "A02060100",
         "contentid": "1556541",
         "contenttypeid": "14",
         "createdtime": "20120221015510",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/36/3072936_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/36/3072936_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3087097418",
         "mapy": "35.5271580556",
         "mlevel": "6",
         "modifiedtime": "20250714114114",
         "sigungucode": "2",
         "tel": "",
         "title": "울산박물관",
         "zipcode": "44668",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE07",
         "lclsSystm3": "VE070100"
      },
      {
         "addr1": "울산광역시 남구 여천로66번길 7",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030100",
         "contentid": "2611134",
         "contenttypeid": "12",
         "createdtime": "20190715231142",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3014916_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3014916_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3413431085",
         "mapy": "35.5235174122",
         "mlevel": "6",
         "modifiedtime": "20250709142832",
         "sigungucode": "2",
         "tel": "",
         "title": "울산 신화마을",
         "zipcode": "44766",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE04",
         "lclsSystm3": "VE040200"
      },
      {
         "addr1": "울산광역시 남구 무거동",
         "addr2": "삼호로 15",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030400",
         "contentid": "3074623",
         "contenttypeid": "12",
         "createdtime": "20230925135400",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/22/3074622_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/22/3074622_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.2649074229",
         "mapy": "35.5479687810",
         "mlevel": "6",
         "modifiedtime": "20250703153114",
         "sigungucode": "2",
         "tel": "",
         "title": "무거천 벚꽃길",
         "zipcode": "44603",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EX",
         "lclsSystm2": "EX07",
         "lclsSystm3": "EX070200"
      },
      {
         "addr1": "울산광역시 남구 남산로 306",
         "addr2": "(신정동)",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0203",
         "cat3": "A02030400",
         "contentid": "2605809",
         "contenttypeid": "12",
         "createdtime": "20190611020002",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/08/2601308_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/08/2601308_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3024681091",
         "mapy": "35.5452836784",
         "mlevel": "6",
         "modifiedtime": "20250703150422",
         "sigungucode": "2",
         "tel": "",
         "title": "태화강동굴피아",
         "zipcode": "44625",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EX",
         "lclsSystm2": "EX07",
         "lclsSystm3": "EX070200"
      },
      {
         "addr1": "울산광역시 남구 장생포고래로 244",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020800",
         "contentid": "769495",
         "contenttypeid": "12",
         "createdtime": "20090723195454",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/95/3072895_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/95/3072895_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3808541361",
         "mapy": "35.5028149271",
         "mlevel": "6",
         "modifiedtime": "20250703145641",
         "sigungucode": "2",
         "tel": "",
         "title": "장생포 고래바다여행선",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EX",
         "lclsSystm2": "EX07",
         "lclsSystm3": "EX070100"
      },
      {
         "addr1": "울산광역시 남구 신정동",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0207",
         "cat3": "A02070200",
         "contentid": "2986930",
         "contenttypeid": "15",
         "createdtime": "20230428172642",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/70/3499070_image2_1.png",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/70/3499070_image3_1.png",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3062231889",
         "mapy": "35.5505442683",
         "mlevel": "6",
         "modifiedtime": "20250630172032",
         "sigungucode": "2",
         "tel": "052-229-2723<br>052-276-8590",
         "title": "울산공업축제",
         "zipcode": "44739",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EV",
         "lclsSystm2": "EV01",
         "lclsSystm3": "EV010600"
      },
      {
         "addr1": "울산광역시 남구 장생포고래로 211",
         "addr2": "",
         "areacode": "7",
         "cat1": "B02",
         "cat2": "B0201",
         "cat3": "B02010100",
         "contentid": "2708665",
         "contenttypeid": "32",
         "createdtime": "20210310005401",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/69/2709169_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/69/2709169_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3773294441",
         "mapy": "35.5028009736",
         "mlevel": "",
         "modifiedtime": "20250626112930",
         "sigungucode": "2",
         "tel": "0503-5052-0693",
         "title": "브라운도트호텔 (장생포점)",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "AC",
         "lclsSystm2": "AC01",
         "lclsSystm3": "AC010100"
      },
      {
         "addr1": "울산광역시 남구 장생포동",
         "addr2": "",
         "areacode": "7",
         "cat1": "A01",
         "cat2": "A0102",
         "cat3": "A01020100",
         "contentid": "1624135",
         "contenttypeid": "12",
         "createdtime": "20120508010217",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/01/3072901_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/01/3072901_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3876451745",
         "mapy": "35.5041121316",
         "mlevel": "6",
         "modifiedtime": "20250611180209",
         "sigungucode": "2",
         "tel": "",
         "title": "울산 귀신고래 회유해면",
         "zipcode": "",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "NA",
         "lclsSystm2": "NA03",
         "lclsSystm3": "NA030200"
      },
      {
         "addr1": "울산광역시 남구 신두왕로 327 (옥동)",
         "addr2": "갈현마을회관~미골공원 (테크노산업단지)",
         "areacode": "7",
         "cat1": "A01",
         "cat2": "A0101",
         "cat3": "A01010500",
         "contentid": "3016047",
         "contenttypeid": "12",
         "createdtime": "20230925142120",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/3016016_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/16/3016016_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.2884977114",
         "mapy": "35.5237663902",
         "mlevel": "6",
         "modifiedtime": "20250611175452",
         "sigungucode": "2",
         "tel": "",
         "title": "두왕 메타세쿼이아길",
         "zipcode": "44776",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "NA",
         "lclsSystm2": "NA05",
         "lclsSystm3": "NA050100"
      },
      {
         "addr1": "울산광역시 남구 무거동",
         "addr2": "(무거동)",
         "areacode": "7",
         "cat1": "A01",
         "cat2": "A0101",
         "cat3": "A01011800",
         "contentid": "128201",
         "contenttypeid": "12",
         "createdtime": "20041014090000",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/21/3008621_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/21/3008621_image3_1.jpg",
         "cpyrhtDivCd": "Type1",
         "mapx": "129.2873637765",
         "mapy": "35.5486691244",
         "mlevel": "6",
         "modifiedtime": "20250611171628",
         "sigungucode": "2",
         "tel": "",
         "title": "태화강",
         "zipcode": "44621",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "NA",
         "lclsSystm2": "NA02",
         "lclsSystm3": "NA020100"
      },
      {
         "addr1": "울산광역시 남구 황성동 668-1",
         "addr2": "",
         "areacode": "7",
         "cat1": "A01",
         "cat2": "A0102",
         "cat3": "A01020200",
         "contentid": "128190",
         "contenttypeid": "12",
         "createdtime": "20041013090000",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/11/3072911_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/11/3072911_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3492190070",
         "mapy": "35.4671988875",
         "mlevel": "6",
         "modifiedtime": "20250610164951",
         "sigungucode": "2",
         "tel": "",
         "title": "처용암",
         "zipcode": "44784",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "NA",
         "lclsSystm2": "NA03",
         "lclsSystm3": "NA030300"
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
         "addr1": "울산광역시 남구 선암호수길 104",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020700",
         "contentid": "1824216",
         "contenttypeid": "12",
         "createdtime": "20130628015950",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/21/3495121_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/21/3495121_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3260724005",
         "mapy": "35.5170400753",
         "mlevel": "6",
         "modifiedtime": "20250604104100",
         "sigungucode": "2",
         "tel": "",
         "title": "선암호수공원",
         "zipcode": "44772",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE03",
         "lclsSystm3": "VE030500"
      },
      {
         "addr1": "울산광역시 울주군 삼남읍 울산역로 255",
         "addr2": "UECO(울산전시컨벤션센터)",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0207",
         "cat3": "A02070200",
         "contentid": "1951053",
         "contenttypeid": "15",
         "createdtime": "20140924182921",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/69/3494369_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/69/3494369_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.1316827314",
         "mapy": "35.5556598644",
         "mlevel": "6",
         "modifiedtime": "20250604102757",
         "sigungucode": "5",
         "tel": "052-229-5331",
         "title": "울산119안전문화축제",
         "zipcode": "44951",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EV",
         "lclsSystm2": "EV01",
         "lclsSystm3": "EV010200"
      },
      {
         "addr1": "울산광역시 남구 장생포고래로 271-1 (매암동)",
         "addr2": "장생포 고래문화마을 일원",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0207",
         "cat3": "A02070200",
         "contentid": "3491764",
         "contenttypeid": "15",
         "createdtime": "20250519165304",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/60/3491760_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/60/3491760_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3831260722",
         "mapy": "35.5059562836",
         "mlevel": "6",
         "modifiedtime": "20250520093233",
         "sigungucode": "2",
         "tel": "052-256-6301~2",
         "title": "장생포 수국 페스티벌",
         "zipcode": "44780",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EV",
         "lclsSystm2": "EV01",
         "lclsSystm3": "EV010500"
      },
      {
         "addr1": "울산광역시 남구 신정동",
         "addr2": "1513 울산광역시 태화강 남구둔치",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0207",
         "cat3": "A02070200",
         "contentid": "3394865",
         "contenttypeid": "15",
         "createdtime": "20241022141242",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/11/3491411_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/11/3491411_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.3076647311",
         "mapy": "35.5504859689",
         "mlevel": "6",
         "modifiedtime": "20250516151551",
         "sigungucode": "2",
         "tel": "052-220-0613",
         "title": "울산축협 한우축제",
         "zipcode": "44658",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "EV",
         "lclsSystm2": "EV01",
         "lclsSystm3": "EV010600"
      },
      {
         "addr1": "울산광역시 남구 대공원로 94 (옥동)",
         "addr2": "",
         "areacode": "7",
         "cat1": "A02",
         "cat2": "A0202",
         "cat3": "A02020600",
         "contentid": "127644",
         "contenttypeid": "12",
         "createdtime": "20070920090000",
         "firstimage": "http://tong.visitkorea.or.kr/cms/resource/22/3072322_image2_1.jpg",
         "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/22/3072322_image3_1.jpg",
         "cpyrhtDivCd": "Type3",
         "mapx": "129.2935470479",
         "mapy": "35.5316989268",
         "mlevel": "6",
         "modifiedtime": "20250430135423",
         "sigungucode": "2",
         "tel": "",
         "title": "울산대공원",
         "zipcode": "44660",
         "lDongRegnCd": "31",
         "lDongSignguCd": "140",
         "lclsSystm1": "VE",
         "lclsSystm2": "VE02",
         "lclsSystm3": "VE020100"
      }
   ]
}
    )



    # import json
    # features = Image_comparison.extract_features(
    #     "http://tong.visitkorea.or.kr/cms/resource/21/3497121_image3_1.jpg"
    # )
    # features1 = Image_comparison.extract_features(
    #     "http://tong.visitkorea.or.kr/cms/resource/88/3082988_image2_1.jpg"
    # )
    # print(
    #     Image_comparison.cosine_similarity(
    #         features, features1
    #     )
    # )
    # print(
    #     json.dumps(
    #         features.tolist(),
    #         indent=3
    #     ),
    #     len(features)
    # )
