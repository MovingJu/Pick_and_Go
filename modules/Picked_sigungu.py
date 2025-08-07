#### to do:::: user 가 선택한 위치 데이터베이스에서 받아오는 기능으로 수정.

import modules

class Picked_sigungu():
    def __init__(self, locs: list[tuple[int, int]]) -> None:
        self.locs = locs
    
    async def get_total(self):
        urls = []
        for loc in self.locs:
            urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=1, pageNo=1))
        tour = await modules.TourAPI.create(*urls)
        data = await tour.fetch_async()

        self.total_loc = []
        for item in data:
            self.total_loc.append(item["data"]["response"]["body"]["totalCount"])
        return self.total_loc

    async def get_related(self):
        await self.get_total()
        urls = []
        for idx, loc in enumerate(self.locs):
            urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=self.total_loc[idx], pageNo=1, arrange="C"))
            #urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=30, pageNo=1, arrange='C')) # 서버 부하 줄이기용
        tour = await modules.TourAPI.create(*urls)
        data = await tour.fetch_url()
        
        return data

if __name__ == "__main__":
    async def main():
        # import json
        
        # data = await test.get_related()
        # data1 = json.dumps(data, indent=3)
        # print(
        #         data1,
        #         len(data["items"])
        #     )
        return

    import asyncio  
    asyncio.run(main())