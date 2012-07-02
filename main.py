from card import Card, MainDeck, ResourceDeck, UsedDeck
from pprint import pprint

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
            card = get_random_card(self)
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


class TheGame(object):
    def __init__(self):
        self.game_field = []  # List of Cards that are in play

    def command_line(self, current_player, phase_commands=None):
        '''
        Show basic command line and ask for player input.
        If unrecognized command, return False.
        If not basic command, return command and have
        phase function deal with it.
        '''
        commands = ['done', 'field', 'hand', 'decks', 'exit']
        if phase_commands is not None:
            commands.extend(phase_commands)

        print '\n%s options: %s' % (current_player.name, str(commands))
        action = raw_input('Action: ')

        if action not in commands:
            print 'Not a valid action.'
            return False
        elif action == 'field':
            print 'Cards in field:'
            pprint(self.game_field)
        elif action == 'hand':
            print 'Cards in hand:'
            pprint(current_player.hand)
        elif action == 'decks':
            for d in (current_player.resource_deck,
                      current_player.main_deck,
                      current_player.used_deck):
                print d
        elif action == 'exit':
            print 'Thank you for playing!'
            exit()
        return action

    def main(self):
        Player1 = Player('Player1')
        Player2 = Player('Player2')
        players = [Player1, Player2]
        self.start_game(players)
        for game_round in xrange(TEST_ROUNDS):
            for current_player in players:
                self.opening_phase(current_player)
                self.deploy_phase(current_player)
                self.move_phase()
                self.attack_phase()
                self.end_phase()

    def start_game(self, players):
        for player in players:
            player.randomize_decks()
            for x in xrange(START_HAND_SIZE):
                player.draw_to_hand('main')

    def opening_phase(self, current_player):
        '''
        Gameplay starts with players moving some cards to their resource deck.
        Other miscellaneous events may occur here before moving on to the next
        phase of the game.
        '''
        for x in xrange(STARTING_RESOURCES):
            current_player.main_deck.move_card_to_deck(
                current_player.resource_deck)

    def deploy_phase(self, current_player):
        '''
        Deploy cards
        '''
        action = None
        deploy_commands = ['play']
        while action != 'done':
            action = self.command_line(current_player, deploy_commands)
            if not action:
                continue
            if action == 'play':
                card_id = raw_input('Card id to play: ')
                card_to_play = current_player.play_card(int(card_id))
                if card_to_play:
                    self.game_field.append(card_to_play)

    def move_phase(self):
        pass

    def attack_phase(self):
        pass

    def end_phase(self):
        pass


def get_random_card(owner):
    card = Card(owner=owner)
    return card

if __name__ == '__main__':
    play_a_game = TheGame()
    play_a_game.main()
