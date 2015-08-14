#!/usr/bin/python3
#
# Coat of arms is an email-based, CLI strategy game of conquest.
# This module holds the representations of all in-game entities.
#
# Copyright (c) 2015 Daniel Vedder, Christopher Borchert
# Licensed under the terms of the MIT license.
#

import xml.etree.ElementTree as xmlET

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

class Unit:
    def __init__(self, uid, max_health, strength, name=""):
        self.uid = uid #A unique id consisting of player name + id number
        self.max_health = self.health = max_health
        self.strength = strength
        self.name = name

    def change_health(self, amount):
        ''' Change the health of this unit by amount. Method returns -1 if the
        unit dies, otherwise returns 0.
        '''
        self.health = self.health + amount
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health <= 0:
            return -1 #replace this with a custom error?
        else: return 0

class Player:
    def __init__(self, name, gold= 0, units=[], territories=[]):
        #TODO replace args with kwargs
        self.name = name
        self.units = units
        self.territories = territories
        self.gold = gold


class World:
    def __init__(self, world_file=None):
        self.players = []
        self.territories = {}
        self.random_seed = None
        if world_file:
            self.load_world(world_file)

    def load_world(self, file_name):
        "Parse the given world file"
        world_tree = xmlET.parse(file_name)
        tree_root = world_tree.getroot()
        self.random_seed = int(tree_root.find('seed').text)
        for t in tree_root.findall('territory'):
            name = t.attrib.get('name')
            tax = t.find('tax')
            neighbours = []
            for n in t.findall('neighbour'): neighbours.append(n.text)
            self.territories[name] = Territory(name, tax, neighbours)

    def pretty_print(self):
        print("World:\n======")
        print("Random seed: "+str(self.random_seed)+"\n")
        for t in self.territories.items():
            print("Territory "+t[0]+":")
            print("> "+str(t[1].tax.text)+" gold taxes")
            neighbours = ""
            for n in t[1].neighbours: neighbours = n+" "+neighbours
            print("> Neighbours: "+neighbours)


if __name__ == '__main__': #debugging
    w = World('example_world.xml')
    w.pretty_print()            
    