#!/usr/bin/env perl
use strict;
use warnings FATAL => 'all';

# Written by Jimmy Gizmo, July 9, 2018. Copyright 2018. MIT License.

# PROBLEM STATEMENT:
# Write code to generate the following histogram display based on the frequency of occurrence of characters in the
# first argument to the program. Example:
#
#    $ perl histogram.pl "Mississippi borders Tennessee."
#    s: #######
#    e: #####
#    i: ####
#     : ##
#    n: ##
#    p: ##
#    r: ##
#    .: #
#    M: #
#    T: #
#    b: #
#    d: #
#    o: #

# ASSUMPTIONS:
# User provides a single program argument of at least one character. If the string provided contains any space
# characters, the user encloses the string in quotes.

# COMMENTS:
#
# Typical histogram display and the problem statement require that the output is sorted from highest frequency to
# lowest.
#
# If no argument is supplied the program exits cleanly but otherwise there is no argument validation.
#

my $input = shift or exit(0); # @ARGV implied.
my $index_last = length($input) - 1;
my %histogram;

for my $index (0 .. $index_last) {
    my $char = substr($input, $index, 1);
    $histogram{$char} += 1;
    print "$char ---- $histogram{$char}\n";
}

# my @keys = sort { $h{$a} <=> $h{$b} } keys(%h);

my @value_sorted_keys = sort { $histogram{$a} <=> $histogram{$b} } keys(%histogram);

print "\n";
# TODO - fix below here. Code above here works fine.
foreach my $value_sorted_key (@value_sorted_keys) {
    print $histogram{$value_sorted_key} . ":" . "#".$histogram{$value_sorted_key} . "\n"
}

##
#
