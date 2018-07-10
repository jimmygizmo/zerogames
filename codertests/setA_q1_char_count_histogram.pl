#!/usr/bin/env perl
use strict;
use warnings FATAL => 'all';

# Written by Jimmy Gizmo, July 9, 2018. Copyright (c) 2018. MIT License.

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
# In the display of the histogram, some character counts could be the same, so in addition to the primary sorting of
# the counts and graphical bar length, secondary sorting will order the characters alphanumerically so adjacent entries
# of the same count will be presented in an organize manner. The example output from the problem statement does not
# show this secondary sorting, but it is appropriate to include and does not complicate the solution below.
#

my $input = shift or exit(0); # @ARGV implied.
my $index_last = length($input) - 1;
my %char_counts;

# Use a hash to perform the initial character counting
for my $index (0 .. $index_last) {
    my $char = substr($input, $index, 1);
    $char_counts{$char} += 1;
    #print "$char ---- $char_counts{$char}\n"; # Developer output
}

# Create a hash with keys designed to accomplish the primary and secondary sorting and with values containing the
# the histogram output. Leading-zero padding will be used on the counts to allow correct sorting for counts that
# may rise to multiple digits. Character counts up to 9999 are supported.
my %sorting_hash;

for my $key (keys %char_counts) {
    my $numeric_part = "0000" . $char_counts{$key};
    $numeric_part =~ /(....)$/g;
    $numeric_part = $1;
    my $sort_key = $numeric_part . "-" . $key;
    $sorting_hash{$sort_key} = "    " . $key . ":" . "#"x$char_counts{$key};
    #print "$sort_key => $sorting_hash{$sort_key}\n"; # Developer output
}

print"\n";
for my $key (sort {$b cmp $a} keys %sorting_hash) {
    print "$sorting_hash{$key}\n";
}
print"\n";

##
#
