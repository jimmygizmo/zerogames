#!/usr/bin/env python3

import sys

verbose = False
optimize_algorithm = False


def set_verbose(verbose_on=True):
    # For a simple module/program, limited use of global variables
    # in this manner for module runtime configuration is fine.
    global verbose
    if verbose_on:
        verbose = True
    else:
        verbose = False


def set_optimized_shuffling(optimize_on=True):
    global optimize_algorithm
    if optimize_on:
        optimize_algorithm = True
    else:
        optimize_algorithm = False


def show_stack(stack, description):
    print(description)
    [ print(card) for card in stack ]


def shuffle(deck, rounds_to_shuffle):
    """Shuffle a deck of cards. The deck argument can be a list of any 
    type of object, representing the cards. The deck will be shuffled 
    rounds_to_shuffle times. One round exhausts all cards in the 
    supplied deck as defined in shuffle_one_round()."""
    if (type(rounds_to_shuffle) is not int
        or rounds_to_shuffle < 0):
            raise ValueError('rounds_to_shuffle argument must be a'
                'postitive integer.')
    if (type(deck) is not list):
            raise TypeError('deck must be a list.')
    if (rounds_to_shuffle == 0 or len(deck) == 0):  # Allowed
        return deck
    
    effective_rounds = rounds_to_shuffle
    if optimize_algorithm:
        number_of_cards = len(deck)
        effective_rounds = optimze_rounds(number_of_cards, rounds_to_shuffle)
        if verbose:
            print('ALGORITHM OPTIMISATION IS ON')
            print('The actual (effective) rounds_to_shuffle which will be '
                'used will be the minimum possible number of rounds required '
                'to achieve the exact same deck state as the requested number '
                'of rounds would achieve.')
            print(f"Requested rounds_to_shuffle: {rounds_to_shuffle}")
            print(f"Effective rounds to be used: {effective_rounds}")

    if verbose:
        print(f"\nShuffling deck with {len(deck)} cards, "
            f"{effective_rounds} rounds.")
    
    a = deck.copy()  # This list.copy() is necessary, otherwise we can have
    # a chain of references into the callee and internal manipulations
    # inside xshuffle can result in the passed/original deck argument
    # variable being modified. We deliberately use references a lot
    # in this module to conserve resources, but this requires some extra
    # care as this now-fixed bug illustrated.
    # This was a difficult bug to identify since it only showed up when
    # tests reused the original deck variable and then only when there
    # were greater than one rounds used prior to the reuse of the variable.
    # The bug is caused by using a = deck, instead of a = deck.copy().

    # * IMPORTANT POSSIBLE OPTIMIZATION DESCRIBED HERE *
    # NOTE that we use references to the deck/stacks heavily from here on
    # because this minimizes copying of data. Specifically, the inner
    # functions of shuffle_one_round() and perform_shuffle_unit() operate
    # on references to a and b. The names start_stack and end_stack are
    # used because for a few reasons. The names a and b refer to 'decks'
    # containing all of their cards (regardless of shuffle) but inside
    # these inner functions, cards are being moved, so these are stacks,
    # not decks. Also, there is an important optimization theoretically
    # possible, which might be able to eliminate the a = b.copy() step.
    # The concept is to swap positions of a, b on alternating calls to
    # the inner functions. This can be done by detecting which deck
    # has cards and which does not and then calling like this:
    # shuffle_one_round(the_deck_with_cards, the_the empty_deck).
    # The effect will be to alternate positions (a, b) and (b, a) in
    # the calls, which could eliminate the a=b.copy() and b = [] steps.
    # The effect of such an optimization would be reduced memory and cpu
    # usage.

    b = []
    round = 1
    if verbose:
        show_stack(a, "\nORIGINAL:")
    
    while (round <= effective_rounds):
        shuffle_one_round(a, b)
        if verbose:
            show_stack(b, f"\nROUND: {round}")
        # TODO: Look for a way to eliminate this need for list.copy()
        a = b.copy()  #  Move stack b to stack a position
        b = []  # Stack b is now empty
        # We cannot simply say a = b above here, as this just copies
        # the reference which immediately thereafter is reset
        # to []. Hence we use list.copy(). It would be desireable
        # to eliminate this need to copy through some optimization,
        # especially since it occurs once per round.
        # POSSIBLE OPTIMIZATION THEORIZED (DISCUSSED ABOVE ALSO):
        # 1. Check len(a) vs len(b) and call one of the following
        #     with the stack containing cards in the first position:
        #     shuffle_one_round(a, b)
        #     shuffle_one_round(b, a)
        # As an important step to avoid confusion, rename vars in
        # the called subs to:
        # a -> start_stack
        # b -> end_stack
        round += 1
    
    return a


def shuffle_one_round(start_stack, end_stack):
    """Shuffle one round, meaning perform as many 'shuffle units' as 
    necessary to exhaust all original cards in start_stack with all 
    cards ending up in end_stack."""
    while (len(start_stack) > 0):
        perform_shuffle_unit(start_stack, end_stack)
    return


def perform_shuffle_unit(start_stack, end_stack):
    """Perform one 'shuffle unit' upon the card stacks start_stack and end_stack. 
    The 'shuffle unit' is the smallest unique set of steps which are
    repeated upon cards being shuffled. Starting with all cards in
    start_stack and no cards in end_stack, the specific steps are:
    1. Move the card from the top of start_stack to the top of end_stack.
    2. Move the card from the bottom of start_stack to the top of start_stack.
    """
    
    card_from_top_of_start_stack = start_stack.pop(0)
    end_stack.insert(0, card_from_top_of_start_stack)
    # Optimized:
    # end_stack.insert(0, start_stack.pop(0))
    
    # If one card is left then this step will have no effect and
    # we just return for efficiency sake. If there are no cards left
    # then there is nothing to do and pop() would error so we return.
    if (len(start_stack) < 2):
        return
    else:
        card_from_top_of_start_stack = start_stack.pop(0)
        start_stack.append(card_from_top_of_start_stack)
        # Optimized:
        # start_stack.append(start_stack.pop(0))

    return


def optimze_rounds(number_of_cards, rounds_to_shuffle):
    # NOT YET IMPLEMENTED
    # TODO: Issue warning if no optimization was possible
    return rounds_to_shuffle


if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
            "not executed directly.")
