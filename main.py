from pprint import pprint

from player import Player

START_HAND_SIZE = 7
TEST_ROUNDS = 4
STARTING_RESOURCES = 3


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
                self.end_phase(current_player)

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

    def end_phase(self, current_player):
        current_player.recycle_used_deck()


if __name__ == '__main__':
    play_a_game = TheGame()
    play_a_game.main()
