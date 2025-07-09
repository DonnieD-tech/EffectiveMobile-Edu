from models.database import create_db
from services.parser import parse_excel_file
from services.urls import find_all_spimex_files
import time
import asyncio
import aiohttp


async def main():
    await create_db()

    start_time = time.perf_counter()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        semaphore = asyncio.Semaphore(10)

        async def limited_parse(url):
            async with semaphore:
                await parse_excel_file(url, session)

        urls = await find_all_spimex_files()
        parse_excel_file.cnt = 0

        tasks = [limited_parse(url) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f'Обработка завершена за {end_time - start_time:.2f} секунд')

if __name__ == '__main__':
    asyncio.run(main())