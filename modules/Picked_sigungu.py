#### to do:::: user 가 선택한 위치 데이터베이스에서 받아오는 기능으로 수정.

import pandas as pd
import modules

class Picked_sigungu():
    """
    # 사용할 때
    ```python
    Instance = await Picked_sigungu.create()
    ```
    로 사용하세요.
    """
    def __init__(self, locs) -> None:
        self.locs = locs

    @classmethod
    async def create(cls, userid: str = "-1"):
        # db = await modules.Manage.create()
        # locs = db.read_table("users", "locations")
        # await db.close()

        inter_table = {"-1": [1, 2, 3]}
        sigungu_table = {1: (31, 140), 2: (31, 170), 3: (31, 200)}

        loc_key = inter_table[userid]
        locs: list[tuple[int, int]] = []
        for val in loc_key:
            locs.append(sigungu_table[val])

        return cls(locs)
    
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
            urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=self.total_loc[idx], pageNo=1))
        tour = await modules.TourAPI.create(*urls)
        data = await tour.fetch_url()

        return data

if __name__ == "__main__":
    async def main():
        import json
        test = await Picked_sigungu.create()
        data = await test.get_related()
        data = json.dumps(data, indent=3, ensure_ascii=False)
        print(data)

    import asyncio  
    asyncio.run(main())