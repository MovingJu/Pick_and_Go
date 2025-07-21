import modules
import aiomysql


class Setup:
    """
    # 사용할 때
    ```python
    Instance = await Setup.create()
    ```
    로 사용하고, 반드시
    ```python
    await Instance.close()
    ```
    하세요.

    # 주의사항
      await 키워드 잘 붙이세요.
      유저한테 절대 sql 쿼리 받아서 쓰지 마세요.
    """

    def __init__(self, conn):
        self.conn = conn

    @classmethod
    async def create(cls):
        conn = await modules.get_connection()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(modules.schema.DB_TABLE_SETUP_QUERY)
        return cls(conn)

    async def close(self):
        self.conn.close()

    async def create_table(self, table_name: str, **columns: str):
        """
        How to use:
        ```python
        await Instance.create_table(Table_name, Column_name="INT Not Null ...")
        ```
        """
        if not columns:
            raise ValueError("At least one column must be specified.")

        columns_def = ", ".join(f"{name} {datatype}" for name, datatype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_def})"

        async with self.conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query)

class Manage(Setup):
    pass
