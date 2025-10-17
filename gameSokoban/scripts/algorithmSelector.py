import pygame 
import pygame_gui as pg
import copy
from scripts.algorithm import forward_tracking
from scripts.algorithm import bfs, dfs, ids, greedy, beam, backtracking, partially_observable, ucs, astar, hill_climbing, sa, ac3, blind_search

dict_algorithm = {
    "bfs" : bfs,
    "dfs" : dfs,
    "ids" : ids,
    "greedy" : greedy,
    "beam" : beam,
    "backtracking" : backtracking,
    "partially_observable" : partially_observable,
    "ucs" : ucs,
    "astar" : astar,
    "forward_tracking" : forward_tracking,
    "hill_climbing" : hill_climbing,
    "sa" : sa,
    "ac3" : ac3,
    "blind_search" : blind_search
}
class AlgorithmSelector:
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.screen_size = self.window.get_data("screen_size")
        self.fps = self.window.get_data("fps")
        self.clock = pygame.time.Clock()
        self.data = self.window.get_data("game_play_AI").copy()
        self.controller = self.data["Controller"]
        self.input_infor = {}
        self.input_boxes = []
        self.algorithm_options = copy.deepcopy(list(dict_algorithm.keys()))

        self.manager = pg.UIManager(self.screen.get_size())

        self.dropdown = pg.elements.UIDropDownMenu(
            options_list=self.algorithm_options,
            starting_option=self.algorithm_options[0],
            relative_rect=pygame.Rect((self.screen_size[0]//2 - 100, 200), (200, 40)),
            manager=self.manager
        )

        self.button_confirm = pg.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_size[0] - 140, 20), (120, 40)),
            text='Xác nhận',
            manager=self.manager
        )

        self.button_back = pg.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (100, 40)),
            text='Quay lại',
            manager=self.manager
        )

        self.selected_algorithm = self.algorithm_options[0]
        self.key_value_list = []
        self.create_input_boxes()

        self.font = pygame.font.SysFont("Arial", 32, True)
        self.title = self.font.render("Chọn thuật toán cho AI", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.screen_size[0]//2, 120))

    def handle_events(self, event):
        if event:
            self.manager.process_events(event)

        if event and event.type == pg.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.dropdown:
                self.selected_algorithm = event.text
                self.create_input_boxes()
                self.key_value_list = []
                for label, entry in self.input_boxes:
                    key = label.text
                    new_value = entry.get_text()
                    key_value = {
                        key : new_value
                    }
                    self.key_value_list.append(key_value)       

        if event and event.type == pg.UI_TEXT_ENTRY_FINISHED:
            self.key_value_list = []
            for label, entry in self.input_boxes:
                key = label.text
                new_value = entry.get_text()
                key_value = {
                    key : new_value
                }
                self.key_value_list.append(key_value)

            check = dict_algorithm[self.selected_algorithm].check_input_infor(self.controller.ai_algorithm, self.key_value_list)
            if check:
                for label, entry in self.input_boxes:
                    t = self.input_infor[label.text]["type"]
                    self.input_infor[label.text]["value"] = t(entry.get_text())
            else:
                self.create_input_boxes()
        elif event and event.type == pg.UI_BUTTON_PRESSED:
            if event.ui_element == self.button_confirm:
                self.window.set_data("algorithm", self.selected_algorithm)
                level = self.window.get_data("level")
                map_ori = copy.deepcopy(self.window.get_data("map_ori_list")[level])
                self.window.set_data("map_current", map_ori)
                dict_algorithm[self.selected_algorithm].change_input_infor(self.controller.ai_algorithm, self.key_value_list)
                self.reset()
                self.window.set_data("game_play_AI", self.data)
                self.window.set_data("status_screen", "gameplay")

            elif event.ui_element == self.button_back:
                self.window.set_data("status_screen", "gameplay")

        return True

    def reset(self):
        self.window.set_data("pos_state", {})
        self.window.set_data("pos_history_list", [])
        self.data["Controller"] = None
        self.data["ButtonPlayAI"]["angle"] = None
        self.data["ButtonPlayAI"]["speed"] = None

    def create_input_boxes(self):
        self.input_infor = dict_algorithm[self.selected_algorithm].input_infor(self.controller.ai_algorithm).copy()
        for label, entry in self.input_boxes:
            label.kill()
            entry.kill()
        self.input_boxes.clear()

        y = 300
        for key, value in self.input_infor.items():
            label = pg.elements.UILabel(
                relative_rect=pygame.Rect((50, y), (200, 30)),
                text=key,
                manager=self.manager
            )
            entry = pg.elements.UITextEntryLine(
                relative_rect=pygame.Rect((220, y), (100, 30)),
                manager=self.manager
            )
            entry.set_text(str(value["value"]))
            self.input_boxes.append((label, entry))
            y += 30

    def run(self):
        time_delta = self.clock.tick(self.fps) / 1000.0

        self.manager.update(time_delta)

        self.draw_ui()
        pygame.display.flip()

    def draw_ui(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.title, self.title_rect)
        self.manager.draw_ui(self.screen)

    def release(self):
        pass