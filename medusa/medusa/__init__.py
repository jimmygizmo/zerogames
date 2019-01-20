#! /usr/bin/env python3

import sys
import math

verbose = False


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





if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
            "not executed directly.")


##
#
