from random import randrange

MAX_DECK_SIZE = 50


class Card(object):

    def __init__(self, owner=None):
        self.name = None
        self.card_type = None
        self.cost = None
        self.card_id = None
        self.owner = owner

    def __repr__(self):
        return "<Card id: %s name:%s type:%s cost:%s owner:%s>" % \
               (self.card_id,
                self.name,
                self.card_type,
                self.cost,
                self.owner.name)

    def get_id(self, card_id):
        '''
        Deck will inform us which number card it is in the deck.
        '''
        self.card_id = card_id


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

    def __len__(self):
        return len(self.cards_in_deck)

    def add_card(self, card, creation=False):
        '''
        Add a card to the deck.
        If this is during the creation of the deck (beginning
        of game) then give the card an id.
        '''
        self.cards_in_deck.append(card)
        if creation:
            card.get_id(len(self.cards_in_deck))

    def move_card_to_deck(self, deck):
        '''
        Given a deck, take a card from this one and
        add it to the given one.
        '''
        card_gathered = self.cards_in_deck.pop()
        deck.add_card(card_gathered)

    def randomize_cards(self):
        '''
        For testing, randomize cards. Give random names and
        other needed stats for the cards.
        '''
        for x in self.cards_in_deck:
            x.name = 'Card %x' % randrange(10000, 99999)
            x.cost = randrange(0, 7)


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

    def recycle_to_main(self, main_deck):
        '''
        Move cards from the used deck to the bottom of the
        main deck. This typically happens at end of turn
        but may happen other times.
        '''
        if len(self.cards_in_deck) > 0:
            main_deck.cards_in_deck.extend(self.cards_in_deck)
            self.cards_in_deck = []
