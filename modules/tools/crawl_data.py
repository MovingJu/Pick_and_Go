import httpx, asyncio, pandas as pd
import modules

async def get_data():
    
    db = await modules.Manage.create()
    sigungu = await db.read_table("sigungu_sigungu", "parent_city_id", "city_id")
    await db.close()
    
    print(sigungu)
    
    return 

asyncio.run(get_data())