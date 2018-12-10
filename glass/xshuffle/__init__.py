#!/usr/bin/env python3

import sys

# deck: list (required)
# rounds_to_shuffle: int (required, positive integer)
# round_callback: function called with (a, b) after each round/unit
#     of shuffling. Can be used for analysis or display of the
#     the shuffling process in detail for debugging or optimization
#     of the shuffling algorithm. (optional)
# returns [a, b]
#
# NOTE: It is possible for a to be the original deck and for b to be
# an empty list, in the case that rounds_to_shuffle == 0.
#
# NOTE: ** It is possible for a to be an empty list and for b to contain
# all of the cards (list items) from the original deck, in the order
# set by shuffling. ** This condition will occur depending on the
# number of cards in the deck and the value of rounds_to_shuffle.
#
# The most common result will be that both stacks of cards (lists)
# a, b will each contain a portion of the cards from the original
# deck. In other words, for a given number of cards in the original
# deck, there will be relatively fewer possible values of
# rounds_to_shuffle which will result in all of the cards being in
# deck b when shuffle() completes all requested rounds.
#
# IT IS IMPLICIT THAT A "START OVER" OR "CIRCULAR" CONVENTION
# IS REQUIRED. What should be done when the value of
# rounds_to_shuffle is high enough such that all the cards end up in
# card stack b.
# The most obvious convention is that if there are any more rounds
# required to reach the requested rounds_to_shuffle, then the card
# stack (list) b will be come a and b will be made empty and 
# shuffling will then continue. This 'starting over' will be repeated
# as many times as nevessary to perform rounds_to_shuffle rounds
# or units of shuffling. 
#
def shuffle(deck, rounds_to_shuffle, round_callback):
    """Shuffle deck of cards"""
    if (type(rounds_to_shuffle) is not int
        or rounds_to_shuffle < 0):
            sys.exit('rounds_to_shuffle must be a postitive integer.')
    if (rounds_to_shuffle == 0 or len(deck) == 0):
        return [deck, []]
    a = deck
    b = []
    round = 1
    while (round <= rounds_to_shuffle):
        shuffle_one_round(a, b)
        round += 1
        round_callback(a, b)
    return [a, b]

# shuffle_one_round(a, b)
# a: list
# b: list
# returns [a, b]
#
# The steps required for one round (or unit) of shuffling have
# been separated out into this function for clarity and to
# facilitate the possible usage of different shuffling code to
# implement different algorithms or do implement them in different
# ways or with different instrumentation, etc.
#
# For efficiency sake, we want to pass the lists a and b by
# reference here. Since these are mutable objects, they will
# pass into shuffle_one_round by reference and the original
# objects will be modified, such as not to create an unnecessary
# copy of them.
# 
def shuffle_one_round(a, b):
    """Shuffle one round"""
    
    card_from_top_of_a = a.pop(0)
    b.insert(0, card_from_top_of_a)  # Added to top of b
    # Optimized:
    # b.insert(0, a.pop(0))  # top of a to top of b

    card_from_top_of_a = a.pop(0)
    a.append(card_from_top_of_a)  # Added to bottom of a
    # Optimized:
    # a.append(a.pop(0))  # top of a to bottom of a

    return

if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
            "not executed directly.")
