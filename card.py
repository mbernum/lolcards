MAX_DECK_SIZE = 50


class Card(object):

    def __init__(self):
        self.name = None
        self.card_type = None
        self.cost = None


class Deck(object):

    def __init__(self):
        self.name = None
        self.kind = None
        self.cards_in_deck = []

    def get_card(self, card):
        self.cards_in_deck.append(card)


class MainDeck(Deck):
    start_size = MAX_DECK_SIZE
