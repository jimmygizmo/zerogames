#!/usr/bin/perl
# File: perlcards.pl
# Console-based simulation of a deck of cards.
# This application uses the CardDeck class.
# All application and class code by Jimmy Gizmo. January, 2010.
$VERSION = 1.0.09;

use strict;
use warnings;
use lib '.'; # Directory containing the CardDeck.pm file.
use CardDeck;

# Instantiate a fresh deck object, which initially contains a full deck
# of un-shuffled cards (nicely ordered by color, suit and type).
my $deck_obj = CardDeck->new();

&show_instructions();

my $exit; # Flag: exit the menu loop
while ( ! $exit ) {
    &display_shuffled_state();
    &display_hand();
    &show_menu();
    my $in = 0; # Flag: recognized input seen
    my $input = <STDIN>;
    print "\n";
    chomp($input);
    if ( $input eq '1' ) {
        $in = 1;
        &display_deck();
    }
    if ( $input eq '2' ) {
        $in = 1;
        &shuffle_deck();
        &display_deck();
    }
    if ( $input eq '3' ) {
        $in = 1;
        &deal_card();
    }
    if ( $input eq '4' ) {
        $in = 1;
        &show_instructions();
    }
    if ( $input =~ /^5|q$/i ) {
        $in = 1;
        $exit = 1;
        print "CardSim Exiting.\n\n";
    } else {
        unless ( $in ) { print "* * * unrecognized selection * * *\n" }
    }
} # End while - main execution loop

exit (0);

sub display_deck {
    my @show_deck = $deck_obj->current_deck;
    print "\nCURRENT DECK OF CARDS:\n";
    print "----------------------\n";
    foreach my $show_card ( @show_deck ) {
        print $show_card . "\n";
    }
} # End sub display_deck

sub shuffle_deck { 
    $deck_obj->shuffle;
    print "\nTHE DECK HAS BEEN SHUFFLED.\n";
} # End sub shuffle_deck

sub deal_card {
    print "\nYOU HAVE JUST BEEN DEALT THIS CARD:\n";
    print $deck_obj->deal_card . "\n";
    print "Any previous card you had was put back onto the bottom of the deck.\n";
    print "The card you were just dealt is no longer in the deck.\n";
} # End sub deal_card

sub display_shuffled_state {
    print "\nSHUFFLED STATE: This deck is currently: ";
    print $deck_obj->current_shuffled_state . "\n";
} # End sub display_shuffled_state

sub display_hand {
    print "\n---- CURRENT HAND ----> ";
    print $deck_obj->current_hand . "\n";
} # End sub display_hand

sub show_menu {
    print "\nMENU:\n";
    print "1   .. Display the current deck of cards.\n";
    print "2   .. Shuffle and then display the deck of cards.\n";
    print "3   .. Deal me a card from the top of the deck.\n";
    print "4   .. Instructions.\n";
    print "5/Q .. Exit.\n";
    print "SELECT 1-5 or Q and PRESS ENTER: ";
} # End sub show_menu

sub show_instructions {
    print "\n********************************************************************\n";
    print "* CardSim * A simulation of a deck of cards.\n";
    print "* The deck is displayed as it is stacked, top card to bottom card.\n";
    print "* Before you shuffle the deck, it starts out very organized.\n";
    print "* (Try displaying the fresh deck both before and then after shuffling!)\n";
    print "* Cards are dealt from the top of the deck.\n";
    print "* A card is no longer a member of the deck once it has been dealt.\n";
    print "* The current simulation will only deal 1 card at a time.\n";
    print "* If you have a card, it will be returned to the bottom of the deck\n";
    print "* when you ask to be dealt another one.\n";
    print "* You can shuffle the deck at any time, with a dealt card or not.\n";
    print "* Type a number and press ENTER to make your menu selections.\n";
    print "********************************************************************\n";
} # End sub show_instructions

##
#
