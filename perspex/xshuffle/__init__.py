#!/usr/bin/env python3

import sys

verbose = False
optimize = False


def set_verbose(verbose_on=True):
    # For a simple module/program, limited use of global variables
    # in this manner for module runtime configuration is fine.
    global verbose
    if verbose_on:
        verbose = True
    else:
        verbose = False


def set_optimized_shuffling(optimize_on=True):
    global optimize
    if optimize_on:
        optimize = True
    else:
        optimize = False


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
            print(f"VALERR1")
            raise ValueError('rounds_to_shuffle argument must be a'
                'postitive integer.')
    if (type(deck) is not list):
            print(f"TYPEERR1")
            raise TypeError('deck must be a list.')
    if (rounds_to_shuffle == 0 or len(deck) == 0):  # Allowed
        print(f"JUST RETURNING DECK - 0 rounds or 0 len deck")
        print(rounds_to_shuffle)  # THIS IS OK
        print(len(deck))  # ********! THE PROBLEM
        return deck
    if verbose:
        print(f"\nShuffling deck with {len(deck)} cards, "
            f"{rounds_to_shuffle} rounds.")
    
    a = deck.copy()  # This list.copy() is necessary, otherwise we can have
    # a chain of references into the callee and internal manipulations
    # here can result in the passed deck argument variable being
    # modified. We deliberately use references a lot internally here
    # to conserve resources, but some extra care is necessary.
    b = []
    round = 1
    if verbose:
        show_stack(a, "\nORIGINAL:")
    
    while (round <= rounds_to_shuffle):
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
        # POSSIBLE OPTIMIZATION FOUND:
        # 1. Check len(a) vs len(b) and call one of the following
        #     with the stack containing cards in the first position:
        #     shuffle_one_round(a, b)
        #     shuffle_one_round(b, a)
        # Then also rename vars in the called subs to:
        # a -> start_stack and
        # b -> end_stack
        round += 1
    
    # First thought might be that we return b, but remember, a
    # gets replaced with b at the end of each iteration above.
    print(f"\nA: {a}")
    print(f"\nB: {b}")
    print(f"RETURNING A")
    return a


def shuffle_one_round(start_stack, end_stack):
    print(f"- - - shuffle one round - - - ")
    print(start_stack)
    """Shuffle one round, meaning perform as many 'shuffle units' as 
    necessary to exhaust all original cards in start_stack with all 
    cards ending up in end_stack."""
    while (len(start_stack) > 0):
        perform_shuffle_unit(start_stack, end_stack)
    return


def perform_shuffle_unit(start_stack, end_stack):
    """Perform one 'shuffle unit' upon the card stacks a and b. 
    The 'shuffle unit' is the smallest unique set of steps which are
    repeated upon cards being shuffled. The specific steps are: 
    1. """
    
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

if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
            "not executed directly.")
