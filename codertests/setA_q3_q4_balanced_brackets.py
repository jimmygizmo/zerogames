#!/usr/bin/env python

# Written by Jimmy Gizmo, July 9, 2018. Copyright (c) 2018. MIT License.

# PROBLEM STATEMENT QUESTION # 3:
# Given a string consisting of different types of brackets, write a function to determine if the string is balanced.
# For example, "([])" and "[]{}" are balanced but "([)]" and "](){" are not.  You can assume these are the only
# characters in the string: ()[]{}
#
# # PROBLEM STATEMENT QUESTION # 4:
# If the string in Question 3 only consists of ( and ), how would it affect your solution from above?
# For example: "(())" or " (()("
#
#
# COMMENTS TO QUESTION # 4:
# With only curly brackets possible, no sets would be needed in this solution.
# The test to search left_bracket_set with the 'in' operator would become just a test to see if cursor == '('.
#
# Similarly, the set of tuples used for matching bracket pairs, bracket_pair_set, would not be needed.
# The test to see if last_left_bracket is in the set bracket_pair_set would become a test to see if it matched
# the tuple ('(', ')').
#
# These changes would be optimizations which accomplish: code simplification, higher performance and reduced
# memory usage. This might not matter in such a simple program but in a more complex program or for working on
# large data sets, these optimizations could become very significant improvements.

# COMMENTS:

test_input_strings = ['([])',  # Covers question # 3
                      '[]{}',  # Covers question # 3
                      '([)]',  # Covers question # 3
                      '](){',  # Covers question # 3
                      '(())',  # Covers question # 4
                      '(()('  # Covers question # 4
                      ]

test_input_strings_q4 = ['(())',  # Covers question # 4
                         '(()('  # Covers question # 4
                         ]

left_bracket_set = set('([{')

bracket_pair_set = set([  # A set of tuples of bracket pairs
                        ('(', ')'),
                        ('[', ']'),
                        ('{', '}')
                        ])


def balanced_brackets(test_string):
    if len(test_string) % 2 != 0:  # Only an even number of characters can be balanced
        return False
    stack_array = []
    for cursor in test_string:
        if cursor in left_bracket_set:
            stack_array.append(cursor)
        else:
            if len(stack_array) == 0:
                return False
            last_left_bracket = stack_array.pop()
            if (last_left_bracket, cursor) not in bracket_pair_set:
                return False
    return len(stack_array) == 0


def balanced_brackets_simplified_q4(test_string):
    if len(test_string) % 2 != 0:  # Only an even number of characters can be balanced
        return False
    stack_array = []
    for cursor in test_string:
        if cursor == '(':
            stack_array.append(cursor)
        else:
            if len(stack_array) == 0:
                return False
            last_left_bracket = stack_array.pop()
            if (last_left_bracket, cursor) != ('(', ')'):
                return False
    return len(stack_array) == 0


print
for test_string in test_input_strings:
    print "Q3. TEST STRING: " + test_string
    if balanced_brackets(test_string):
        print "Q3. STATE: balanced"
    else:
        print "Q3. STATE: not-balanced"
    print

print
for test_string in test_input_strings_q4:
    print "Q4. TEST STRING: " + test_string
    if balanced_brackets_simplified_q4(test_string):
        print "Q4. STATE: balanced"
    else:
        print "Q4. STATE: not-balanced"
    print

##
#
