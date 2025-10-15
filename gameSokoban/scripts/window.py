import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()

image_icon_path = r"assets\images\icon.png"

class Window():
    def __init__(self):
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        self.size = (screen_w, screen_h)
        self.screen = pygame.display.set_mode(self.size)

        self.caption = "Sokoban Game"
        pygame.display.set_caption(self.caption)
    
        self.icon_ori = pygame.image.load(image_icon_path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon_ori, (32, 32))
        pygame.display.set_icon(self.icon)

        self.data_ori = {
            "status_screen" : "menu",
            "menu_back" : False,
            "map_ori_list" : [
                [],
                [  # Level 1
                "ewwwww",
                "wwcppw",
                "wgbbww",
                "wgggwe",
                "wgggwe",
                "wwwwwe"
                ],
                [  # Level 2
                "wwwwwww",
                "wppbppw",
                "wppwppw",
                "wgbbbgw",
                "wggbggw",
                "wgbbbcw",
                "wgggggw",
                "wwwwwww"
                ],
                [  # Level 3
                "eeeewwwwweeeeeeeeew",
                "eeeewgggweeeeeeeeee",
                "eeeewbggweeeeeeeeee",
                "eewwwggbwweeeeeeeee",
                "eewggbgbgweeeeeeeee",
                "wwwgwgwwgweeewwwwww",
                "wgggwgwwgwwwwwggppw",
                "wgbggbggggggggggppw",
                "wwwwwgwwwgwcwwggppw",
                "eeeewgggggwwwwwwwww",
                "eeeewwwwwwweeeeeeee"
                ]
            ],
            "map_current" : [],
            "level" : 0,
            "pos_history_list" : [],
            "pos_endpoints" : [],
            "pos_state" : {},
            "limit_condition_algorithm" : {
                "max_time" : 5,
                "max_step" : 500000
            },
            "algorithm_time_run_each_step" : 0.3,
            "fps" : 30,
            "algorithm" : "",
            "game_play_human" : {
                "TextClockHuman" : {
                    "elapsed" : None,
                    "stop" : None
                },
                "TextStatusHuman" : {
                    "text" : ""
                },
                "TextEsc" : {
                    "show" : None
                }
            },
            "game_play_AI" : {
                "Controller" : None,
                "ButtonPlayAI" : {
                    "angle" : None,
                    "speed" : None
                },
                "TextStatusAI" : {
                    "text" : ""
                },
                "TextEsc" : {
                    "show" : None
                },
                "ButtonSelectAlgorithm" : {
                    "zoom_current_rate" : None,
                    "zoom_init_rate" : None
                },
            },
            "algorithm_list"  : [
                "bfs",
                "dfs"
            ]
        }
        self.data = self.data_ori.copy()

    def reset_data(self):
        mode = self.data["mode"]
        level = self.data["level"]
        self.data = self.data_ori.copy()
        self.data["mode"] = mode
        self.data["level"] = level
        print(self.data)

    def set_data(self, name, value):
        self.data[name] = value

    def get_data(self, name):
        return self.data.get(name)