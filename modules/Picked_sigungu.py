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
            # urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=self.total_loc[idx], pageNo=1, arrange="C"))
            urls.append(modules.Url("areaBasedList2", lDongRegnCd=loc[0], lDongSignguCd=loc[1], numOfRows=30, pageNo=1, arrange='C')) # 서버 부하 줄이기용
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
            elif(i['lclsSystm2']=='AC06'): #식당
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