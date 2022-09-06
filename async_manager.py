import asyncio
import logging
import aiosqlite


async def main():
    logging.basicConfig(level=logging.INFO)
    # When using 'async with', the context manager will call __aenter__ and __aexit__
    async with (  # Python3.10 syntax: multiple 'with' statements
        aiosqlite.connect(":memory:") as db,
        db.execute("SELECT * FROM blogs") as cursor,
    ):
        await db.execute("CREATE TABLE blogs (name text, url text)")
        await db.execute(
            "INSERT INTO blogs (name, url) VALUES ('The Python Standard Library', 'https://docs.python.org/3/')"
        )
        logging.info(await cursor.fetchall())


if __name__ == "__main__":
    asyncio.run(main())
