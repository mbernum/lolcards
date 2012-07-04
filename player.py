from random import randrange

from card import Card, Character
from card import MainDeck, ResourceDeck, UsedDeck


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

        main_deck, resource_deck, used_deck = self.start_decks()
        self.main_deck = main_deck
        self.resource_deck = resource_deck
        self.used_deck = used_deck

    def __repr__(self):
        return "<Player name:%s hand:%s>" % (self.name,
                                             self.hand)

    def start_decks(self):
        '''
        Initialize decks for player. Player will have their normal resource
        deck. Other decks are started but empty.
        '''
        main_deck = MainDeck()
        resource_deck = ResourceDeck()
        used_deck = UsedDeck()
        for opening_card in xrange(main_deck.start_size):
            card = get_random_card(self)
            main_deck.add_card(card, creation=True)
        return main_deck, resource_deck, used_deck

    def receive_card(self, card):
        '''
        Receive a card and add it to a players hand.
        '''
        self.hand.append(card)

    def draw_to_hand(self, deck_type='resource'):
        '''
        Take a card from a deck and add it to a players hand
        '''
        if deck_type == 'main':
            card_gathered = self.main_deck.cards_in_deck.pop()
        elif deck_type == 'resource':
            card_gathered = self.resource_deck.cards_in_deck.pop()

        self.receive_card(card_gathered)

    def randomize_decks(self):
        '''
        For testing, randomize players decks.
        '''
        for d in (self.main_deck, self.resource_deck, self.used_deck):
            d.randomize_cards()

    def find_card_in_hand(self, card_id):
        '''
        Given the card_id, find it in the hand
        '''
        for c in self.hand:
            if c.card_id == card_id:
                return c
        return False

    def play_card(self, card_id):
        '''
        Take card from hand. Return that card.
        Returns false if can not find card in hand.
        '''
        card_to_play = self.find_card_in_hand(card_id)
        if not card_to_play:
            print 'Can not find card %s in hand.' % card_id
            return False
        if card_to_play.cost > len(self.resource_deck):
            print 'You do not have enough resources to play this card.'
            return False
        for x in xrange(0, card_to_play.cost):  # Pay cost of card
            self.resource_deck.move_card_to_deck(self.used_deck)

        card_to_play = self.hand.pop(self.hand.index(card_to_play))
        return card_to_play

    def recycle_used_deck(self):
        '''
        Move cards from the used deck to the bottom of the
        main deck. This typically happens at end of turn
        but may happen other times.
        '''
        self.used_deck.recycle_to_main(self.main_deck)


def get_random_card(owner):
    character_chance = randrange(0, 10)
    if character_chance > 8:  # Randomly choose a character
        card = Character(owner=owner)
    else:  # Otherwise just default card
        card = Card(owner=owner)
    return card
