from random import randrange
from PyQt4 import QtGui

from card import Card, Character, Item
from card import MainDeck, ResourceDeck, UsedDeck, DiscardPile

MAX_TOWERS = 3


class Player(object):
    def __init__(self, name, game_field):
        self.name = name
        self.hand = []
        self.game_field = game_field

        self.next_hand_field_position = [20, 550]

        main_deck, resource_deck, used_deck, discard_pile = self.start_decks()
        self.main_deck = main_deck
        self.resource_deck = resource_deck
        self.used_deck = used_deck
        self.discard_pile = discard_pile
        self.gui_labels()

    def __repr__(self):
        return "<Player name:%s hand:%s>" % (self.name,
                                             self.hand)

    def gui_labels(self):
        '''
        Set up labels for this player on the gui game table
        '''
        hand_label = QtGui.QLabel('%s Hand' % self.name,
                                  self.game_field)
        label_offset = 0
        if self.name == 'Player2':
            label_offset = 500
        hand_label.move(15, 500 - label_offset)

    def start_decks(self):
        '''
        Initialize decks for player. Player will have their normal resource
        deck. Other decks are started but empty.
        '''
        main_deck = MainDeck()
        resource_deck = ResourceDeck()
        used_deck = UsedDeck()
        discard_pile = DiscardPile()

        for opening_card in xrange(main_deck.start_size):
            card = get_random_card(self)
            main_deck.add_card(card, creation=True)

        towers = self.set_up_towers()
        for tower in towers:
            main_deck.add_card(tower, creation=True)

        return main_deck, resource_deck, used_deck, discard_pile

    def set_up_towers(self):
        '''
        Each player starts with three towers on the field.
        This does not count against max cards in deck.
        Towers are essentially defending characters with some restrictions.
        '''
        towers = [Character(owner=self, name='Tower %s' % x,
                            attack=3, defense=3, health=5, cost=0)
                  for x in xrange(0, 3)]
        return towers

    def receive_card(self, card):
        '''
        Receive a card and add it to a players hand.
        '''
        self.hand.append(card)
        card.gui_frame(self.game_field,
                       self.next_hand_field_position)
        self.next_hand_field_position[0] += 150

    def draw_to_hand(self, deck_type='resource', actions=None):
        '''
        Take a card from a deck and add it to a players hand
        '''
        if deck_type == 'main':
            card_gathered = self.main_deck.cards_in_deck.pop()
        elif deck_type == 'resource':
            card_gathered = self.resource_deck.cards_in_deck.pop()

        self.receive_card(card_gathered)
        card_gathered.deploy_button.clicked.connect(
            lambda: actions['deploy'](card_gathered))

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
    card_chance = randrange(0, 10)
    if card_chance >= 0 and card_chance <= 4:  # Randomly choose a character
        card = Character(owner=owner)
    elif card_chance >= 5 and card_chance <= 8:
        card = Item(owner=owner)
    else:  # Otherwise just default card
        card = Card(owner=owner)
    return card
