from __future__ import print_function
import os
import random

class GameEngine(object):
    def __init__(self):
        self.locationx = 0
        self.locationy = 0
        self.action = ''
        self.location_description = ''
        self.enemy = None
        self.enemy_description = ''
    
    
    def main_loop(self):
        while self.action != 'Quit':
            os.system('cls' if os.name == 'nt' else 'clear')
                        
            self.read_location()
            
            print(self.location_description)
            
            self.generate_enemy()
            
            print(self.enemy_description)
            print("\n")
            
            print("What do you want to do? ")
            self.action = raw_input()
            
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
            
            
            
