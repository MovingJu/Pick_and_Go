#### to do:::: user 가 선택한 위치 데이터베이스에서 받아오는 기능으로 수정.

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

        inter_table = {"-1": [1, ]}
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
            urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=self.total_loc[idx], pageNo=1, arrange="Q"))
            #urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=30, pageNo=1, arrange="Q"))
        tour = await modules.TourAPI.create(*urls)
        data = await tour.fetch_url()
        filtered_data={'totalCount':0, 'items':[]}

        for i in data['items']: # type: ignore
            if(i['lclsSystm2']=='AC04'): #모텔
                continue
            elif(i['lclsSystm2']=='AC01'): #호텔
                continue
            elif(i['lclsSystm2']=='FD03'): #피자햄버거등
                continue
            elif(i['lclsSystm2']=='AC03' or i['lclsSystm2']=='AC06'): #각종 작은 숙소들
                continue
            elif(i['lclsSystm2']=='FD02'): #식당
                continue
            elif(i['lclsSystm2']=='FD04'): #술집
                continue
            elif(i['lclsSystm3']=='AC020100'): #콘도 AC020100
                continue
            elif(i['lclsSystm3']=='NA020600'): #염전 NA020600
                continue
            elif(i['lclsSystm3']=='C0117000'): #맛코스 C0117000
                continue
            elif(i['lclsSystm3']=='VE060200'): #영화관 VE060200
                continue
            elif(i['lclsSystm3']=='VE090600'): #학교 VE090600
                continue
            elif(i['lclsSystm3']=='SH030100'): #대형마트 SH030100
                continue
            else:
                filtered_data['items'].append(i)
        
        filtered_data['totalCount']=len(filtered_data['items'])
        return filtered_data

if __name__ == "__main__":
    async def main():
        import json
        test = await Picked_sigungu.create()
        data = await test.get_related()
        print(
                data,
                len(data["items"])
            )


    import asyncio  
    asyncio.run(main())