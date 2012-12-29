from random import randrange
from PyQt4 import QtGui

MAX_DECK_SIZE = 50


class Card(object):

    def __init__(self, owner=None, name=None, cost=None, card_type=None):
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.card_id = None
        self.owner = owner

    def __repr__(self):
        return "<Card id: %s name:%s cost:%s owner:%s>" % (self.card_id,
                                                           self.name,
                                                           self.cost,
                                                           self.owner.name)

    def get_id(self, card_id):
        '''
        Deck will inform us which number card it is in the deck.
        '''
        self.card_id = card_id

    def randomize_stats(self):
        '''
        For testing, randomize card stats. Give random name and
        other needed stats for the card.
        '''
        self.name = 'Card %x' % randrange(10000, 99999)
        self.cost = randrange(0, 7)

    def gui_frame(self, game_field, position):
        #print "$"*8, game_field, position, self.owner.name
        off_set_hand = 0
        if self.owner.name == "Player2":
            off_set_hand -= 500
        card_frame = QtGui.QFrame(game_field)
        card_frame.setGeometry(position[0], position[1] + off_set_hand,
                                    130, 150)
        card_frame.setStyleSheet(
            "border: 1px solid black")
        card_label = QtGui.QLabel(self.name, game_field)
        card_label.move(position[0], position[1] + off_set_hand)

        type_label = QtGui.QLabel('Type: %s' % self.card_type, game_field)
        type_label.move(position[0], position[1] + off_set_hand + 15)

        cost_label = QtGui.QLabel('Cost: %s' % self.cost, game_field)
        cost_label.move(position[0], position[1] + off_set_hand + 30)

        #self.card_frame.update()
        #game_field.update()


class Character(Card):
    '''
    A card that will do battle with other character cards.
    Primarily will do damage to opponent to win the game.
    '''

    def __init__(self, owner=None, name=None, cost=None, attack=None,
                 defense=None, health=None):
        self.attack_value = attack
        self.defense_value = defense
        self.max_health_value = health
        self.health_value = health
        self.items = []
        self.exposed = None  # When in play, next to a tower or not (bool then)
        self.card_type = "Character"
        super(Character, self).__init__(owner=owner, name=name, cost=cost,
                                        card_type=self.card_type)

    def __repr__(self):
        return "<CharacterCard id: %s name:%s cost:%s owner:%s hp:%s/%s \
a/d:%s/%s items: %s>" % \
               (self.card_id,
                self.name,
                self.cost,
                self.owner.name,
                self.health_value,
                self.max_health_value,
                self.attack_value,
                self.defense_value,
                self.items)

    def total_defense(self):
        '''
        Return the characters defense value, including buffs.
        '''
        buffs = self.check_buffs()
        defense = buffs['defense_value'] + self.defense_value
        return defense

    def total_attack(self):
        '''
        Return the character attack value, including buffs.
        '''
        buffs = self.check_buffs()
        attack = buffs['attack_value'] + self.attack_value
        return attack

    def take_damage(self, damage):
        '''
        Given a value, this is how much damage is done to the cards health
        value. Will take into account any possible "shield" effects.
        If health drops to zero, will be discarded (goto lost pile).
        '''
        self.health_value -= damage

    def attack(self, card_to_attack):
        '''
        Compare attack and defense values against the enemy card and deal
        appropriate damage (if any). Returns damage done.
        '''
        damage = self.total_attack() - card_to_attack.total_defense()
        if damage > 0:
            card_to_attack.take_damage(damage)
        else:
            print 'No damage done.'
        return damage

    def move(self):
        '''
        Move from exposed to defending or defending to exposed.
        '''
        if self.exposed == False:
            self.exposed = True
        else:
            self.exposed = False
        return self.exposed

    def attach_item(self, attached_item):
        '''
        Given an item, attach it to the character.
        '''
        if type(attached_item) != Item:
            return False
        self.items.append(attached_item)
        return True

    def check_buffs(self):
        '''
        Check to see if character has buffs from items, spells, etc.
        '''
        buffs = {'attack_value': 0,
                 'defense_value': 0,
                 'health_value': 0}
        for i in self.items:
            item_buffs = i.get_buffs()
            buffs['attack_value'] += item_buffs['attack_value']
            buffs['defense_value'] += item_buffs['defense_value']
            buffs['health_value'] += item_buffs['health_value']
        return buffs

    def randomize_stats(self):
        self.attack_value = randrange(0, 5)
        self.defense_value = randrange(0, 5)
        health = randrange(0, 10)
        self.health_value = health
        self.max_health_value = health
        super(Character, self).randomize_stats()


class Spell(Card):
    '''
    Cards that are played by the "summoner" (player). These are generally
    effects played upon enemy character cards or possibly even on the enemy
    player directly.

    Effects of spells can be numerous and can potentially do anything (within
    game balance reasons of course), including changing the rules of the game.
    '''

    def __init__(self, owner=None, name=None, cost=None, target=None):
        self.target = target
        self.card_type = "Spell"
        super(Spell, self).__init__(owner=owner, name=name, cost=cost,
                                    card_type=self.card_type)


class Item(Card):
    '''
    Item cards are cards that modify the stats of players and may give certain
    benefits (like a shield).
    '''

    def __init__(self, owner=None, name=None, cost=None, buffs=None):
        self.buffs = buffs
        self.equiped_to = None
        self.card_type = "Item"
        super(Item, self).__init__(owner=owner, name=name, cost=cost,
                                   card_type=self.card_type)

    def __repr__(self):
        return "<ItemCard id: %s name: %s cost: %s buffs: %s>" % (
            self.card_id,
            self.name,
            self.cost,
            self.buffs)

    def get_buffs(self):
        '''
        Check if item card gives buffs. If so, return buffs to what stats.
        '''
        buff = {'attack_value': 0,
                'defense_value': 0,
                'health_value': 0}
        buff['attack_value'] += self.buffs.get('attack_value', 0)
        buff['defense_value'] += self.buffs.get('defense_value', 0)
        buff['health_value'] += self.buffs.get('health_value', 0)
        return buff

    def equip_to(self, equip_character):
        '''
        Items attach to characters. Give the character who this item is
        attached to.
        '''
        if type(equip_character) != Character:
            return False
        self.equiped_to = equip_character
        return True

    def randomize_stats(self):
        self.buffs = {'attack_value': randrange(1, 3),
                      'defense_value': randrange(1, 3),
                      'health_value': randrange(1, 3)}
        super(Item, self).randomize_stats()


class Deck(object):

    def __init__(self, name=None, kind=None, cards=None):
        self.name = name
        self.kind = kind
        if cards is None:
            self.cards_in_deck = []
        else:
            self.cards_in_deck = cards

    def __repr__(self):
        return "<Deck #cards:%s>" % len(self.cards_in_deck)

    def __len__(self):
        return len(self.cards_in_deck)

    def add_card(self, card, creation=False):
        '''
        Add a card to the deck.
        If this is during the creation of the deck (beginning
        of game) then give the card an id.
        '''
        self.cards_in_deck.append(card)
        if creation:
            card.get_id(len(self.cards_in_deck))

    def move_card_to_deck(self, deck):
        '''
        Given a deck, take a card from this one and
        add it to the given one.
        '''
        card_gathered = self.cards_in_deck.pop()
        deck.add_card(card_gathered)

    def randomize_cards(self):
        '''
        For testing, randomize cards. Give random names and
        other needed stats for the cards.
        '''
        for x in self.cards_in_deck:
            x.randomize_stats()


class MainDeck(Deck):
    '''
    This is the "core" deck. All cards start in this deck.
    '''
    start_size = MAX_DECK_SIZE

    def __repr__(self):
        return "<MainDeck #cards:%s>" % len(self.cards_in_deck)

    def get_towers(self):
        '''
        Find towers in the deck.
        '''
        towers = []
        for c in self.cards_in_deck:
            if type(c) == Character and c.name is not None and \
                   c.name.startswith('Tower'):
                towers.append(c)
        for tower in towers:
            self.cards_in_deck.pop(self.cards_in_deck.index(tower))
        return towers


class ResourceDeck(Deck):
    '''
    Players will move cards from their resource deck to the used deck
    when they wish to play a card. How many needs to be moved is
    dependant on the cards deploy value.
    '''

    def __repr__(self):
        return "<ResourceDeck #cards:%s>" % len(self.cards_in_deck)


class UsedDeck(Deck):
    '''
    When a card needs to be deployed, the cards from the resource deck
    are moved to here. Other cards may end up here to do being "used" but
    not being discarded.
    At the end of a turn, all cards here move back to under the resource deck
    so that the cycling of cards completes.
    '''

    def __repr__(self):
        return "<UsedDeck #cards:%s>" % len(self.cards_in_deck)

    def recycle_to_main(self, main_deck):
        '''
        Move cards from the used deck to the bottom of the
        main deck. This typically happens at end of turn
        but may happen other times.
        '''
        if len(self.cards_in_deck) > 0:
            main_deck.cards_in_deck.extend(self.cards_in_deck)
            self.cards_in_deck = []


class DiscardPile(Deck):
    '''
    Cards that are discarded go here. This may be from being killed in battle
    or removed from the game field by some other means.
    '''

    def __repr__(self):
        return "<DiscardPile #cards:%s>" % len(self.cards_in_deck)
