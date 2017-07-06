from __future__ import print_function
import os
import random

class GameEngine(object):
    def __init__(self):
        self.locationx = 0
        self.locationy = 0
        self.action = ' '
        self.location_description = ''
        self.enemy = None
        self.enemy_description = ''
    
    
    def main_loop(self):
        while self.action != 'QUIT':
            os.system('cls' if os.name == 'nt' else 'clear')
                        
            self.read_location()
            
            print(self.location_description)
            
            self.generate_enemy()
            
            print(self.enemy_description)
            print("\n")
            
            print("What do you want to do? ")
            self.action = raw_input()
            
            self.action = self.action.strip().upper()
            self.process_action()
            
    def read_location(self):
        with open("map.txt", "r") as themap:
            for line in themap:
                if line == "[{0},{1}]\n".format(self.locationx, self.locationy):
                    self.location_description = themap.next()
                    break

    def generate_enemy(self):
        possible = random.randint(1,10)
        
        ## no enemy
        if possible not in [2,5,10]:
            self.enemy = None
            self.enemy_description = ''
            return 
        
        self.enemy_description = "An enemy was encountered"
        
##        if ((self.locationx >= 0 and self.locationx <= 5) and
##            (self.locationy >= 0 and self.locationy <= 8)):

    def process_action(self):
        if "QUIT" in self.action:
            return  ## Nothing to do
        
        if "GO " in self.action:
            self.navigate()
            
        elif "SEARCH" in self.action:
            self.search_area()
        
        elif "USE " in self.action:
            self.satchel_action()
        
        else:
            print("I'm confused. Do what now?")
            raw_input("\nPress Enter to continue.")
        
        
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
        return
        
    def satchel_action(self):
        return
    