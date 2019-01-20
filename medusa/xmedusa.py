#! /usr/bin/env python3

###############################################################################
import asyncio
import random


async def mainCoroutineSimple():
    print('Simple coroutine')


async def mainCoroutineFancy(id):
    process_time  = random.randint(1,5)
    await asyncio.sleep(process_time)
    print(f"Fancy coroutine: {id} done after {process_time} seconds.")


async def mainCoroutineMarvelous():
    print('Marvelous coroutine')


async def main():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(mainCoroutineFancy(i)))

    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()


##
#
