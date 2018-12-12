#! /usr/bin/env python3

# A card deck consisting of the alphabet in all capital letters
# is a good one for test/demo purposes.
# string.ascii_uppercase.split() provides this.
import string

import xshuffle

xshuffle.set_verbose(True)

deck_of_four_ascii_art_cards = [
    '###',
    '-##',
    '--#',
    '---'
]

deck_of_five_ascii_art_cards = [
    '####',
    '-###',
    '--##',
    '---#',
    '----'
]

deck_of_eight_ascii_art_cards = [
    '#######',
    '-######',
    '--#####',
    '---####',
    '----###',
    '-----##',
    '------#',
    '-------'
]

# Integers 1 through 8 in ascending order
# The card on the TOP of the deck is 1
deck_of_numeric_cards = range(1, 8)

# The alphabet. A through Z in order, in uppercase Ascii
# The card on the TOP of the deck is 'A'
deck_of_alphabetic_cards = string.ascii_uppercase.split()

shuffled_deck = xshuffle.shuffle(deck_of_eight_ascii_art_cards, 1)
xshuffle.show_stack(shuffled_deck, "\nRETURNED:")

