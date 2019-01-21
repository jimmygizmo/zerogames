#! /usr/bin/env python3

###############################################################################
import asyncio
import random


async def mainCoroutineSimple():
    print('Simple coroutine')


async def spiderDrop(id, spiders):
    #print(f"spiders var type: {type(spiders)}")  # it is a list. ok good.
    print(f"id: {id}  spiders: {spiders}")
    spiders[id] = 0
    drop_step  = random.randint(1,5)
    spiders[id] = spiders[id] + drop_step
    print(f"spiderDrop: {id} dropped {drop_step} steps.")


async def mainCoroutineMarvelous():
    print('Marvelous coroutine')


async def main(spiders):
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(spiderDrop(i, spiders)))

    await asyncio.gather(*tasks)

spiders = []
loop = asyncio.get_event_loop()
loop.run_until_complete(main(spiders))
loop.close()

print(spiders)


##
#
