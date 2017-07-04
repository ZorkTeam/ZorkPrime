from __future__ import print_function
import os

class GameEngine(object):
    def __init__(self):
        self.locationx = 0
        self.locationy = 0
        self.action = ''
        self.location_description = ''
        self.enemy_description = ''
    
    
    def main_loop(self):
        while self.action != 'Quit':
            os.system('cls' if os.name == 'nt' else 'clear')
                        
            self.read_location()
            
            print(self.location_description)
            ##self.generate_enemy()
            
    def read_location(self):
        with open("map.txt", "r") as themap:
            for line in themap:
                if line == "[{0},{1}]\n".format(self.locationx, self.locationy):
                    self.location_description = themap.next()
                    break

