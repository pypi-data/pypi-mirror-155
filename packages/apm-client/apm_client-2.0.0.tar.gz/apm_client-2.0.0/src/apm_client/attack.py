import asyncio
import time

import requests
import os


def attack(curl):
    sleep_time = 1 / (4000 / 60)
    os.system(curl)
    time.sleep(sleep_time)


async def main():
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None,
            attack,
            "curl 'http://localhost:8081/markets/' >/dev/null 2>&1"
        )
        for i in range(2000)
    ]
    for response in await asyncio.gather(*futures):
        pass

loop = asyncio.get_event_loop()
# rate = 9000
# sleep_time = 1 / (9000 / 60)
curl = "curl 'http://localhost:8081/markets/' > /dev/null 2>&1"
while True:
    loop.run_until_complete(main())
