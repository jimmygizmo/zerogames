#! /usr/bin/env python3

import xshuffle
import json  # For comparison of hypothetical complex (nested dict) cards

VERBOSE = True
# Set 'VERBOSE' to True to see verbose output from the 
# xshuffle module as it operates.
# This may also enable some additional output from THIS test script.
if VERBOSE:
    xshuffle.set_verbose(True)

# Uncomment this line to perform shuffling using the round-optimized variant
# of the xshuffle algorithm, meaning the same shuffling results will be
# achieved, but via the minimum number of rounds of shuffling, thus avoiding
# unnecessary/redundant shuffling rounds.
# NOTE: All tests in this file should have the same results when performed
# both with and without optimization.
xshuffle.set_optimized_shuffling(True)


################################## TEST SUITE ##################################


# If desired, specific tests can be disabled by commenting them out here.
# This function is called at the very end of this file.
# See code comments near the function for each demo/test for details.
def run_demos_and_tests():
    demo_five_card_deck_asciiart_twenty()
    demo_eight_card_deck_asciiart_thirtytwo()
    test_fifty_two_card_deck_numerical_once()
    test_one_card_deck_complex()


#################################### TESTS #####################################


# TEST CASE: (DEMO) five_card_deck_asciiart_twenty
# Put the xshuffle module in verbose mode to display all activity and use a
# graphical (ascii-art) deck of five cards which makes it easy to see what is
# happening to the cards upon each round of shuffling. This makes it easy to
# see when the deck is shuffled back to its original state and on what
# intervals this occurs, depending on the number of cards (even or odd etc.)
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


# TEST CASE: test_one_card_deck_complex
# (Complex refers to the card being an object of any kind.)
# Verify correct handling of a one card deck. It should be returned, identical to
# the original deck, regardless of the valid rounds_to_shuffle argument used.
# Verify correct handling of cards of an arbitrary data type, in this case,
# a dictionary of card attributes as a graphical card game might use.
# These tests are repeated for a few different rounds_to_shuffle values (1, 2, 5)
def test_one_card_deck_complex():
    print("\nRUNNING TEST: test_one_card_deck_complex")
    complex_card = dict(
        card_title = 'Ace of Spades',
        card_image_files = dict(
            large = 'ace_of_spades_400px.png',
            small = 'ace_of_spades_150px.png'
            )
        )
    comparable_complex_card = json.dumps(complex_card, sort_keys=True)
    one_card_deck = [ complex_card ]

    round_vals_to_try = [1, 2, 5]
    for rounds_to_shuffle in round_vals_to_try:
        shuffled_deck = xshuffle.shuffle(one_card_deck, rounds_to_shuffle)

        assert len(shuffled_deck) == 1, \
            f"one card deck shuffle returned a deck with {len(shuffled_deck)} " \
                f"cards in it. (rounds used: {rounds_to_shuffle})"

        card_in_shuffled_deck = shuffled_deck.pop()
        comparable_card = json.dumps(card_in_shuffled_deck, sort_keys=True)

        assert comparable_card == comparable_complex_card, \
            f"one card deck shuffle returned a complex card which had " \
                f"some difference in it. (rounds used: {rounds_to_shuffle})"

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


# ---------------------------------------------------------------------------- #

run_demos_and_tests()
