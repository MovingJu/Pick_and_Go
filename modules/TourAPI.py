from urllib.parse import urlencode
import asyncio, httpx, os, dotenv

dotenv.load_dotenv()

class Url:
    """
    Url 조작을 위한 클래스. 별로 쓸 필요는 없음. 클린한 코드를 지향하는 당신 츄라이츄라이.
    """
    def __init__(self, service_type: str, **params) -> None:
        """
        - service_type : 사용하는 서비스 이름 적기
        - params : 쿼리 적는곳 
        
        # 필요한 쿼리들
        - numOfRows
        - pageNo
        - 기타 서비스 필수 코드
        """
        self.base_url = "http://apis.data.go.kr/B551011/KorService2"
        self.service_key: str = os.getenv("TOUR_API_KEY") or ""
        self.service_type = service_type
        self.params = {
            "serviceKey" : self.service_key,
            "numOfRows" : 10,
            "pageNo" : 1,
            "MobileOS" : "ETC",
            "MobileApp" : "PIGO",
            "_type" : "json"
        }
        for key, val in params.items():
            self.params[key] = val

    def __str__(self):
        query = urlencode(self.params)
        return f"{self.base_url}/{self.service_type}?{query}"
    
    def set_params(self, **params: str):
        for key, val in params.items():
            self.params[key] = val

    def change_serviceKey(self):
        newKey = os.getenv("TOUR_API_KEY_DECODING") or ""
        if((not newKey) or (self.service_key == newKey)):
            raise ValueError("서비스 키가 잘못됨. 둘다 안되는듯")
        self.service_key = newKey
        self.params["serviceKey"] = newKey

class TourAPI:
    """
    TourAPI에 정보 조회해주는 클래스
    불러와야하는 데이터가 많아지면 비동기 관리하기 힘들어서 만듦.
    동기로 처리하면 많이 느리니 웬만하면 써주세요.
    """
    def __init__(self, url: tuple[Url, ...]) -> None:
        self.url = url
        
    @classmethod
    async def create(cls, *url: Url):
        return cls(url)
    
    @staticmethod
    async def make_request(url: Url, client: httpx.AsyncClient):
        response = await client.get(url.__str__())
        return {"url": url.__str__(), "status": response.status_code, "data": response.json()}
    
    async def fetch(self):
        results = []
        async with httpx.AsyncClient() as client:
            for url in self.url:
                res = await TourAPI.make_request(url, client)
                results.append(res)
        return results

    async def fetch_async(self):
        async with httpx.AsyncClient() as client:
            tasks = [TourAPI.make_request(url, client) for url in self.url]
            results = await asyncio.gather(*tasks)
        return results
    
    async def fetch_url(self) -> dict[str, int | list]:
        results = await self.fetch_async()

        all_items = []
        total_count = -1

        for res in results:
            try:
                body = res["data"]["response"]["body"]
                items = body.get("items", {}).get("item", [])
                if isinstance(items, dict):  # 단일 item인 경우 리스트로
                    items = [items]
                all_items.extend(items)

                if total_count < body.get("totalCount"):
                    total_count = body.get("totalCount")
            except Exception as e:
                print(f"[WARN] 응답 파싱 실패: {res.get('url')}, error={e}")

        return {
            "totalCount": total_count,
            "items": all_items
        }

    async def fetch_url_not_async(self):
        results = await self.fetch()

        all_items = []
        total_count = -1

        for res in results:
            try:
                body = res["data"]["response"]["body"]
                items = body.get("items", {}).get("item", [])
                if isinstance(items, dict):  # 단일 item인 경우 리스트로
                    items = [items]
                all_items.extend(items)

                if total_count < body.get("totalCount"):
                    total_count = body.get("totalCount")
            except Exception as e:
                print(f"[WARN] 응답 파싱 실패: {res.get('url')}, error={e}")

        return {
            "totalCount": total_count,
            "items": all_items
        }


if __name__ == "__main__":

    from time import time

    async def main():
        st = time()
        t1 = await TourAPI.create(*(Url("areaBasedList2", numOfRows=5, pageNo=5, arrange="Q") for i in range(1, 8)))
        print(f"{await t1.fetch_url()}, time : {time() - st}")

        print("-"*10)

        st = time()
        t2 = await TourAPI.create(Url("ldongCode2", numOfRows=100))
        print(f"{await t2.fetch_url()}, time : {time() - st}")
    
    asyncio.run(main())
