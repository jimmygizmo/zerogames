#! /usr/bin/env python3

# https://www.youtube.com/watch?v=3mb9jFAHRfw
###############################################################################
import asyncio

# showing asyncio futures. callbacks, futures like this are messy!


def annie(when_frank_is_done_future):
    print('Anything you can do, I can do better.')
    print('    I can do anything better than you.')

    def defiance(_):
        print('Yes, I can!')

    when_frank_is_done_future.add_done_callback(defiance)


def frank(when_frank_is_done_future):
    print("No, you can't!")
    when_frank_is_done_future.set_result(None)


loop = asyncio.get_event_loop()
future = loop.create_future()
annie(future)
frank(future)

loop.run_until_complete(future)


##
#
