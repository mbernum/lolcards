MAX_DECK_SIZE = 50


class Card(object):

    def __init__(self):
        self.name = None
        self.card_type = None
        self.cost = None

    def __repr__(self):
        return "<Card name:%s type:%s cost:%s>" % (self.name,
                                                   self.card_type,
                                                   self.cost)


class Deck(object):

    def __init__(self, name=None, kind=None, cards=None):
        self.name = name
        self.kind = kind
        if cards is None:
            self.cards_in_deck = []
        else:
            self.cards_in_deck = cards

    def __repr__(self):
        return "<Deck #cards:%s>" % len(self.cards_in_deck)

    def add_card(self, card):
        '''
        Add a card to the deck.
        '''
        self.cards_in_deck.append(card)

    def move_card_to_deck(self, deck):
        '''
        Given a deck, take a card from this one and
        add it to the given one.
        '''
        card_gathered = self.cards_in_deck.pop()
        deck.add_card(card_gathered)


class MainDeck(Deck):
    '''
    This is the "core" deck. All cards start in this deck.
    '''
    start_size = MAX_DECK_SIZE

    def __repr__(self):
        return "<MainDeck #cards:%s>" % len(self.cards_in_deck)


class ResourceDeck(Deck):
    '''
    Players will move cards from their resource deck to the used deck
    when they wish to play a card. How many needs to be moved is
    dependant on the cards deploy value.
    '''

    def __repr__(self):
        return "<ResourceDeck #cards:%s>" % len(self.cards_in_deck)


class UsedDeck(Deck):
    '''
    When a card needs to be deployed, the cards from the resource deck
    are moved to here. Other cards may end up here to do being "used" but
    not being discarded.
    At the end of a turn, all cards here move back to under the resource deck
    so that the cycling of cards completes.
    '''

    def __repr__(self):
        return "<UsedDeck #cards:%s>" % len(self.cards_in_deck)
