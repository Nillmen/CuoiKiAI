import pygame

class AIAlgorithm():
    def __init__(self, window):
        self.window = window
        self.algorithm = self.window.get_data("algorithm")
        if len(self.algorithm) == 0:
            self.algorithm = "bfs" 

    def get_response(self):
        if self.algorithm == "bfs":
            return self.bfs()

    def bfs(self):
        pass

