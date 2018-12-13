#! /usr/bin/env python3

import xshuffle
import json  # For comparison of hypothetical complex (nested dict) cards

VERBOSE = True
# Set 'VERBOSE' to True to see verbose output from the 
# xshuffle module as it operates.
# This may also enable some additional output from THIS test script.
if VERBOSE:
    xshuffle.set_verbose(True)


############################## TEST & DEMO SUITE ###############################


# If desired, specific tests can be disabled by commenting them out here.
# This function is called at the very end of this file.
# See code comments near the function for each demo/test for details.
def run_demos_and_tests():
    #test_six_card_deck_twentyfive_optim_notoptim()  # PASS
    #test_seven_card_deck_twentyfive_optim_notoptim()  # TODO: FIX: TEST/ALGORITHM FAILS
    test_eight_card_deck_fortythree_optim_notoptim()  # PASS
    #demo_three_card_deck_asciiart_twenty()  # (demo, not a test)
    #demo_five_card_deck_asciiart_twenty()  # (demo, not a test)
    #demo_six_card_deck_asciiart_twentyfour()  # (demo, not a test)
    #demo_eight_card_deck_asciiart_thirtytwo()  # (demo, not a test)
    #test_fifty_two_card_deck_numerical_once()  # PASS

# TODO: Add test cases which deliberately pass invalid arguments to the
# xshuffle module. There is robust argument validation in the module, but
# we are not currently testing it. Argument validation failures will raise
# an exception so these tests cause errors by design.
# There are probably 5 or 6 such argument/input validation tests needed.
# Our tests so far look for correctly returned values and implicitly,
# error-free operation. However, these tests would be looking for specific errors.


########################### INDIVIDUAL TESTS & DEMOS ###########################

# TEST CASE: six_card_deck_twentyfive_optim_notoptim
# This test compares the results when optimization is off with the results
# when optimization is on. The deck state should be the same, although the
# effective rounds of shuffling used may differ.
#
# OBSERVATION: restoration_interval is 6
#
def test_six_card_deck_twentyfive_optim_notoptim():
    six_card_deck = ['A', 'B', 'C', 'D', 'E', 'F']
    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    shuffled_deck_notoptim = xshuffle.shuffle(six_card_deck, 25)
    comparable_deck_notoptim = '-'.join(shuffled_deck_notoptim)
    # Turn optimization on
    xshuffle.set_optimized_shuffling(True)
    shuffled_deck_optim = xshuffle.shuffle(six_card_deck, 25)
    comparable_deck_optim = '-'.join(shuffled_deck_optim)

    assert comparable_deck_optim == comparable_deck_notoptim, \
        'six_card_deck_twentyfive_optim_notoptim test failed. ' \
            'non-optimized vs. optimized operation should have ' \
            'returned identical decks, but they were different.'

    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: seven_card_deck_twentyfive_optim_notoptim
# This test compares the results when optimization is off with the results
# when optimization is on. The deck state should be the same, although the
# effective rounds of shuffling used may differ.
#
# TODO - FIX ALGORITHM: OPTIMIZATION DOES NOT WORK FOR 7 CARDS
# OBSERVATION: restoration_interval is 5
# ALGORITHM INCORRECT: restoration_interval calculated as 7
#
def test_seven_card_deck_twentyfive_optim_notoptim():
    seven_card_deck = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    shuffled_deck_notoptim = xshuffle.shuffle(seven_card_deck, 25)
    comparable_deck_notoptim = '-'.join(shuffled_deck_notoptim)
    # Turn optimization on
    xshuffle.set_optimized_shuffling(True)
    shuffled_deck_optim = xshuffle.shuffle(seven_card_deck, 25)
    comparable_deck_optim = '-'.join(shuffled_deck_optim)

    assert comparable_deck_optim == comparable_deck_notoptim, \
        'seven_card_deck_twentyfive_optim_notoptim test failed. ' \
            'non-optimized vs. optimized operation should have ' \
            'returned identical decks, but they were different.'

    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: eight_card_deck_fortythree_optim_notoptim
# This test compares the results when optimization is off with the results
# when optimization is on. The deck state should be the same, although the
# effective rounds of shuffling used may differ.
#
# OBSERVATION: restoration_interval is 4
#
def test_eight_card_deck_fortythree_optim_notoptim():
    eight_card_deck = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'E']
    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    shuffled_deck_notoptim = xshuffle.shuffle(eight_card_deck, 43)
    comparable_deck_notoptim = '-'.join(shuffled_deck_notoptim)
    # Turn optimization on
    xshuffle.set_optimized_shuffling(True)
    shuffled_deck_optim = xshuffle.shuffle(eight_card_deck, 43)
    comparable_deck_optim = '-'.join(shuffled_deck_optim)

    assert comparable_deck_optim == comparable_deck_notoptim, \
        'eight_card_deck_fortythree_optim_notoptim test failed. ' \
            'non-optimized vs. optimized operation should have ' \
            'returned identical decks, but they were different.'

    # Ensure optimization is off
    xshuffle.set_optimized_shuffling(False)
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: (DEMO) three_card_deck_asciiart_twenty
# Put the xshuffle module in verbose mode to display all activity and use a
# graphical (ascii-art) deck of three cards which makes it easy to see what is
# happening to the cards upon each round of shuffling. This makes it easy to
# see when the deck is shuffled back to its original state and on what
# intervals this occurs, depending on the number of cards (even or odd etc.)
#
# OBSERVATION: restoration_interval is 3 (the number of cards)
#
def demo_three_card_deck_asciiart_twenty():
    print("\nRUNNING DEMO: demo_three_card_deck_asciiart_twenty")
    deck_of_three_ascii_art_cards = [
        '##',
        '-#',
        '--'
    ]

    # Demo tests like this set the xshuffle module verbosity on temporarily
    xshuffle.set_verbose(True)
    shuffled_deck = xshuffle.shuffle(deck_of_three_ascii_art_cards, 20)
    if not VERBOSE:  # Restore the VERBOSITY setting of the test file
        xshuffle.set_verbose(False)

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: (DEMO) five_card_deck_asciiart_twenty
#
# OBSERVATION: restoration_interval is 5 (the number of cards)
#
def demo_five_card_deck_asciiart_twenty():
    print("\nRUNNING DEMO: demo_five_card_deck_asciiart_twenty")
    deck_of_five_ascii_art_cards = [
        '####',
        '-###',
        '--##',
        '---#',
        '----'
    ]

    # Demo tests like this set the xshuffle module verbosity on temporarily
    xshuffle.set_verbose(True)
    shuffled_deck = xshuffle.shuffle(deck_of_five_ascii_art_cards, 20)
    if not VERBOSE:  # Restore the VERBOSITY setting of the test file
        xshuffle.set_verbose(False)

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: (DEMO) six_card_deck_asciiart_twentyfour
#
# OBSERVATION: restoration_interval is 6 (the number of cards)
#
def demo_six_card_deck_asciiart_twentyfour():
    print("\nRUNNING DEMO: demo_six_card_deck_asciiart_twentyfour")
    deck_of_six_ascii_art_cards = [
        '#####',
        '-####',
        '--###',
        '---##',
        '----#',
        '-----'
    ]

    # Demo tests like this set the xshuffle module verbosity on temporarily
    xshuffle.set_verbose(True)
    shuffled_deck = xshuffle.shuffle(deck_of_six_ascii_art_cards, 24)
    if not VERBOSE:  # Restore the VERBOSITY setting of the test file
        xshuffle.set_verbose(False)

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: (DEMO) eight_card_deck_asciiart_thirtytwo
# Put the xshuffle module in verbose mode to display all activity and use a
# graphical (ascii-art) deck of eight cards which makes it easy to see what is
# happening to the cards upon each round of shuffling. This makes it easy to
# see when the deck is shuffled back to its original state and on what
# intervals this occurs, depending on the number of cards (even or odd etc.)
def demo_eight_card_deck_asciiart_thirtytwo():
    print("\nRUNNING DEMO: demo_eight_card_deck_asciiart_thirtytwo")
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

    # Demo tests like this set the xshuffle module verbosity on temporarily
    xshuffle.set_verbose(True)
    shuffled_deck = xshuffle.shuffle(deck_of_eight_ascii_art_cards, 32)
    if not VERBOSE:  # Restore the VERBOSITY setting of the test file
        xshuffle.set_verbose(False)

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #


# TEST CASE: fifty_two_card_deck_numerical_once
# Does a typical deck of cards, shuffled one round, get shuffled to the known
# correct state for the xshuffle algorithm?

# This is a general purpose test which uses a deck of the same size as
# a standard playing card deck to see if the algorithm works in this
# general case. The known correct result was manually computed and verified
# for use here in this test.
# NOTE: It is not really necessary to have this many cards in such a test,
# but the concept of such a deck is recognizable to users so it logically
# fits into a test suite and this could very well be a typical usage of this
# module, in shuffling a standard playing card deck.
# Tangentially, this test also shows that numerical 'cards' are supported.
def test_fifty_two_card_deck_numerical_once():
    print("\nRUNNING TEST: test_fifty_two_card_deck_numerical_once")
    fifty_two_card_deck_numerical = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
        
    # This test only supports 1 round of shuffling.
    shuffled_deck = xshuffle.shuffle(fifty_two_card_deck_numerical, 1)

    known_correct_result_string = '40-8-24-48-32-16-52-44-36-28-' \
        '20-12-4-50-46-42-38-34-30-26-' \
        '22-18-14-10-6-2-51-49-47-45-' \
        '43-41-39-37-35-33-31-29-27-25-' \
        '23-21-19-17-15-13-11-9-7-5-3-1'

    assert ('-'.join(str(item) for item in shuffled_deck)
        == known_correct_result_string), \
        'fifty-two card deck numerical test failed ' \
            '(rounds used: 1)'  # This test only supports 1 round

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #

run_demos_and_tests()
