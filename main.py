from card import Card, MainDeck

START_HAND_SIZE = 7
TEST_ROUNDS = 4


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.main_deck = None
        self.resource_deck = None
        self.used_deck = None

    def get_card(self, card):
        self.hand.append(card)

    def get_deck(self, deck, deck_type):
        if deck_type == 'main':
            self.main_deck = deck
        elif deck_type == 'resource':
            self.resource_deck = deck
        elif deck_type == 'used':
            self.used_deck = deck

    def draw_to_hand(self, deck_type='resource'):
        if deck_type == 'main':
            card_gathered = self.main_deck.cards_in_deck.pop()
        elif deck_type == 'resource':
            card_gathered = self.resource_deck.cards_in_deck.pop()

        self.get_card(card_gathered)


def opening_phase():
    pass


def deploy_phase():
    pass


def move_phase():
    pass


def attack_phase():
    pass


def end_phase():
    pass


def get_random_card():
    card = Card()
    return card


def start_deck():
    deck = MainDeck()
    for opening_card in xrange(deck.start_size):
        card = get_random_card()
        deck.get_card(card)
    return deck


def start_game(players):
    for player in players:
        starting_deck = start_deck()
        player.get_deck(starting_deck, 'main')

        for x in xrange(START_HAND_SIZE):
            #start_card = get_random_card()
            player.draw_to_hand('main')


def main():
    Player1 = Player('Player1')
    Player2 = Player('Player2')
    players = [Player1, Player2]
    start_game(players)

    for game_round in xrange(TEST_ROUNDS):
        opening_phase()
        deploy_phase()
        move_phase()
        attack_phase()
        end_phase()

if __name__ == '__main__':
    main()
