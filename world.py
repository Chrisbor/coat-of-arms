#!/usr/bin/python3
#
# Coat of arms is an email-based, CLI strategy game of conquest.
# This module holds the representations of all in-game entities.
#
# Copyright (c) 2015 Daniel Vedder, Christopher Borchert
# Licensed under the terms of the MIT license.
#

import xml.etree.ElementTree as xmlET

global unit_cost
unit_cost = 2000

class Territory:
    def __init__(self, name, tax, neighbours=[], owner="", units=[]):
        self.name = name
        self.tax = tax
        self.neighbours = neighbours
        self.owner = owner
        self.units = units

    def add_neighbour(self, neighbour):
        "Add a neighbour to this territory (by name)"
        if neighbour not in self.neighbours:
            self.neighbours.append(neighbour)
            print(self.name+" now has the neighbours "+str(self.neighbours))

    def add_unit(self, unit):
        "Add a unit to this territory (by UID)"
        if unit not in self.units:
            self.units.append(unit)

class Occupations:
    "A list of possible activities for army units"
    # Better done with enums, but they aren't introduced until Python 3.4
    RESTING = 0
    MARCHING = 1
    TRAINING = 2
    FIGHTING = 3

class Unit:
    def __init__(self, uid, location, max_size=100, strength=5, name=""):
        self.uid = uid #A unique id consisting of player name + id number
        self.max_size = self.size = max_size
        self.strength = strength
        self.name = name
        self.location = location
        self.current_occupation = Occupations.RESTING
        self.training_units = 0

    def change_size(self, amount):
        ''' Change the size of this unit by amount. Method returns -1 if the
        unit dies, otherwise returns 0.
        '''
        self.size = self.size + amount
        if self.size > self.max_size:
            self.size = self.max_size
        elif self.size <= 0:
            return -1 #replace this with a custom error?
        else: return 0

    def train(self):
        ''' Tell a unit to train. For every three turns spent training, the unit
        gains one strength point.
        '''
        self.current_occupation = Occupation.TRAINING
        self.training_units = self.training_units + 1
        if self.training_units % 3 == 0:
            self.strength = self.strength + 1

class Player:
    def __init__(self, name, gold=0, territories=[], units={}):
        #TODO replace args with kwargs
        self.name = name
        self.units = units
        self.territories = territories
        self.gold = gold
        self.uid_counter = 1

    def new_unit(self, location):
        ''' The player buys a new unit that is set down at the specified
        location. If the player has insufficient funds, nothing happens and
        the method returns -1.
        '''
        global unit_cost
        if self.gold >= unit_cost:
            self.gold = self.gold - unit_cost
            uid = self.name+str(self.uid_counter)
            self.uid_counter = self.uid_counter + 1
            self.units[uid] = Unit(uid, location)
            return 0
        else: return -1

    def upgrade_unit(self, uid):
        ''' The player upgrades a unit (i.e. increases it's max size by one).
        Requires unit_cost / 50 gold. If the player has insufficient funds, the
        method does nothing and returns -1, otherwise it returns 0.
        '''
        global unit_cost
        if self.gold >= unit_cost / 50:
            self.gold = self.gold - unit_cost / 50
            self.units[uid].max_size = self.units[uid].max_size + 1
            return 0
        else: return -1

class World:
    def __init__(self, world_file=None):
        self.players = {}
        self.territories = {}
        self.random_seed = None
        if world_file:
            self.load_world(world_file)

    def load_world(self, file_name):
        "Parse the given world file"
        world_tree = xmlET.parse(file_name)
        tree_root = world_tree.getroot()
        self.random_seed = int(tree_root.find('seed').text)
        # Load all territories
        for t in tree_root.findall('territory'):
            name = t.attrib.get('name')
            tax = int(t.find('tax').text)
            owner = t.find('owner').text
            neighbours = []
            for n in t.findall('neighbour'): neighbours.append(n.text)
            units = []
            for u in t.findall('unit'): units.append(u.text)
            self.territories[name] = Territory(name, tax, neighbours,
                                               owner, units)
        # Load the players
        for p in tree_root.findall('player'):
            name = p.attrib.get('name')
            gold = int(p.find('gold').text)
            territories = []
            for t in p.findall('territory'): territories.append(t.text)
            units = {}
            for u in p.findall('unit'):
                uid = u.attrib.get('uid')
                u_name = u.attrib.get('name', "")
                max_size = u.attrib.get('max_size')
                size = u.attrib.get('size')
                strength = u.attrib.get('strength')
                location = u.attrib.get('location')
                units[uid] = Unit(uid, max_size, strength, location, u_name)
            self.players[name] = Player(name, gold, territories, units)


    def save_world(self, file_name=None):
        #Creating and appending tree elements
        #Creating root, adding seed
        root = xmlET.Element('world')
        world_tree = xmlET.ElementTree(root)
        seedE = xmlET.Element('seed')
        seedE.text = str(self.random_seed)
        root.append(seedE)
        #Creating territories, adding name and owner
        for t in self.territories:
            terr = self.territories[t]
            tE = xmlET.Element('territory', {'name': t})
            taxE = xmlET.Element('tax')
            taxE.text = str(terr.tax)
            tE.append(taxE)
            ownerE = xmlET.Element('owner')
            ownerE.text = terr.owner
            tE.append(ownerE)
            #Adding neighbours
            for n in terr.neighbours:
                nE = xmlET.Element('neighbour')
                nE.text = n
                tE.append(nE)
            #Adding units
            for u in terr.units:
                uE = xmlET.Element('unit')
                uE.text = u
                tE.append(uE)
            root.append(tE)
        #Creating players, adding name and gold
        for p in self.players:
            pl = self.players[p]
            pE = xmlET.Element('player', {'name': p})
            goldE = xmlET.Element('gold')
            goldE.text = str(pl.gold)
            pE.append(goldE)
            #Adding the player's territories
            for t in pl.territories:
                tE = xmlET.Element('territory')
                tE.text = t
                pE.append(tE)
            #Adding the player's units and corresponding data
            for u in pl.units:
                un = pl.units[u]
                uE = xmlET.Element('unit', {'uid': un.uid, 'name': un.name,
                            'strength': un.strength, 'size': un.size,
                            'max_size': un.max_size, 'location': un.location})
                pE.append(uE)
            root.append(pE)
        #Writing the complete ElementTree
        world_tree.write(file_name, "utf-8", True)
        print("\n\nWorking?\n\n _ \n/_\\\n\\_/\n")


    def pretty_print(self):
        "This is primarily a debugging function"
        print("World:\n======")
        print("Random seed: "+str(self.random_seed)+"\n")
        for t in self.territories.items():
            print("Territory "+t[0]+":")
            print("> Owner is "+str(t[1].owner))
            print("> "+str(t[1].tax)+" gold taxes")
            neighbours = ""
            for n in t[1].neighbours: neighbours = n+" "+neighbours
            print("> Neighbours: "+neighbours)
            t_units = ""
            for tu in t[1].units: t_units = tu+" "+t_units
            print("> Units: "+t_units)
        for p in self.players.items():
            print("Player "+p[0]+":")
            print("> "+str(p[1].gold)+" gold")
            territories = ""
            for t in p[1].territories: territories = t+" "+territories
            print("> Territories: "+territories)
            p_units = ""
            for pu in p[1].units.items(): p_units = pu[1].uid+" "+p_units
            print("> Units: "+p_units)


if __name__ == '__main__': #debugging
    w = World('example_world.xml')
    w.pretty_print()
    w.save_world('test_save.xml')

