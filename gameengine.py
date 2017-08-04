''' Module gameengine.py '''

from __future__ import print_function
import os
import random
import time
import shelve

"""
ZorkPrime

Contributors:
    Richard Hamm    (reh14c@my.fsu.edu)
    Jordan Harlow   (jth14b@my.fsu.edu)
    Robert Zink     (rjz11@my.fsu.edu)

CIS4930 - Python Programming
Summer 2017
4 August 2017
gameengine.py
"""


class GameEngine(object):
    """ The core game engine
    """
    def __init__(self):
        """ Function: __init__
        Sets up the initial game variables
        """
        self.full_reset()
    
    def full_reset(self):
        self.exitopen = False
        self.locationx = 5
        self.locationy = 17
        self.action = ' '
        self.location_description = ''
        self.enemy = None
        self.items = [("Rusty Knife", 0, 5)]
        self.exititemx = random.randint(0,17)
        self.exititemy = random.randint(0,17)
        self.playerhitpoints = 100
        #18x18 grid of whether a player has searched or killed an enemy in an area
        self.grid_events = [[[False, False]] * 18 for i in range(18)]

    def save(self):
        """ Function: save
        Saves the progress of the current playthrough. Only one save file is allowed.
        :return:
        """
        s = shelve.open('zork_save.db')
        s['save'] = {'locationx': self.locationx, 'locationy': self.locationy, 'enemy': self.enemy, 'items': self.items, 'exititemx': self.exititemx, 'exititemy': self.exititemy, 'hp': self.playerhitpoints, 'gridevents': self.grid_events}
        s.close()
        print('Progress saved.')
        raw_input('Press Enter to continue')

    def load(self):
        """ Function: load
        Loads a saved game file, if it exists
        :return:
        """
        print('Loading game...\n')
        raw_input('Press Enter to continue')
        s = shelve.open('zork_save.db')
        if s:
            d = s['save']
            self.locationx = d['locationx']
            self.locationy = d['locationy']
            self.enemy = d['enemy']
            self.items = d['items']
            self.exititemx = d['exititemx']
            self.exititemy = d['exititemy']
            self.playerhitpoints = d['hp']
            self.grid_events = d['gridevents']
        else:
            print('There is no saved game to load!')
            raw_input('Press Enter to continue')

    def main_loop(self):
        """ Function: main_loop
        The main game loop, controls execution flow of the Zork game
        :return:
        """
        clearscreen = True
        
        while self.action != 'QUIT':
            if clearscreen: 
                os.system('cls' if os.name == 'nt' else 'clear')
                self.read_location()
                clearscreen = False
                print(self.location_description)
            
                if self.enemy is None:
                    self.enemy_manager()
            
                if self.enemy is not None:
                    print("You have encountered a {0}.\n\n".format(self.enemy[0]))
                    print("{0}\n".format(self.enemy[3]))
            
                print("\n")
            
            print("What do you want to do? ")
            self.action = raw_input()
            
            self.action = self.action.strip().upper()
            clearscreen = not self.process_action()
            
            if self.playerhitpoints <= 0:
                self.exec_deathscene()
                clearscreen = True

    def exec_deathscene(self):
        """ Function: exec_deathscene
        This function runs upon the death of the player
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("I died?!! How the hell did that happen? Next time use a potion! \n")
        print("I see a bright light.... and I hear a voice...\n")
        print("'You will live again! But you shall have nothing but what you started with.....'\n")
        print("........\n")
        raw_input("\n Press Enter to continue")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("It lied.... I feel like I only have half the energy...\n")

        haswand = False
        if ("Wand of Solomon", -2, 0) in self.items:
            print("... and this stupid wand? Is there something special?")
            haswand = True
        
        raw_input("\n Press Enter to continue")

        self.exitopen = False
        self.playerhitpoints = 50
        self.locationx = 5
        self.locationy = 17
        self.enemy = None
        del self.items [:]
        self.items.append(("Rusty Knife", 0, 5))
        if haswand:
            self.items.append(("Wand of Solomon", -2, 0))

    def read_location(self):
        """ Function: read_location
        Used to grab the location information for the current x and y coordinates from the map file
        :return:
        """
        with open("map.txt", "r") as themap:
            for line in themap:
                if line == "[{0},{1}]\n".format(self.locationx, self.locationy):
                    self.location_description = themap.next()
                    break

    def enemy_manager(self):
        """ Function: enemy_manager
        Handles enemy management and creation
        :return:
        """
        possible = random.randint(1,10)
        if (possible not in [2,5,10] or self.grid_events[self.locationx][self.locationy][1] == True or
            (self.locationx == 5 and self.locationy == 17) or
            (self.locationx == 8 and self.locationy == 0)):

            self.enemy = None
            self.enemy_description = ''
            return 
        else:
            if self.locationx in range(0,9) and self.locationy in range(0, 12):
                self.enemy = self.generate_enemy("CornfieldEnemies.txt")
            elif self.locationx in range(9,18) and self.locationy in range(0, 7):
                self.enemy = self.generate_enemy("CraggyEnemies.txt")       
            elif self.locationx in range(9,18) and self.locationy in range(7, 13):
                self.enemy = self.generate_enemy("PlantationEnemies.txt")
            elif self.locationx in range(0,6) and self.locationy in range(13, 18):
                self.enemy = self.generate_enemy("SwampEnemies.txt")
            elif self.locationx in range(6,18) and self.locationy in range(13, 18):
                self.enemy = self.generate_enemy("ForestEnemies.txt")

    def generate_enemy(self, enemyfile):
        """ Function: generate_enemy
        Generates an enemy for the player to fight from the specified enemy file
        :param enemyfile: The file to grab the enemy information from
        :return: Tuple containing enemy name, hitpoints, deals, and description
        """
        with open(enemyfile, "r") as enemies:
            which = random.randint(1, (int)(enemies.readline()))
            for line in enemies:
                if line == "[{0}]\n".format(which):
                    name = enemies.next().strip()
                    hitpoints = int(enemies.next())
                    deals = int(enemies.next())
                    description = enemies.next()
                    
                    return name, hitpoints, deals, description

    def process_action(self):
        """ Function: process_action
        Executes the action entered by the player
        :return: Boolean, determines whether or not the screen is cleared after the action
        """
        if "QUIT" in self.action:
            return  # Nothing to do
        
        if "GO " in self.action:
            return self.navigate()
            
        elif "SEARCH" in self.action:
            if not self.grid_events[self.locationx][self.locationy][0]:
                self.search_area()
                return False
            else:
                print("You've already searched this area before...\n")
                return True

        elif "USE " in self.action:
            return self.satchel_action()

        elif "HELP" in self.action:
            self.get_help()
            return False

        elif "SATCHEL" in self.action:
            self.get_satchel()
            return False

        elif "ESCAPE " in self.action:
            return self.escape()

        elif "SAVE" in self.action:
            self.save()
            return False

        elif "LOAD" in self.action:
            self.load()
            return False

        elif "HEALTH" in self.action:
            self.show_health()
            return True
        
        else:
            print("I'm confused. Do what now?")
            return True
 
    def navigate(self):
        """ Function: navigate
        Handles player movement around the x and y coordinates
        :return: Boolean, whether to clear screen or not
        """
        if self.enemy:
            print("There is an enemy here! I can't just leave!\n")
            return True

        if "EAST" in self.action:
            self.locationx += 1
            
            if self.locationx > 17:
                self.locationx = 17
                print("I can't go that way. Can't you read?")
                raw_input("\nPress Enter to continue.")
            
        elif "WEST" in self.action:
            self.locationx -= 1
            
            if self.locationx < 0:
                self.locationx = 0
                print("I can't go that way. Can't you read?")
                raw_input("\nPress Enter to continue.")
                
        elif "SOUTH" in self.action:
            self.locationy += 1
            
            if self.locationy > 17:
                self.locationy = 17
                print("I can't go that way. Can't you read?")
                raw_input("\nPress Enter to continue.")
                
        elif "NORTH" in self.action:
            self.locationy -= 1
            
            if self.locationy < 0:
                if self.exitopen and self.locationx == 8:
                    self.player_win()
                
                else:
                    self.locationy = 0
                    print("I can't go that way. Can't you read?")
                    raw_input("\nPress Enter to continue.")
        else:
            print("Go where? I don't think so. Sober up!")
            raw_input("\nPress Enter to continue.")
        
        return False
        
    def search_area(self):
        """ Function: search_area
        Handles the search command, adding an item to the player's satchel if one is found
        :return:
        """
        print("Searching the area...")
        time.sleep(2)
        new_item = self.generate_item()

        print("After a careful search of the area, you've found...")
        if new_item is not None:
            print("\t\t" + new_item[0])
            self.items.append(new_item)
            print("\nYou added the " + new_item[0] + " to your satchel.")
        else:
            print("\t\tNothing!")

        if self.enemy is not None:
            enemy_damage = random.randint(0, self.enemy[2])
            print("While searching, the {2} did {0} out of {1} to me. \n".format(enemy_damage, self.playerhitpoints, self.enemy[0]))
            self.playerhitpoints -= enemy_damage
        
        self.grid_events[self.locationx][self.locationy] = [True, self.grid_events[self.locationx][self.locationy][1]]
        raw_input("\nPress Enter to continue.")

    def generate_item(self):
        """ Function: generate_item
        Creates an item to be generated for the user (upon searching an area)
        :return: None, or a tuple with item information
        """
        item_chance = random.randint(1, 500)

        if self.locationx == self.exititemx and self.locationy == self.exititemy:
            return ("Wand of Solomon", -2, 0)

        if item_chance >= 300:
            return None
        elif item_chance >= 250:
            return ('Small potion', 1, 10)
        elif item_chance >= 200:
            return ('Medium potion', 1, 25)
        elif item_chance >= 150:
            return ('Large Potion', 1, 50)
        elif item_chance >= 100:
            return ('Spear', 0, 10)
        elif item_chance >= 80:
            return ('Long Sword',0, 15)
        elif item_chance >= 60:
            return ('Bow and Arrows', 0, 20)
        elif item_chance >= 40:
            return ('Long Axe', 0, 30)
        elif item_chance >= 20:
            return ('Max Potion', 1, 100)
        elif item_chance >= 10:
            return ('Fireball', 0, 40)
        elif item_chance >= 2:
            return ('Lightning', 0, 50)
        elif item_chance == 1:
            return ('ULTIMATE HAMMER OF GOD', 0, 100)

    def get_help(self):
        """ Function: get_help
        Shows the help screen with list of available commands
        :return:
        """
        with open("help.txt", "r") as help_file:
            for line in help_file:
                print(line.strip())
        raw_input("\nPress Enter to continue.")
        return

    def get_satchel(self):
        """ Function: get_satchel
        Prints the contents of the player's satchel
        :return:
        """
        print('Contents of satchel:\n')
        for item in self.items:
            print(item[0])
        raw_input("\nPress Enter to continue.")
        return

    def satchel_action(self):
        """ Function: satchel_action
        Handles the use of an item specified by the player
        :return: Boolean, to clear screen or not
        """
        usewhat = self.action.upper().strip().replace("USE ", "")
        index = self.find_item(usewhat)
        
        if index == -1:
            print("Ummm.... where is that? Did I lose it?")
            raw_input("\nPress Enter to continue.")
            
            return False
        else:
            name, target, points = self.items[index]

            if self.enemy is not None and target == 0:
                enemy, enemyhp, enemydeals, enemydesc = self.enemy
                player_damage = (points / 2) + random.randint(1, (points / 2))
                enemy_damage = random.randint(1, enemydeals)
                print("I used the {2} and did {0} out of {1} points of damage.".format(player_damage, enemyhp, name))
                print("\tBut he did {0} out of {1} to me too. \n".format(enemy_damage, self.playerhitpoints))
                enemyhp -= player_damage
                self.playerhitpoints -= enemy_damage
                
                if enemyhp <= 0:
                    print("\nI defeated the {0} - this area should be clear now.\n".format(enemy))
                    self.grid_events[self.locationx][self.locationy] = [self.grid_events[self.locationx][self.locationy][0], True]
                    self.enemy = None
                    raw_input("\nPress Enter to continue.")

                    return False
                
                else:
                    self.enemy = (enemy, enemyhp, enemydeals, enemydesc)
                
                return True

            elif self.enemy is None and target == 0:
                print("Uhh, what exactly are you swinging at?\n")
                raw_input("\nPress Enter to continue.")

                return True
                
            elif target == 1:
                if self.playerhitpoints == 100:
                    print("Your health is already full, you can't drink away your problems!\n")
                    raw_input("\nPress Enter to continue.")

                    return True
                elif self.playerhitpoints + points > 100:
                    self.playerhitpoints = 100
                else:
                    self.playerhitpoints += points
                    
                self.items.remove((name, target, points))
                
                print("I healed myself to {0} out of 100 health.".format(self.playerhitpoints))
                raw_input("\nPress Enter to continue.\n")
                if self.enemy is not None:
                    return True
                else:
                    return False

            elif target == -1:
                print("Ummm... Do you see a store? Maybe in the next town.")
                raw_input("\nPress Enter to continue.")
                return False
            
            elif target == -2:
                if self.locationx == 8 and self.locationy == 0:
                    print("The Wand of Solomon glows and the briars have opened the road. You can finally leave!!")
                    self.exitopen = True
                
                else:
                    print("The Wand makes a stuttering sound but does nothing else. Is this thing broken?!!\n")
                
                raw_input("\nPress Enter to continue.")
                return False
    
        return False

    def escape(self):
        """ Function: escape
        Escapes from an enemy encounter. Works like navigate, but only when an enemy is present on the screen
        :return: Boolean, returns whether to clear screen or not
        """
        if not self.enemy:
            print('Huh? There isn\'t an enemy here to escape from!\n')
            raw_input("\nPress Enter to continue.")
            return True
        else:
            if "EAST" in self.action:
                self.locationx += 1

                if self.locationx > 17:
                    self.locationx = 17
                    print("I can't go that way.")
                    raw_input("\nPress Enter to continue.")
                    return False

            elif "WEST" in self.action:
                self.locationx -= 1

                if self.locationx < 0:
                    self.locationx = 0
                    print("I can't go that way.")
                    raw_input("\nPress Enter to continue.")
                    return False

            elif "SOUTH" in self.action:
                self.locationy += 1

                if self.locationy > 17:
                    self.locationy = 17
                    print("I can't go that way.")
                    raw_input("\nPress Enter to continue.")
                    return False

            elif "NORTH" in self.action:
                self.locationy -= 1

                if self.locationy < 0:
                    if self.exitopen and self.locationx == 8:
                        self.player_win()
                    
                    else:
                        self.locationy = 0
                        print("I can't go that way.")
                        raw_input("\nPress Enter to continue.")
                        return False
            else:
                print("Go where? I don't think so. Sober up!")
                raw_input("\nPress Enter to continue.")
                return False

            escape_will_damage = random.choice([True, False, True])

            if escape_will_damage:
                escape_damage = (int)(self.enemy[2] * 0.5)
                print('You took {0} out of {2} damage escaping from {1}'.format(escape_damage, self.enemy[0], self.playerhitpoints))
                self.playerhitpoints -= escape_damage
                self.enemy = None
                raw_input('\nPress Enter to continue.')
            else:
                print('You managed to sneak away from the enemy without being noticed!')
                self.enemy = None
                raw_input('\nPress Enter to continue.')

            return False
    
    def find_item(self, itemname):
        """ Function: find_item
        Finds an item in the player's satchel
        :param itemname: The name of the item to search for
        :return: The item, or -1 if the item isn't found
        """
        item = 0
        for name,target,points in self.items:
            if itemname == name.upper().strip():
                return item
            
            item += 1
        
        return -1

    def player_win(self):
        """ Function: player_win
        Function that runs upon a win (player reaches [8,0] and uses Wand of Solomon, then goes north)
        :return: True, to clear the screen
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("CONGRATULATIONS!!! You have escaped the Doomed Valley!\n")
        print("You and I now part ways and I can continue on my journey.\n")
        again = raw_input("So... Do you want to play again? (Y/N)")
        
        if again.upper() == "Y":
            self.full_reset()
            return True
        
        else: 
            self.action = "QUIT"
            return True

    def show_health(self):
        """ Function: show_health
        Shows the players current health.
        :return:
        """
        print("You currently have " + str(self.playerhitpoints) + " out of 100 health.")
