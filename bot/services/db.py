import psycopg
import asyncio

async def wait_db():
    while True:
        try:
            conn = await psycopg.AsyncConnection.connect(
                host="db",
                dbname="bot_db",
                user="appuser",
                password="pass123"
            )
            await conn.close()
            break
        except Exception:
            await asyncio.sleep(2)

async def execute(sql):
    async with await psycopg.AsyncConnection.connect(
        host="db",
        dbname="bot_db",
        user="appuser",
        password="pass123"
    ) as conn:

        async with conn.cursor() as cur:
            await cur.execute(sql)
            r = await cur.fetchone()

            if not r or r[0] is None:
                return 0

            return r[0]