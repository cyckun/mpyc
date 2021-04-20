# create on 20210414 to test asyncio

import threading
import asyncio


async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    await asyncio.sleep(10)
    print('Hello again! (%s)' % threading.currentThread())

if __name__ == '__main__':
    """
    loop = asyncio.get_event_loop()
    tasks = [hello() for i in range(10*10)]
    loop.run_until_complete(asyncio.wait(tasks))
    print("end loop")
    loop.close()
    """
    n = 1
    m = 2
    shares = [[None] * n for _ in range(m)]
    print('share:', shares)