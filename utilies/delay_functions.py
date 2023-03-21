import asyncio


async def delay(time: int) -> None:
    print('Start sleep for %s seconds' % time)
    await asyncio.sleep(time)
    print('Finished sleep for %s seconds' % time)
