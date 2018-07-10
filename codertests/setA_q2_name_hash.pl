#!/usr/bin/env perl
use strict;
use warnings FATAL => 'all';

# Written by Jimmy Gizmo, July 9, 2018. Copyright 2018. MIT License.

# PROBLEM STATEMENT:
#

# ASSUMPTIONS: Any punctuation marks in names are included in name length character count and
# sorting.

# COMMENTS:
#
# Pragmas strict and warnings/FATAL speed development of quality code, help IDE
# features work, and help developers consistently write better code. Can be removed for
# production releases to increase performance whenever that is relevant.
#
# Shebang /usr/bin/env increases portability for cases where perl interpreter location may vary.
#
# Strategies of using custom sort indices and leading-0-padded key components are powerful
# and general purpose, particularly useful for complex sorting needs.
#
# Last names of up to 9999 characters in length are supported.
#

my %last_names = (
    "Mary" => "Li",
    "James" => "O'Day",
    "Thomas" => "Miller",
    "William" => "Garcia",
    "Elizabeth" => "Davis"
    );

my $index = 0;
my %output_hash;

for my $key (keys %last_names) {
    $index++;
    my $full_name = "$key $last_names{$key}";
    my $last_name_length = length($last_names{$key});
    my $index_key = "0000" . $last_name_length;
    $index_key =~ /(....)$/g;
    $index_key = $1;
    my $index_last_name = $last_names{$key};
    $index_key .= $index_last_name;
    $output_hash{$index_key} = $full_name;
}

print "\n";
for my $key (sort keys %output_hash) {
    print "$output_hash{$key}\n"
}

##
#
