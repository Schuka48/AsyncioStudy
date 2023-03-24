import logging

import aiohttp
import asyncio
from aiohttp_socks import SocksConnector

from utilies.delay_functions import async_timed
from chapter_04 import fetch_status


@async_timed()
async def main():
    # session_timeout = aiohttp.ClientTimeout(total=1)
    proxy_url = 'http://keisy:1YdvAo%40I@10.33.102.102:50000'
    async with aiohttp.ClientSession(connector=SocksConnector.from_url(proxy_url)) as session:
        url = 'https://www.example.com'
        pending = [asyncio.create_task(fetch_status(session, url)),
                   asyncio.create_task(fetch_status(session, url)),
                   asyncio.create_task(fetch_status(session, url))]
        while pending:
            done, pending = await asyncio.wait(pending,
                                               return_when=asyncio.FIRST_COMPLETED)
            print(f'Число завершившихся задач: {len(done)}')
            print(f'Число ожидающих задач: {len(pending)}')

            for done_task in done:
                print(await done_task)


asyncio.run(main())
