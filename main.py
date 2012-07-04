from pprint import pprint

from player import Player
from card import Character

START_HAND_SIZE = 7
TEST_ROUNDS = 4
STARTING_RESOURCES = 3


class TheGame(object):
    def __init__(self):
        self.game_field = []  # List of Cards that are in play

    def find_card_on_field(self, card_id, target_player):
        '''
        Find a card on the field for a certain player given the card
        id and the player.
        '''
        for c in self.game_field:
            if c.card_id == card_id and c.owner == target_player:
                return c
        return False

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
                      current_player.used_deck,
                      current_player.discard_pile):
                print d
        elif action == 'exit':
            print 'Thank you for playing!'
            exit()
        return action

    def main(self):
        '''
        Player creation and game phases. Basic functions of gameplay
        and how the game moves from phase to phase.
        '''
        Player1 = Player('Player1')
        Player2 = Player('Player2')
        players = [Player1, Player2]
        enemy_player = players[1]
        self.start_game(players)
        for game_round in xrange(TEST_ROUNDS):
            for current_player in players:
                self.opening_phase(current_player)
                self.deploy_phase(current_player)
                self.move_phase()
                self.attack_phase(current_player, enemy_player)
                self.end_phase(current_player)
                enemy_player = current_player

    def start_game(self, players):
        '''
        Deck creation and other starting options needed for players.
        '''
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
            print 'Deploy Phase'
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

    def attack_phase(self, current_player, enemy_player):
        '''
        Characters on field may attack one another or any other valid target.
        '''
        action = None
        attack_commands = ['attack']
        while action != 'done':
            print 'Attack Phase'
            action = self.command_line(current_player, attack_commands)
            if not action:
                continue
            if action == 'attack':
                print 'Field:'
                pprint(self.game_field)
                card_id = raw_input('Card id attacking: ')
                card_attacking = self.find_card_on_field(int(card_id),
                                                      current_player)
                if not card_attacking:
                    print 'Can not find that card you own.'
                    continue
                card_id = raw_input('Card id to attack: ')
                card_to_attack = self.find_card_on_field(int(card_id),
                                                         enemy_player)
                if not card_to_attack:
                    print 'Can not find that enemy card on field.'
                    continue

                damage_done = card_attacking.attack(card_to_attack)
                print 'Damage done: %s' % damage_done
        discard_cards = []
        for c in self.game_field:  # Check which cards need to be discarded
            if type(c) == Character and c.health_value <= 0:
                discard_cards.append(c)
        for c in discard_cards:
            card_to_discard = self.game_field.pop(self.game_field.index(c))
            card_to_discard.owner.discard_pile.add_card(card_to_discard)
            print 'Moved %s to discard pile.' % card_to_discard.name

    def end_phase(self, current_player):
        current_player.recycle_used_deck()


if __name__ == '__main__':
    play_a_game = TheGame()
    play_a_game.main()
