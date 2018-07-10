#!/usr/bin/env perl
use strict;
use warnings FATAL => 'all';

# Written by Jimmy Gizmo, July 9, 2018. Copyright (c) 2018. MIT License.

# PROBLEM STATEMENT:
# Given a string consists of different types of brackets, write a function to determine the string is balanced.
# For example, "([])" and "[]{}" are balanced but "([)]" and "](){" are not.  You can assume these are the only
# characters in the string: ()[]{}

# ANALYSIS RULES COMMENTS:
#
# The below conditions are labeled and numbered so they can be referred to in other comments.
# B conditions represent a balanced state.
# N conditions represent a not-balanced state.
# The final analysis must find only B conditions and possibly multiple B conditions, for the string to be balanced.
# If any N conditions exist at all, then the string is determined to be not-balanced.
# NOTE: Not all conditions will necessarily be tested. Some of the conditions are implicit in other conditions.
# These analysis rules are not intended to model program logic, but are described to aid programming and comments.
# The solution will seek to test the minimum number of conditions in the most efficient manner and avoid redundant
# testing of conditions which are implicitly covered by other tests.
#
# Required conditions for the string to be balanced or which can occur in a balanced string:
#    B1 - A balanced pair can contain another balanced pair.
#    B2 - Multiple balanced pairs can exist in the string and can be adjacent to one another.
#
# Conditions which make the string unbalanced:
#    N1 - Any bracket exists in the string which does not have the other side of its pair also in the string.
#    N2 - Any pair of brackets spans across only one side of another balanced pair but does not contain it.
#
# The overall analysis is tracked with three states: "undetermined", "balanced" and "not-balanced".
# We begin in the "undetermined" state and may encounter this state during development tests, but once the final
# solution is working, there should not be any occurrences of "undetermined".
# Generally, we will first test for "balanced" conditions, followed by testing for "not-balanced" conditions,
# but it is possible that tests for either may occurring during analysis flow.

# Uncomment only the input string to be analyzed. Leave others commented-out.
my $input = "([])"; # Balanced
#my $input = "[]{}"; # Balanced
#my $input = "([)]"; # Not balanced
#my $input = "](){"; # Not balanced

my $state = "undetermined";


##
#
