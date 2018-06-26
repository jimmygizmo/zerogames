# File: CardDeck.pm
# Class code by Jimmy Gizmo. January 2010.

package CardDeck;
$VERSION = 1.0.14;

# Class to implement a traditional deck of playing cards.
# Capability to shuffle, deal a card and remember the state of the deck.
# The current version can only deal a single card at a time but future
# versions could conceivably deal hands of specified sizes, deal multiple
# hands to multiple players or perform other specialized tasks to support
# various card games.
# Deck can be shuffled whether or not a card has been dealt from it.
# Cards are dealt from the top of the deck. If a card has already been
# dealt, then it is returned to the bottom of the deck at the time that
# another card is dealt.
#
# The deck is initialized in an organized state.
# To help demonstrate this class, it's data and the shuffling operation,
# the deck is not shuffled as part of initialization. The application is
# allowed the opportunity to display the 'un-shuffled' new deck.

use strict;
use vars qw( $AUTOLOAD ); # strict would complain otherwise
use warnings;
use Carp;
# These constants are interpolated into all code in this file at compile time.
use constant { COLOR => 0, SUIT => 1, CARD => 2 };

# A variable or method beginning with an underscore _ is considered private

{
# This closure serves to encapsulate all class data and methods. No indentation
# is added for this standard, large block as a matter of style and to ease editing.

#### Definition of how the data for the deck is stored and translated
# @_deck is defined outside of the general attribute data hash for readability
# then specified via reference within the usual %_attr_data hash.
#
# @_deck is defined via an array of references to anonymous arrays
# of card attributes. As an array, the deck naturally retains its sort order.
# The attributes could have been implemented with anaymous hashes so that they
# could be referred to using nicely-named keys such as: color, suit, card
# but for compactness in the data as well as in the code,  we will use an array
# and access via the numerical index/position, albeit through constants in the source.
# We make the code more readable than [0] [1] [2] when using these constants to
# refer to the attribute array indices. In some processing, such as our shuffling of
# the deck, we might also appreciate a slight performance gain with the use of
# an array over a hash. For larger data sets it can be a good performance strategy
# to use arrays with constants in this manner, rather than hashes. In this case
# of our deck of cards, the main benefit is in not having a cluttered initialization.
#
# Position Keys for the Attributes:
# [ COLOR, SUIT, CARD ]
# Position 0 = COLOR: B=Black, R=Red
# Position 1 = SUIT: C=Clubs, S=Spades, H=Hearts, D=Diamonds
# Position 2 = CARD: Specific card is stored explicitly without a lookup
my @_deck = (
    [ 'B', '', 'Joker'],
    [ 'R', '', 'Joker'],
    [ 'B', 'C', 'Ace'],
    [ 'B', 'C', '2'],
    [ 'B', 'C', '3'],
    [ 'B', 'C', '4'],
    [ 'B', 'C', '5'],
    [ 'B', 'C', '6'],
    [ 'B', 'C', '7'],
    [ 'B', 'C', '8'],
    [ 'B', 'C', '9'],
    [ 'B', 'C', '10'],
    [ 'B', 'C', 'Jack'],
    [ 'B', 'C', 'Queen'],
    [ 'B', 'C', 'King'],
    [ 'B', 'S', 'Ace'],
    [ 'B', 'S', '2'],
    [ 'B', 'S', '3'],
    [ 'B', 'S', '4'],
    [ 'B', 'S', '5'],
    [ 'B', 'S', '6'],
    [ 'B', 'S', '7'],
    [ 'B', 'S', '8'],
    [ 'B', 'S', '9'],
    [ 'B', 'S', '10'],
    [ 'B', 'S', 'Jack'],
    [ 'B', 'S', 'Queen'],
    [ 'B', 'S', 'King'],
    [ 'R', 'H', 'Ace'],
    [ 'R', 'H', '2'],
    [ 'R', 'H', '3'],
    [ 'R', 'H', '4'],
    [ 'R', 'H', '5'],
    [ 'R', 'H', '6'],
    [ 'R', 'H', '7'],
    [ 'R', 'H', '8'],
    [ 'R', 'H', '9'],
    [ 'R', 'H', '10'],
    [ 'R', 'H', 'Jack'],
    [ 'R', 'H', 'Queen'],
    [ 'R', 'H', 'King'],
    [ 'R', 'D', 'Ace'],
    [ 'R', 'D', '2'],
    [ 'R', 'D', '3'],
    [ 'R', 'D', '4'],
    [ 'R', 'D', '5'],
    [ 'R', 'D', '6'],
    [ 'R', 'D', '7'],
    [ 'R', 'D', '8'],
    [ 'R', 'D', '9'],
    [ 'R', 'D', '10'],
    [ 'R', 'D', 'Jack'],
    [ 'R', 'D', 'Queen'],
    [ 'R', 'D', 'King'],
); # End of @_deck array of references to anonymous arrays

# Lookups for Color and Suit since we prefer a compact definition of the deck.
# This would be more relevant to an application with large data sets where
# ad-hoc compression like this might be very important to reduce data size and
# speed up various operations.
# Rather than clutter up the definition of %_attr_data below, we define these hashes
# outside and then make a reference to them inside of %_attr_data as we did for @_deck
my %_color_lookup = ( 'B' => 'Black', 'R' => 'Red' );
my %_suit_lookup = (
    'C' => 'Clubs',
    'S' => 'Spades',
    'H' => 'Hearts',
    'D' => 'Diamonds',
);

my %_attr_data = #               DEFAULT        ACCESSIBILITY
    ( _deck =>               [ \@_deck,         'read/write' ], 
      _shuffled_state =>     [ '0',             'read/write' ],
      _hand =>               [ '',              'read/write' ], # SEE NOTE *HAND1
      _color_lookup =>       [ \%_color_lookup, 'read'       ],
      _suit_lookup =>        [ \%_suit_lookup,  'read'       ],
    );

# NOTE *HAND1: This scalar represents the single dealt card, but would likely become
# an array if future versions were to support dealing multiple cards.
# This is a reference to the anonymous array of the attributes of the single dealt card.
# In the 'deal_card' method, if _hand is not an empty string, that indicates a card has
# already been dealt and thus a reference to a single card's anon array would be in _hand.

# As a general rule, the class will keep track of how many CardDeck objects have been
# instantiated. If we build a multi-user online casino with this class, this class
# variable would tell us how many decks of cards are currently in use.
my $_deck_count = 0;

# Is a specified object attribute accessible in a given mode?
sub _accessible {
    my ( $self, $attr, $mode ) = @_;
    $_attr_data{$attr}[1] =~ /$mode/
}

# Classwide default value for a specified object attribute
sub _default_for {
    my ( $self, $attr ) = @_;
    $_attr_data{$attr}[0];
}

# Private method returns list of names of all specified object attributes
sub _standard_keys { keys %_attr_data; }

sub get_deck_count { $_deck_count; } # Public method to retrieve the object (deck) count

sub _incr_deck_count { ++$_deck_count } # Private method to increment object count
sub _decr_deck_count { --$_deck_count } # Private method to decrement object count

} # End of block enclosing/encapsulating class data and class methods

# new() Constructor:
# The constructor is dual-purpose in the sense that it can both create a fresh
# new instance of the class (object), initialized with defaults or it can clone
# an existing object by copying all of that objects attributes, possibly tweaking some of
# those attributes. Calling through the class name like this creates a fresh object:
# Class->new( %args_for_new_object )
# Thus new() is considered a class method in that case. Unspecified args defer to defaults.
#
# Calling through an existing object reference as below clones/customizes that object:
# $obj_ref->new( %args_to_customize_cloned_object )
# Thus new() is considered an object method in that scenario.
sub new {
    my ( $caller, %arg ) = @_;
    my $caller_is_obj = ref($caller);
    my $class = $caller_is_obj || $caller;
    my $self = bless {}, $class;
    foreach my $attrname ( $self->_standard_keys() )
    {
        my ( $argname ) = ( $attrname =~ /^_(.*)/);
        if ( exists $arg{$argname} )
            { $self->{$attrname} = $arg{$argname} } # Class uses supplied attr for new obj
        elsif ( $caller_is_obj )
            { $self->{$attrname} = $caller->{$attrname} } # Cloning uses attr of orig object
        else
            { $self->{$attrname} = $self->_default_for( $attrname ) } # Class uses default
    } # End foreach _standard_keys
    $self->_incr_deck_count();
    return $self;
} # End new constructor

# Destructor decrements the classes count of deck objects
sub DESTROY {
    $_[0]->_decr_deck_count();
}

# OBJECT METHODS

# Returns an array of the current state of the deck with nicely formatted
# names for each card. Top to bottom of the deck is first to last element of the array.
sub current_deck {
    my ( $self, %arg ) = @_;
    my $deck_arr_ref = $self->get_deck;
    my @deck = @{$deck_arr_ref};
    my @formatted_deck;
    my %suit_lu = %{$self->get_suit_lookup};
    my %color_lu = %{$self->get_color_lookup};
    foreach my $card_arr_ref ( @deck ) {
        my $formatted_card = $self->formatted_card( $card_arr_ref );
        push( @formatted_deck, $formatted_card );
    } # End foreach $card_arr_ref
    return( @formatted_deck );
} # End sub current_deck

# Randomly reorders all cards currently in the deck and sets the shuffled flag
# Does not return anything.
sub shuffle {
    my ( $self, %arg ) = @_;
    my $deck_arr_ref = $self->get_deck;
    my @deck = @{$deck_arr_ref}; # Copied the existing deck to work with temporarily
    my @shuffled_deck; # Also a temporary deck array we will reconstruct randomly
    my %randomizer_hash;
    foreach my $card ( @deck ) {
        my $lg_random_key = int( rand(9999) + 1 );
        $randomizer_hash{$lg_random_key} = $card;
    }
    foreach my $key ( sort keys %randomizer_hash ) {
        push( @shuffled_deck, $randomizer_hash{$key} );
    }
    $self->set_deck( \@shuffled_deck );
    $self->set_shuffled_state( 1 );
} # End sub shuffle

# Returns a string indicating the shuffled state of the deck
sub current_shuffled_state {
    my ( $self, %arg ) = @_;
    my @shuffle_words = ( 'NOT shuffled', 'shuffled' );
    return $shuffle_words[$self->get_shuffled_state];
} # End sub current_shuffled_state

# Returns a formatted string describing the current single dealt card/hand
sub current_hand {
    my ( $self, %arg ) = @_;
    my $card_arr_ref = $self->get_hand;
    my $formatted_hand;
    if ( $card_arr_ref eq '' ) {
        $formatted_hand = "NO CARD DEALT. NO HAND.";
        return( $formatted_hand );
    }
    $formatted_hand = $self->formatted_card( $card_arr_ref );
    return( $formatted_hand );
} # End sub current_hand

# Moves the card on the top of the deck into the _hand attribute and if there was a 
# pre-existing _hand, moves that onto the bottom of the deck.
# Returns a formatted string describing the single card just dealt.
sub deal_card {
    my ( $self, %arg ) = @_;
    my $deck_arr_ref = $self->get_deck;
    my @deck = @{$deck_arr_ref}; # Copied the existing deck to work with temporarily
    my $current_hand = $self->get_hand;
    # If a card has already been dealt (the player has a single card 'hand'),
    # then first -push- that card back onto the bottom of the deck.
    if ( $current_hand ne '' ) { 
        push( @deck, $current_hand );
    }
    # Now we can deal a new card by -shifting- it off the top of the deck
    my $new_hand = shift( @deck );
    # Store the reference to the new/modified deck in the object attributes
    $self->set_deck( \@deck );
    # Store the reference to the single dealt card/hand in the object attributes
    $self->set_hand( $new_hand ); # This was never copied but remains the same reference
    # to the same card, just now maintained in a different place (in hand not in the deck.)
    my $formatted_hand = $self->formatted_card( $new_hand );
    return( $formatted_hand );
} # End sub deal_card

# Takes a reference to an array of a card, which can be in the deck or in the single dealt
# hand and returns a formatted string describing that card, using lookups and constants
# and some logic upon the data to perform the formatting.
sub formatted_card {
    my ( $self, $card_attr_arr_ref ) = @_;
    my %suit_lu = %{$self->get_suit_lookup};
    my %color_lu = %{$self->get_color_lookup};
    my @card_attr = @{$card_attr_arr_ref};
    my $formatted_card = $card_attr[CARD];
    if ( $formatted_card ne 'Joker' ) {
        $formatted_card .= " of " . $suit_lu{$card_attr[SUIT]};
    }
    $formatted_card .= " (" . $color_lu{$card_attr[COLOR]} . ")";
    return( $formatted_card );
} # End sub formatted_card

# END OBJECT METHODS

# Dynamically generate basic attribute accessor methods (get/set) for elements
# of our object's attributes, honoring the accessibility settings in %_attr_data.
# The basic accessor subroutines spring into existence when first called if
# access is permitted and those dynamic subs remain after their first invocation,
# so subsequent calls are as efficient as a hardcoded subrountine.
sub AUTOLOAD {
    no strict "refs";
#    my $self = shift;
#    my $newval = shift;
    my ( $self, $newval ) = @_;

    # As yet unseen get_* method called?
    if ( $AUTOLOAD =~ /.*::get(_\w+)/ && $self->_accessible( $1, 'read' ) ) {
        my $attr_name = $1;
        *{$AUTOLOAD} = sub { return $_[0]->{$attr_name} };
        return $self->{$attr_name}
    }

    # As yet unseen set_* method called?
    if ( $AUTOLOAD =~ /.*::set(_\w+)/ && $self->_accessible( $1, 'write' ) ) {
        my $attr_name = $1;
        *{$AUTOLOAD} = sub { $_[0]->{$attr_name} = $_[1]; return };
        $self->{$1} = $newval;
        return
    }

    croak( "No such method: $AUTOLOAD" );
} # End sub AUTOLOAD

1;
##
#
