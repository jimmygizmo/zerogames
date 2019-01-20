#! /usr/bin/env python3

import sys
import math

verbose = False
optimize_algorithm = False


def set_verbose(verbose_on=True):
    """Turn verbose output on or off. Verbosity is off by
    default. If this function is called with no argument, it will
    turn verbosity on.
    
    Args: single argument (boolean)"""

    # For a simple module/program, limited use of global variables
    # in this manner for module runtime configuration is fine.
    global verbose
    if verbose_on:
        verbose = True
    else:
        verbose = False


def set_optimized_shuffling(optimize_on=True):
    """Turn shuffling optimization on or off. Optimization is off by
    default. If this function is called with no argument, it will
    turn optimization on.
    
    Args: single argument (boolean)"""

    global optimize_algorithm
    if optimize_on:
        optimize_algorithm = True
    else:
        optimize_algorithm = False


def show_stack(stack, description):
    """Prints out a stack of cards from top card to bottom card with
    a description printed above the stack. 'Stack' is more accurate
    here than 'deck' as this function may be used on partial decks
    during sorting.
    
    Args:
        stack (list):  a list of card objects of a printable type
        description (string):  a descriptive string to print
            above the printed stack."""

    print(description)
    [ print(card) for card in stack ]


def shuffle(deck, rounds_to_shuffle):
    """Shuffle a deck of cards. The deck argument can be a list of any 
    type of object, representing the cards. The deck will be shuffled 
    rounds_to_shuffle times. One round exhausts all cards in the 
    supplied deck as defined in shuffle_one_round().

    Args:
        deck (list): a list of card objects of any type
        rounds_to_shuffle (int): a positive integer indicating the
            number of rounds to shuffle. May be optimized to less
            rounds when optimization is on and possible."""

    if (type(rounds_to_shuffle) is not int
        or rounds_to_shuffle < 0):
            raise ValueError('rounds_to_shuffle argument must be a'
                'postitive integer.')

    if (type(deck) is not list):
            raise TypeError('deck must be a list.')

    # The follwoing arguments are allowed but will result in no operations
    # being performed or an identical deck being returned, not bad arguments
    # per se, but appropriate to simply return the unaltered deck right here.
    # In fact, a deck with one card is not supported by the current optimization
    # calculations (in addition to being irrelevant and having no efffect)
    # hence, to prevent the resulting error in optimization calculations, that is
    # in fact the strongest reason to return here for a deck with one card.
    if (rounds_to_shuffle == 0 or len(deck) == 0 or len(deck) == 1):
        return deck
    
    effective_rounds = rounds_to_shuffle  # Prior to any optimization
    if optimize_algorithm:
        number_of_cards = len(deck)
        if verbose:
            print("\nALGORITHM OPTIMIZATION IS ON")
            print('The actual (effective) rounds_to_shuffle which will be '
                'used will be the minimum possible number of rounds required '
                'to achieve the exact same deck state as the requested number '
                'of rounds would achieve.')
            
        effective_rounds = optimze_rounds(number_of_cards, rounds_to_shuffle)
        if verbose:
            print(f"Requested rounds_to_shuffle: {rounds_to_shuffle}")
            print(f"Effective rounds to be used: {effective_rounds}")

    if (effective_rounds == 0):
        print(f"Optimization has determined that the requested rounds_to_shuffle "
            " would return the deck to its original state. Returning the "
            " original deck. No shuffling performed.")
        return deck

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

    # * ANOTHER IMPORTANT POSSIBLE OPTIMIZATION DESCRIBED HERE *
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
        # TODO: The OPTIMIZATION described just above here is a possible
        # way to eliminate this list.copy().
        a = b.copy()  #  Move stack b to stack a position VIA COPY
        b = []  # Stack b is now empty
        # We cannot simply say a = b above here, as this just copies
        # the reference which immediately thereafter is reset
        # to []. Hence we use list.copy(). It would be desireable
        # to eliminate this need to copy through some optimization,
        # especially since it occurs once per round.
        # POSSIBLE OPTIMIZATION THEORIZED (DISCUSSED ABOVE ALSO):
        # 1. Check len(a) vs len(b) and call one of the following
        #     with the stack containing cards in the first position:
        #     shuffle_one_round(a, b) OR
        #     shuffle_one_round(b, a)
        # As an important step to avoid confusion, rename vars in
        # the called subs to:
        # a -> start_stack
        # b -> end_stack
        # * This renaming was done in preparation, but this particular
        # optimization has not yet been attempted/implemented.
        round += 1
    
    return a


def shuffle_one_round(start_stack, end_stack):
    """Shuffle one round, meaning perform as many 'shuffle units' as 
    necessary to exhaust all original cards in start_stack with all 
    cards ending up in end_stack. Note that in this case lists are
    passed by reference and this is very much by design to avoid
    unnecessary data replication. This behavior is automatic for
    mutable objects like lists. When this function concludes,
    no cards/items will remain in start_stack and all cards/items will
    be in the (one round) shuffled state in end_stack.
    
    Args:
        start_stack (list): the stack (or deck) with the cards in it
        end_stack (list): an empty stack/list which will receive
            all the cards during shuffling.
            
     Returns: Nothing. Operates on stacks/lists via reference."""

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

    Note that in this case lists are passed by reference and this is very much
    by design to avoid unnecessary data replication. This behavior is automatic for
    mutable objects like lists.

    Args:
        start_stack (list): a stack/list with at least one item/card in it
        end_stack (list): a stack/list which may or may not have any cards in it
            depending where we are in the shuffling process.
    
    Returns: Nothing. Operates on stacks/lists via reference."""
    
    end_stack.insert(0, start_stack.pop(0))
    
    # If one card is left then this step will have no effect and
    # we just return for efficiency sake. If there are no cards left
    # then there is nothing to do and pop() would error so we return.
    if (len(start_stack) < 2):
        return
    else:
        start_stack.append(start_stack.pop(0))

    return


# OPTIMIZATION OF SHUFFLING ROUNDS
#
# Because of the nature of the shuffling algorithim in xshuffle,
# generally speaking, the deck will be shuffled all the way back to
# its original state after a certain number of rounds, DEPENDING
# upon the number of cards in the deck and also DEPENDING on whether
# there is an odd or an even number of cards in the deck.
# We will call the shuffling round interval at which a deck with a
# given number of cards returns to its original state/order, the
# 'restoration_interval'.
#
# One can see that the states of the deck after each round are also
# identical as rounds progress, such that we can say, the state after
# round 1 will be identical to the state after restoration_interval + 1.
# The state of the deck is a repeating cycle, which is sort of intuitively
# obvious because our shuffling method uses a fixed set of steps where
# the same input always gives the same output.
#
# These facts give us the opportunity to avoid unnecessary rounds of shuffling.
# One can acheive the exact same state in a deck as would be acheived by
# repeat_cycles * restoration_interval + x
# as would be acheived by simply shuffling for x rounds.
# This is the optimization.
#
# ( NOTE: Testing has shown the following is not quite correct. See comments
#   near this calculation below in the function.)
# The other important consideration is how restoration_interval is determined.
# Through experimentation/observation or through mathematical reasoning,
# one discovers that there are two rules:
# 1. When the deck contains an EVEN number of cards,
#    The restoration_interval = one half of the number of cards
# 2. When the deck contains an ODD number of cards,
#    The restoration interval = the number of cards.
#
# Of course if the rounds_to_shuffle value is lower than the restoration_interval,
# then restoration will not be observed and no optimization is possible, which is
# why I qualified this description at the beginning with 'generally speaking.'
# 
# To implement the optimization, this function performs the needed calculations
# and adjusts rounds_to_shuffle to its minimum possible value to acheive the
# exact same stte of the card deck, avoiding unnecessary shufling rounds.
# The optimized value is reterned and used as 'effective_rounds'.
def optimze_rounds(number_of_cards, rounds_to_shuffle):
    """Calculate an optimized number of rounds to shuffle if possible and
    and return that number. NOTE: This algorithm is known to be broken for
    some/many (but not all) values of number_of_cards. The problem lies
    in the calculation of restoration_interval. The rest of the code here should
    work fine if a fix can be found for determining the correct restoration_interval
    for ALL values of number_of_cards.
    
    Args:
        number_of_cards (int): the number of cards in the original deck
        rounds_to_shuffle (int): a positive integer of the requested rounds
            to shuffle
            
    Returns: An optimized number of rounds to shuffle to acheive the exact
        same results (when possible.)"""
    
    # TODO: FIX: This is where the problem is with the current optimization.
    # These calculations of the restoration_interval work for many values
    # of number_of_cards, BUT NOT ALL, For example, the restoration_interval
    # for a deck of 7 cards is calculated here to be 7, but in fact it
    # is observed to be 5. It seems this part needs to be a bit more complex
    # than it currently is.
    if number_of_cards % 2 == 0:
        # Even number of cards
        restoration_interval = int(number_of_cards / 2)
    else:
        # Odd number of cards
        restoration_interval = number_of_cards
    if verbose:
        print(f"\nRestoration interval for this deck: {restoration_interval}")

    # We need to determine how many WHOLE restoration intervals fit into
    # the requested rounds_to_shuffle. This will be called 'repetitions'.
    repetitions = int(math.floor(rounds_to_shuffle / restoration_interval))
    if verbose:
        print(f"\nRepetittions seen in optimization analysis: {repetitions}")
    
    # potential_alst_restoraiton is the highest round number which will result
    # in the deck returning to its original state and by the nature of our
    # calculations, this will always be less than or equal to the value of
    # rounds_to_shuffle. We call it 'potential' because we wont actually do that
    # many rounds (or more, either) since we are optimizing.
    potential_last_restoration = repetitions * restoration_interval
    if verbose:
        if (potential_last_restoration == 0):
            print("\nNot enough rounds were requested to see any restoration "
                "occur in a deck of this size.")
        else:
            print(f"\nThe potential last restoration round would "
                f"be: {potential_last_restoration}")
    
    # If we subtract potential_last_restoration from rounds_to_shuffle
    # the result is the 'effective' rounds to shuffle, use as
    # the 'effective_rounds' variable.

    effective_rounds = rounds_to_shuffle - potential_last_restoration
    if verbose:
        print(f"\nOptimized/effective rounds to shuffle would be: {effective_rounds}")
    
    # TODO: Maybe issue warning if no optimization was possible, perhaps because the
    # rounds_to_shuffle was lower than the restoration_interval, meaning that
    # not enough rounds were requested to result in any repetition of deck state
    # and thus no opportunity to optimize.
    return effective_rounds


if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
            "not executed directly.")
