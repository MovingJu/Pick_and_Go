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
    async def create(cls):
        db = await modules.Manage.create()

        locs = db.read_table("users", "locations")

        await db.close()
        return cls(locs)

    
class Related():
    pass