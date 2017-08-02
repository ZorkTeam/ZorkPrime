from __future__ import print_function
import os
import random
import time

class GameEngine(object):
    def __init__(self):
        self.locationx = 5
        self.locationy = 17
        self.action = ' '
        self.location_description = ''
        self.enemy = None
        self.items = [("Rusty Knife", 0, 5)]
        self.exititemx = random.randint(0,17)
        self.exititemy = random.randint(0,17)
        self.playerhitpoints = 100
    
    def main_loop(self):
        clearscreen = True
        
        while self.action != 'QUIT':
            if clearscreen: 
                os.system('cls' if os.name == 'nt' else 'clear')
                self.read_location()
            
                print(self.location_description)
            
                self.enemy_manager()
            
                if self.enemy != None:
                    print("You have encountered a {0}.\n\n".format(self.enemy[0]))
                    print("{0}\n".format(self.enemy[3]))
            
                print("\n")
            
            print("What do you want to do? ")
            self.action = raw_input()
            
            self.action = self.action.strip().upper()
            clearscreen = not self.process_action()
            
            if self.playerhitpoints <= 0:
                self.exec_deathscene()

    def exec_deathscene(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("I died?!! How the hell did that happen? Next time use a potion! \n")
        print("I see a bright light.... and I hear a voice...\n")
        print("'You will live again! But you shall have nothing but what you started with.....'\n")
        print("........\n")
        time.sleep(10)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("It lied.... I feel like I only have half the energy...\n")
        
        haswand = False
        if ("Wand of Solomon", -2, 0) in self.items:
            print("... and this stupid wand? Is there something special?")
            haswand = True
        
        time.sleep(5)
        self.playerhitpoints = 50
        del self.items [:]
        self.items.append([("Rusty Knife", 0, 5)])
        if haswand:
            self.items.append(("Wand of Solomon", -2, 0))

    def read_location(self):
        with open("map.txt", "r") as themap:
            for line in themap:
                if line == "[{0},{1}]\n".format(self.locationx, self.locationy):
                    self.location_description = themap.next()
                    break

    def enemy_manager(self):
        possible = random.randint(1,10)
        if (possible not in [2,5,10] or 
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
        with open(enemyfile, "r") as enemies:
            which = (int)(enemies.readline())
            for line in enemies:
                if line == "[{0}]\n".format(which):
                    name = enemies.next().strip()
                    hitpoints = int(enemies.next())
                    deals = int(enemies.next())
                    description = enemies.next()
                    
                    return name, hitpoints, deals, description

    def process_action(self):
        if "QUIT" in self.action:
            return  ## Nothing to do
        
        if "GO " in self.action:
            self.navigate()
            return False
            
        elif "SEARCH" in self.action:
            self.search_area()
            return False
        
        elif "USE " in self.action:
            return self.satchel_action()

        elif "HELP" in self.action:
            self.get_help()
            return True

        elif "SATCHEL" in self.action:
            self.get_satchel()
            return False
        
        else:
            print("I'm confused. Do what now?")
            raw_input("\nPress Enter to continue.")
            return True
 
    def navigate(self):
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
                self.locationy = 0
                print("I can't go that way. Can't you read?")
                raw_input("\nPress Enter to continue.")
        else:
            print("Go where? I don't think so. Sober up!")
            raw_input("\nPress Enter to continue.")
        
    def search_area(self):
        print("Searching the area...")
        time.sleep(3)
        new_item = self.generate_item()

        print("After a careful search of the area, you've found...")
        if new_item != None:
            print("\t\t" + new_item[0])
            self.items.append(new_item)
            print("You added the " + new_item[0] + " to your satchel.")
        else:
            print("\t\tNothing!")
            
        raw_input("\nPress Enter to continue.")

    def generate_item(self):
        item_chance = random.randint(1, 500)

        if self.locationx == self.exititemx and self.locationy == self.exititemy:
            return ("Wand of Solomon", -2, 0)

        if item_chance >= 400:
            return None
        elif item_chance >= 300:
            return ('A bundle of sticks', 0, 1)
        elif item_chance >= 250:
            return ('Small potion', 1, 5)
        elif item_chance >= 200:
            return ('Medium potion', 1, 10)
        elif item_chance >= 150:
            return ('Large Potion', 1, 20)
        elif item_chance >= 100:
            return ('Spear', 0, 10)
        elif item_chance >= 80:
            return ('Long Sword',0, 15)
        elif item_chance >= 60:
            return ('Bow and Arrows', 0, 20)
        elif item_chance >= 40:
            return ('Gold', -1, 0)
        elif item_chance >= 20:
            return ('Jewels', -1, 0)
        elif item_chance >= 10:
            return ('Fireball', 0, 40)
        elif item_chance >= 2:
            return ('Lightning', 0, 50)
        elif item_chance == 1:
            return ('ULTIMATE HAMMER OF GOD', 0, 100)

    def get_help(self):
        with open("help.txt", "r") as help_file:
            for line in help_file:
                print(line.strip())
        raw_input("\nPress Enter to continue.")
        return

    def get_satchel(self):
        print('Contents of satchel:\n')
        for item in self.items:
            print(item[0])
        raw_input("\nPress Enter to continue.")
        return

    def satchel_action(self):
        usewhat = self.action.upper().strip().replace("USE ","")
        index = self.find_item(usewhat)
        
        if index == -1:
            print("Ummm.... where is that? Did I lose it?")
            raw_input("\nPress Enter to continue.")
            
            return False
        else:
            name,target,points = self.items[index]
            
            if self.enemy != None and target == 0:
                enemy, enemyhp, enemydeals, enemydesc = self.enemy
                player_damage = (points / 2) + random.randint(1, (points / 2))
                enemy_damage = random.randint(1, enemydeals)
                print("I used the weapon and did {0} out of {1} points of damage. \n ".format(player_damage, enemyhp))
                print("But he did {0} out of {1} to me too. \n".format(enemy_damage, self.playerhitpoints))
                enemyhp -= player_damage
                self.playerhitpoints -= enemy_damage
                
                if enemyhp <= 0:
                    print("\n I defeated the {0}.".format(enemy))
                    self.enemy = None
                
                else:
                    self.enemy = (enemy, enemyhp, enemydeals, enemydesc)
                
                return True
                
            elif target == 1:
                if self.playerhitpoints + points > 50:
                    self.playerhitpoints = 50
                else:
                    self.playerhitpoints += points
                    
                self.items.remove((name, target, points))
                
                print("Healed some of my damage.")
                raw_input("Press Enter to continue.\n")
                if self.enemy != None:
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
                
                else:
                    print("The Wand makes a stuttering sound but does nothing else. Is this thing broken?!!\n")
                
                raw_input("Press Enterto continue.")
                return False
    
        return False
    
    def find_item(self, itemname):
        '''Returns the index of the item'''
        
        item = 0
        for name,target,points in self.items:
            if itemname == name.upper().strip():
                return item
            
            item += 1
        
        return -1
