from card import Card, MainDeck, ResourceDeck, UsedDeck

START_HAND_SIZE = 7
TEST_ROUNDS = 4
STARTING_RESOURCES = 3


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
            card = get_random_card()
            main_deck.add_card(card)
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


def opening_phase(current_player):
    '''
    Gameplay starts with players moving some cards to their resource deck.
    Other miscellaneous events may occur here before moving on to the next
    phase of the game.
    '''
    for x in xrange(STARTING_RESOURCES):
        current_player.main_deck.move_card_to_deck(
            current_player.resource_deck)


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


def start_game(players):
    for player in players:
        for x in xrange(START_HAND_SIZE):
            player.draw_to_hand('main')


def main():
    Player1 = Player('Player1')
    Player2 = Player('Player2')
    players = [Player1, Player2]
    start_game(players)

    for game_round in xrange(TEST_ROUNDS):
        import pdb; pdb.set_trace()
        opening_phase()
        deploy_phase()
        move_phase()
        attack_phase()
        end_phase()

if __name__ == '__main__':
    main()
