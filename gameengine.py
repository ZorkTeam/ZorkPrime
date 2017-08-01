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
        self.playerhitpoints = 50
    
    def main_loop(self):
        clearscreen = True
        
        while self.action != 'QUIT':
            if clearscreen: 
                os.system('cls' if os.name == 'nt' else 'clear')
                self.read_location()
            
                print(self.location_description)
            
                self.generate_enemy()
            
                if self.enemy != None:
                    print("You have encountered a {0}.\n\n".format(self.enemy[0]))
                    print("{0}\n".format(self.enemy[3]))
            
                print("\n")
            
            print("What do you want to do? ")
            self.action = raw_input()
            
            self.action = self.action.strip().upper()
            clearscreen = not self.process_action()

    def read_location(self):
        with open("map.txt", "r") as themap:
            for line in themap:
                if line == "[{0},{1}]\n".format(self.locationx, self.locationy):
                    self.location_description = themap.next()
                    break

    def generate_enemy(self):
        possible = random.randint(1,10)
        if possible not in [2,5,10]:
            self.enemy = None
            self.enemy_description = ''
            return 

        else:
            which = random.randint(1,4)

            with open("enemy.txt", "r") as enemies:
                for line in enemies:
                    if line == "[{0}]\n".format(which):
                        name = enemies.next().strip()
                        hitpoints = int(enemies.next())
                        deals = int(enemies.next())
                        description = enemies.next()
                        
                        self.enemy = name, hitpoints, deals, description
                        break

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
        
        else:
            print("I'm confused. Do what now?")
            raw_input("\nPress Enter to continue.")
            return 
 
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
        time.sleep(5)
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
            return ('LIghtning', 0, 50)
        elif item_chance == 1:
            return ('ULTIMATE HAMMER OF GOD', 0, 100)

    def satchel_action(self):
        usewhat = self.action.upper().strip().replace("USE ","")
        
        for name,target,points in self.items:
            if name.upper() != usewhat:
                print("Ummm.... where is that? Did I lose it?")
                raw_input("\nPress Enter to continue.")
                
                return False
            else:
                if self.enemy != None and target == 0:
                    enemy, enemyhp, enemydeals, enemydesc = self.enemy
                    
                    print("I used the weapon and did {0}/{1} points of damage. \n ".format(points, enemyhp))
                    print("But he did {0}/{1} to me too. \n".format(enemydeals, self.playerhitpoints))
                    enemyhp -= points
                    self.playerhitpoints -= enemydeals
                    
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
                    
                    
        
        return
    