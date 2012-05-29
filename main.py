from card import Card

START_HAND_SIZE = 7
TEST_ROUNDS = 4


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = []

    def get_card(self, card):
        self.hand.append(card)


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


def start_game(players):
    for player in players:
        for x in xrange(START_HAND_SIZE):
            start_card = get_random_card()
            player.get_card(start_card)


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
