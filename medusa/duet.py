#! /usr/bin/env python3

# https://www.youtube.com/watch?v=3mb9jFAHRfw
###############################################################################

# annie() and frank() are generators.
# Generators yield their result to the caller, BUT they retain their state.
# They are actually bi-directional. You can send info in as well as get it out.


def annie():
    yield 'Anything you can do, I can do better.\n' \
          '    I can do anything better than you.'
    yield "Yes, I can."
    yield "Yes, I can."
    yield "Yes, I can. Yes, I can!"


def frank():
    yield "No, you can't."
    yield "No, you can't."
    yield "No, you can't."


queue = [annie(), frank()]
while queue:
    singer = queue.pop(0)
    try:
        print(next(singer))
        #print(next(singer.send(None)))  # Sending info into a generator
        queue.append(singer)
    except StopIteration:
        pass


##
#
