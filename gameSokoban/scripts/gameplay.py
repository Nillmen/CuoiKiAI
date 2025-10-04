import pygame
from scripts import controller, map
from scripts import aiAlgorithms
from scripts.objects import box,character,wall,endpoint,ground

class Gameplay():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.level = self.window.get_data("level")
        self.mode = self.window.get_data("mode")
        self.map= map.Map(self.window)
        self.algorithm="BFS"
        self.window.set_data("algorithm", self.algorithm)

        self.character=self.map.character
        self.boxes = self.map.boxes
        self.controller=None
        
        self.aIAlgorithm = aiAlgorithms.Algorithm(self.window)

        self.mode_choosing()
        self.map.createMap()

        
        

    def handle_events(self, event):

        return True
    def release(self):
        pass
    def run(self):
        self.map.createMap()
        self.map.drawMap()
        
        pygame.display.flip()

    def mode_choosing(self):
        if self.mode =="human":
            self.controller=controller.Controller(self.character,self.boxes)
        if self.mode =="AI":
            self.ai_illustrate()
    def ai_illustrate(self):
        cellList,moveList = self.aIAlgorithm.get_solution()

        move = moveList[-1]
        self.character.move(move[0], move[1],self.map.walls,self.map.boxes)



    

    
 


        



        

        