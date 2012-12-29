import sys
from pprint import pprint
from PyQt4 import QtGui

from player import Player
from card import Character, Item

START_HAND_SIZE = 7
TEST_ROUNDS = 4
STARTING_RESOURCES = 3
SCREEN_SIZE = [1200, 750]


class GameField(QtGui.QFrame):
    def __init__(self):
        #print "*"*8, self
        self.field = []
        super(GameField, self).__init__()
        self.gui_field()

    def gui_field(self):
        '''
        Create window frame to play the game on.
        '''
        #self.setGeometry(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1])
        #frame_window = self.frameGeometry()
        #screen_center = QtGui.QDesktopWidget().availableGeometry().center()

        # Move center of frame to screen center
        #frame_window.moveCenter(screen_center)
        # Move top left application window to top left point of frame_window
        #self.move(frame_window.topLeft())

        #hand_label = QtGui.QLabel('Hand', self)
        #hand_label.move(15, 500)

        ## self.card_frame = QtGui.QFrame(self)
        ## self.card_frame.setGeometry(20, 420, 130, 150)
        ## self.card_frame.setStyleSheet("QWidget { border: 1px solid black }")

        #self.setWindowTitle('LoL CCG')
        #self.update()

    def exposed_characters(self):
        '''
        Look through the field and find which character cards are exposed.
        Exposed characters are ones not next to towers.
        If not exposed, the character is considered to be defending, towers
        will retaliate then.
        '''
        exposed_characters = [c for c in self.field
                              if type(c) == Character and c.exposed == True]
        return exposed_characters

    def defending_characters(self):
        '''
        Look through the field and find which characters cards are defending.
        '''
        defending_characters = [c for c in self.field
                                if type(c) == Character and c.exposed == False]
        return defending_characters

    def add_card(self, player_card):
        '''
        Add a card to the field.
        '''
        self.field.append(player_card)

    def discard_card(self, card_to_discard):
        '''
        Move target card to the discard pile.
        '''
        self.field.pop(self.field.index(card_to_discard))
        card_to_discard.owner.discard_pile.add_card(card_to_discard)
        print 'Moved %s to discard pile.' % card_to_discard.name

    def remove_dead_cards(self):
        '''
        Check the field for cards that should be sent do discard pile, such as
        character cards with no health left or expired spells or effects.
        '''
        discard_cards = []
        for c in self.field:
            if type(c) == Character and c.health_value <= 0:
                discard_cards.append(c)
        for c in discard_cards:
            self.discard_card(c)


class TheGame(QtGui.QMainWindow):
    def __init__(self):
        super(TheGame, self).__init__()
        self.setGeometry(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.setWindowTitle('LoL CCG')

        self.game_field = GameField()  # List of Cards that are in play

        self.setCentralWidget(self.game_field)
        self.center_screen()

    def center_screen(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                 (screen.height() - size.height()) / 2)

    def find_card_on_field(self, card_id, target_player):
        '''
        Find a card on the field for a certain player given the card
        id and the player.
        '''
        for c in self.game_field.field:
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
            pprint(self.game_field.field)
            print 'Exposed:'
            pprint(self.game_field.exposed_characters())
            print 'Defending:'
            pprint(self.game_field.defending_characters())
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
            #exit()
        return action

    def main(self):
        '''
        Player creation and game phases. Basic functions of gameplay
        and how the game moves from phase to phase.
        '''
        Player1 = Player('Player1', self.game_field)
        Player2 = Player('Player2', self.game_field)
        players = [Player1, Player2]
        enemy_player = players[1]
        self.start_game(players)

        ## self.card_frame = QtGui.QFrame(self.game_field)
        ## self.card_frame.setGeometry(20, 420, 130, 150)
        ## self.card_frame.setStyleSheet("QWidget { border: 1px solid black }")
        #self.game_field.show()

        for game_round in xrange(TEST_ROUNDS):
            for current_player in players:
                return
                self.opening_phase(current_player)
                self.deploy_phase(current_player)
                self.move_phase(current_player)
                self.attack_phase(current_player, enemy_player)
                self.end_phase(current_player)
                enemy_player = current_player

    def start_game(self, players):
        '''
        Deck creation and other starting options needed for players.
        '''
        for player in players:
            towers = player.main_deck.get_towers()
            for tower in towers:
                self.game_field.add_card(tower)
                tower.exposed = False
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
                    self.game_field.add_card(card_to_play)
                    if type(card_to_play) == Character:
                        # Characters start next to towers
                        card_to_play.exposed = False
                    if type(card_to_play) == Item:
                        attach_to = raw_input('Card id to attach to: ')
                        attach_to = self.find_card_on_field(int(attach_to),
                                                            current_player)
                        if type(attach_to) != Character:
                            print 'Must attach to character cards.'
                        if not attach_to:
                            print 'Can not find that card on field.'
                        attach_to.attach_item(card_to_play)

    def move_phase(self, current_player):
        '''
        Characters can move from defending to exposed.
        '''
        action = None
        move_commands = ['move']
        while action != 'done':
            print 'Move phase'
            action = self.command_line(current_player, move_commands)
            if not action:
                continue
            if action == 'move':
                card_id = raw_input('Card id to move: ')
                card_to_move = self.find_card_on_field(int(card_id),
                                                       current_player)
                if not card_to_move:
                    print 'Can not find that card you own.'
                    continue
                if type(card_to_move) != Character:
                    print 'That card is not a character & can not move.'
                    continue
                if type(card_to_move) == Character and \
                       card_to_move.name.startswith('Tower'):
                    print 'You can not move towers.'
                    continue
                moved = card_to_move.move()
                print 'Moved %s to %s.' % (card_to_move.name,
                                           'exposed' if moved else 'defending')

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
                pprint(self.game_field.field)
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
                if card_attacking.exposed == True or \
                       card_to_attack.exposed == True:
                    damage_done = card_attacking.attack(card_to_attack)
                else:
                    print 'Neither card is exposed, can not attack.'
                    continue
                print 'Damage done: %s' % damage_done
        self.game_field.remove_dead_cards()

    def end_phase(self, current_player):
        current_player.recycle_used_deck()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    play_a_game = TheGame()

    play_a_game.main()
    play_a_game.show()
    sys.exit(app.exec_())
