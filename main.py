from card import Card


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = []


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


def start_game(players):
    pass


def main():
    Player1 = Player('Player1')
    Player2 = Player('Player2')
    players = [Player1, Player2]
    start_game(players)

    while(True):
        opening_phase()
        deploy_phase()
        move_phase()
        attack_phase()
        end_phase()

if __name__ == '__main__':
    main()
