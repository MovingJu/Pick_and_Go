import modules
import asyncio
import numpy
from modules import Picked_sigungu

if __name__ == "__main__":
    async def main():
        test = await Picked_sigungu.create()
        data = await test.get_related()
        data=data['items']

        X=[]

        for i in data:
            iteration_list=[]
            iteration_list.append(i['contentid'])
            iteration_list.append(i['title'])
            iteration_list.append(i['lclsSystm3'])
            
            X.append(iteration_list)

        print(X)

    import asyncio  
    asyncio.run(main())