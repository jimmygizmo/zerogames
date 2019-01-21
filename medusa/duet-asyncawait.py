#! /usr/bin/env python3

# https://www.youtube.com/watch?v=3mb9jFAHRfw
###############################################################################
import asyncio

# showing asyncio async await


async def annie():
    print('Anything you can do, I can do better.')
    print('    I can do anything better than you.')
    await frank()
    print('Yes, I can!')
    await frank()
    print('Yes, I can!')
    await frank()
    print('Yes, I ca. Yes, I can!')


async def frank():
    print("No, you can't!")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.ensure_future(annie()))


##
#
