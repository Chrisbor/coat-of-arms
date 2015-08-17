#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Coat-of-Arms.py
#
# Copyright 2015 Christopher Borchert <chrisbor@outlook.com>
#
# Licensed under the terms of the MIT license.
#
# I know this is not quite the most efficient code you've ever seen.
# Whatever, it works.
#

from menu import Menu
from menu import GuidedMenu
from world import *

#World. Not that important.
global world

#Menus *m
global startm
global newgamem
global quitm

#Guided menus *gm
global startgamegm
global joingamegm
global loadgamegm
global createplayergm
global createworldgm
global connecttoservergm

def main():
    create_menus()
    startm.execute()
    world.pretty_print()
    return 0

def create_menus():
    #Globals...   -.-
    global startm
    global newgamem
    global quitm

    global startgamegm
    global joingamegm
    global loadgamegm
    global createplayergm
    global createworldgm
    global connecttoservergm

    #Actual creation
    startm = Menu([], "\n-- Start menu --")
    newgamem = Menu([], "\nStart game or join game?")
    quitm = Menu([] ,"\nDo you really want to leave? :o")

    startgamegm = GuidedMenu([], "\nPlease give the following data to start a new game:")
    joingamegm = GuidedMenu([], "\nPlease follow the instructions to join an existing game:")
    loadgamegm = GuidedMenu([], "\nPlease help me to load the game:")
    createplayergm = GuidedMenu([], "\nPlease choose your player's attributes:")
    createworldgm = GuidedMenu([], "\nPlease choose these parameters to create a new world:")
    connecttoservergm = GuidedMenu([], "\nBefore continuing, we have to connect to the communication server:")

    #Adding entries just now, to avoid circular references
    startm.entries = [("New Game", newgamem.execute),("Load Game", loadgamegm.execute),("Quit", quitm.execute)]
    newgamem.entries = [("Start game", startgamegm.execute),("Join game", joingamegm.execute),("Return to start menu", startm.execute)]
    quitm.entries = [("Yes", exit),("No", startm.execute),("Return to start menu", startm.execute)]

    startgamegm.add_entries([connecttoservergm.execute, createworldgm.execute, loadgamegm.execute, createplayergm.execute])
    joingamegm.add_entries([connecttoservergm.execute, createplayergm.execute])
    loadgamegm.add_entries(["Absolute file path to the save file:", load_world])
    createplayergm.add_entries(["Name:", create_player])#, "Nation:", "Age (Be careful!):"])#, (sexm = Menu([("Female", return "Female"), ("Male", return "Male")])).execute])
    createworldgm.add_entries(["Name:", "Height:", "Width:", create_world])
    connecttoservergm.add_entries(["Game name:", "Communication e-mail server:", "E-mail account password:", connect_to_server])

def load_world():
    global world

    path = loadgamegm.entries[0][1]
    if path == "test": path = "c:\\users\\private\\documents\\github\\coat-of-arms\\example_world.xml"
    elif path == "none":
        print("!No world loaded!")
        return
    print("Loading world save "+path+"...   ", end="")
    world = World(path)
    print("Done.")

def create_player():
    global world

    print("Creating player...   ", end="")
    try:
        world.players[createplayergm.entries[0][1]] = Player(createplayergm.entries[0])
        print("Done.")
    except NameError:
        print("Sorry. Joining impossible. There is no world you can go into!")
        newgamem.execute()

def create_world():
    global world

    print("Just for completion. Doesn't work in the first versions!")
    print("Creating world...   ", end="")
    #get data from createworldgm; the world = World(data)
    print("Done.")

def connect_to_server():
    print("Trying to connect...   ", end="")
    #get data from connecttoservergm and connect to server
    print("Done.\nLogging in...   ", end="")
    #Log in to e-mail account
    print("Done.")



if __name__ == '__main__':
    main()




