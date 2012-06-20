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


class MainDeck(Deck):
    start_size = MAX_DECK_SIZE

    def __repr__(self):
        return "<MainDeck #cards:%s>" % len(self.cards_in_deck)


class ResourceDeck(Deck):

    def __repr__(self):
        return "<ResourceDeck #cards:%s>" % len(self.cards_in_deck)


class UsedDeck(Deck):

    def __repr__(self):
        return "<UsedDeck #cards:%s>" % len(self.cards_in_deck)
