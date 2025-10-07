import pygame
import cv2
import math
import time
from PIL import Image

pygame.init()
pygame.mixer.init()

video_bg_paths = [
    r"assets\videos\0.mp4",
    r"assets\videos\1.mp4",
    r"assets\videos\2.mp4",
    r"assets\videos\3.mp4",
    r"assets\videos\4.mp4",
    r"assets\videos\5.mp4"
]
video_bg_rev_paths = [
    r"assets\videos\1_rev.mp4",
    r"assets\videos\2_rev.mp4",
    r"assets\videos\3_rev.mp4",
    r"assets\videos\4_rev.mp4"
]

gif_button_exit_path = r"assets\images\buttonExit.gif"
image_button_start_paths = [r"assets\images\startButton.png", r"assets\images\aroundButton.png"]
image_human_selector_paths = [r"assets\images\humanSelector.png", r"assets\images\clickedhumanselector.png", r"assets\images\aroundButton.png"]
image_AI_selector_paths = [r"assets\images\buttonAISelector.png", r"assets\images\clickedAISelector.png", r"assets\images\aroundButton.png"]
image_button_level_paths = [r"assets\images\buttonLevel.png", r"assets\images\aroundButton.png"]


music_bg_path = r"sounds\FrenchFuse-Space-YouTube.mp3"
pygame.mixer.music.load(music_bg_path)

sound_clicked_button_path = r"sounds\buttonClicked.mp3"

class QuantumInt():
    def __eq__(self, value):
        return isinstance(value, int)

class ExtraFunc():
    def __init__(self):
        pass
    def normalize_speed(self, d, s):
        if d <= s:
            return d
        frac, interger = math.modf(round(d / s, 5))
        if frac >= 0.5:
            s = d / (interger + 1)
        elif 0 < frac < 0.5:
            s = d / (interger - 1)
        return s
    def direction(self, a):
        if a != 0:
            return a / abs(a)
        else:
            return a
    def distance(self, a, b):
        dx = (b[0] - a[0])**2
        dy = (b[1] - a[1])**2
        d = math.sqrt(dx + dy)
        return round(d, 5)
            
all_frame = QuantumInt()
extra_func = ExtraFunc()

scenes = [{
            "video_bg_path": video_bg_paths[0],
            "init" : {"ButtonExit" : 0, "TextContinue" : 0},
            "remove" : [],
            "remain" : ["music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : all_frame,
                    "music_bg" : all_frame,
                    "ButtonExit" : all_frame,
                    "TextContinue" : all_frame
                }, 
                "MOUSE1" : {
                    "ButtonExit" : all_frame
                },
                "MOUSE" : {
                    "ButtonExit" : all_frame
                }
            }
        }, {
            "video_bg_path": video_bg_paths[1],
            "init" : {"ButtonStart" : -1, "TextEsc" : -1},
            "remove" : ["ButtonExit", "TextContinue"],
            "remain" : ["music_bg"],
            "event" : {
                "MOUSE1" : {
                    "ButtonStart" : -1,
                    "scene" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonStart" : -1
                }
            }
        }, {
            "video_bg_path": video_bg_paths[2],
            "init" : {"ButtonHumanSelector" : -1, "ButtonAISelector" : -1, "TextDetailMode" : -1},
            "remove" : ["ButtonStart"],
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "MOUSE1" : {
                    "scene" : -1,
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                },
                "MOUSE" : {
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                }
            }
        }, {
            "video_bg_path": video_bg_paths[3],
            "init" : {"ButtonLevel1" : -1, "TextDetailLevel" : -1},
            "remove" : ["ButtonHumanSelector", "ButtonAISelector", "TextDetailMode"],
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonLevel1" : -1
                },
                "MOUSE" : {
                    "ButtonLevel1" : -1,
                    "TextDetailLevel" : -1
                },
                "MOUSE1" : {
                    "scene" : -1,
                    "ButtonLevel1" : -1,
                    "TextDetailLevel" : -1
                }
            }
        }, {
            "video_bg_path": video_bg_paths[4],
            "init" : {"TextPlay" : 0},
            "remove" : ["ButtonLevel1", "TextDetailLevel", "TextEsc"],
            "remain" : ["music_bg"],
            "event" : {
                "end_frame" : {
                    "scene" : -1
                },
                "ENTER" : {
                    "play" : all_frame
                }
            }
        }, {
            "video_bg_path": video_bg_paths[5],
            "init" : {"TextEsc" : 0},
            "remove" : [],
            "remain" : ["music_bg", "TextPlay"],
            "event" : {
                "K_ESCAPE" : {
                    "scene" : all_frame
                },
                "end_frame" : {
                    "loop" : -1
                },
                "ENTER" : {
                    "play" : all_frame
                }
            }
        }
]

scenes_rev = [{
            "video_bg_rev_path": video_bg_rev_paths[0],
            "init" : {"ButtonExit" : -1, "TextContinue" : -1},
            "remove" : ["ButtonStart", "TextEsc"],
            "remain" : ["music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : -1,
                    "ButtonExit" : -1,
                    "TextContinue" : -1,
                },
                "MOUSE1" : {
                    "ButtonExit" : -1
                },
                "MOUSE" : {
                    "ButtonExit" : -1
                }
            }
        }, {
            "video_bg_rev_path": video_bg_rev_paths[1],
            "init" : {"ButtonStart" : -1},
            "remove" : ["ButtonHumanSelector", "ButtonAISelector", "TextDetailMode"],
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "MOUSE1" : {
                    "ButtonStart" : -1,
                    "scene" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonStart" : -1
                }
            }
        }, {
            "video_bg_rev_path": video_bg_rev_paths[2],
            "init" : {"ButtonHumanSelector" : -1, "ButtonAISelector" : -1, "TextDetailMode" : -1},
            "remove" : ["ButtonLevel1", "TextDetailLevel"],
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "MOUSE1" : {
                    "scene" : -1,
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                },
                "MOUSE" : {
                    "ButtonHumanSelector" : -1,
                    "ButtonAISelector" : -1,
                    "TextDetailMode" : -1
                }
            }
        }, {
            "video_bg_rev_path": video_bg_rev_paths[3],
            "init" : {"ButtonLevel1" : -1, "TextDetailLevel" : -1},
            "remove" : ["TextPlay"],
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "K_ESCAPE" : {
                    "scene" : -1,
                    "ButtonLevel1" : -1,
                    "TextDetailLevel" : -1
                },
                "MOUSE" : {
                    "ButtonLevel1" : -1,
                    "TextDetailLevel" : -1
                },
                "MOUSE1" : {
                    "scene" : -1,
                    "ButtonLevel1" : -1,
                    "TextDetailLevel" : -1
                }
            }
        }
]

def select_scenes(index):
    if index >= 0:
        return scenes
    else:
        return scenes_rev

class Menu():
    def __init__(self, window):
        self.window = window
        self.screen = window.screen

        self.cap = None
        self.last_frame_surface = None
        self.width = self.height = 0

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.window.set_data("fps", 30)

        self.scenes = scenes
        self.index_scene = 0

        self.index_frame_video_bg = None

        self.button_start = None
        self.button_exit = ButtonExit(self.window)
        self.text_continue = TextContinue(self.window)
        self.text_esc = None
        self.button_human_selector = None
        self.button_AI_selector = None
        self.text_detail_mode = None
        self.button_level_1 = None
        self.text_detail_level = None
        self.text_play = None

        self.music_bg_is_running = False
        self.is_back = self.window.get_data("menu_back")
        if self.is_back:
            self.button_exit = None
            self.text_continue = None
            self.scenes = scenes_rev
            self.index_scene = 3
            pygame.mixer.music.play(-1)
            self.music_bg_is_running = True
            self.is_back = False
            self.window.set_data("menu_back", False)
            self.set_background(self.scenes[self.index_scene]["video_bg_rev_path"])
        else:
            self.set_background(self.scenes[self.index_scene]["video_bg_path"])

    def handle_events(self, event):
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and "K_SPACE" in self.scenes[self.index_scene]["event"]:
                k_space_event_in_scene = self.scenes[self.index_scene]["event"]["K_SPACE"]
                if "scene" in k_space_event_in_scene and k_space_event_in_scene.get("scene") == self.index_frame_video_bg:
                    self.scenes = scenes
                    self.index_scene += 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_path"])
                if "music_bg" in k_space_event_in_scene and k_space_event_in_scene.get("music_bg") == self.index_frame_video_bg and not self.music_bg_is_running:
                    pygame.mixer.music.play(-1)
                    self.music_bg_is_running = False
                if "ButtonExit" in k_space_event_in_scene and k_space_event_in_scene.get("ButtonExit") == self.index_frame_video_bg and self.button_exit:
                    self.button_exit.space_action()


            if event.key == pygame.K_ESCAPE and "K_ESCAPE" in self.scenes[self.index_scene]["event"]:
                k_esc_event_in_scene = self.scenes[self.index_scene]["event"]["K_ESCAPE"]
                if "scene" in k_esc_event_in_scene and k_esc_event_in_scene.get("scene") == self.index_frame_video_bg:
                    self.scenes = scenes_rev
                    self.index_scene -= 1
                    while self.index_scene > len(self.scenes) - 1:
                        self.index_scene -= 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_rev_path"])
                buttons = {
                    "ButtonStart" : self.button_start,
                    "ButtonHumanSelector" : self.button_human_selector,
                    "ButtonAISelector" : self.button_AI_selector,
                    "ButtonLevel1" : self.button_level_1
                }
                for name, button in buttons.items():
                    if name in k_esc_event_in_scene and k_esc_event_in_scene.get(name) == self.index_frame_video_bg and button:
                        button.escape_action()

            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and "ENTER" in self.scenes[self.index_scene]["event"]:
                enter_event_in_scene = self.scenes[self.index_scene]["event"]["ENTER"]
                if "play" in enter_event_in_scene and enter_event_in_scene.get("play") == self.index_frame_video_bg:
                    self.window.set_data("status_screen", "gameplay")
                    pygame.mixer.music.fadeout(2000)
                    self.music_bg_is_running = False

        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and "MOUSE1" in self.scenes[self.index_scene]["event"]:
                mouse1_event_in_scene = self.scenes[self.index_scene]["event"]["MOUSE1"]
                pos = pygame.mouse.get_pos()

                if "scene" in mouse1_event_in_scene and mouse1_event_in_scene.get("scene") == self.index_frame_video_bg:    

                    buttons = {
                        "ButtonStart" : self.button_start, 
                        "ButtonHumanSelector" : self.button_human_selector, 
                        "ButtonAISelector" : self.button_AI_selector, 
                        "ButtonLevel1" : self.button_level_1
                    }

                    for name, button in buttons.items():
                        if name in mouse1_event_in_scene and mouse1_event_in_scene.get(name) == self.index_frame_video_bg:
                            if button and button.check_collided(pos):
                                button.run_music()
                                for button in buttons.values():
                                    if button:
                                       button.clicked()
                                       if button.check_collided(pos) and (name == "ButtonHumanSelector" or name == "ButtonAISelector"):
                                           button.set_data()
                                self.scenes = scenes
                                self.index_scene += 1
                                self.set_background(self.scenes[self.index_scene]["video_bg_path"])
                                break              

                if "ButtonExit" in mouse1_event_in_scene and mouse1_event_in_scene.get("ButtonExit") == self.index_frame_video_bg and self.button_exit.check_collided(pos):
                    self.button_exit.run_music()
                    return False
        
        if not event:
            if "end_frame" in self.scenes[self.index_scene]["event"]:
                end_frame_event_in_scene = self.scenes[self.index_scene]["event"]["end_frame"]
                if "scene" in end_frame_event_in_scene and end_frame_event_in_scene.get("scene") == self.index_frame_video_bg:
                    self.scenes = scenes
                    self.index_scene += 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_path"])
                if "loop" in end_frame_event_in_scene and end_frame_event_in_scene.get("loop") == self.index_frame_video_bg:
                    self.set_background(self.scenes[self.index_scene]["video_bg_path"])
            if "MOUSE" in self.scenes[self.index_scene]["event"]:
                mouse_event_in_scene = self.scenes[self.index_scene]["event"]["MOUSE"]
                pos = pygame.mouse.get_pos()
                if "ButtonExit" in mouse_event_in_scene and mouse_event_in_scene.get("ButtonExit") == self.index_frame_video_bg and self.button_exit:
                    if self.button_exit.check_collided(pos):
                        self.button_exit.change_color_text((0,0,0))
                    else:
                        self.button_exit.change_color_text()
                if "TextDetailMode" in mouse_event_in_scene and mouse_event_in_scene.get("TextDetailMode") == self.index_frame_video_bg and self.text_detail_mode:
                    buttons = {
                        "ButtonHumanSelector" : [self.button_human_selector, "Chế độ người chơi"],
                        "ButtonAISelector" : [self.button_AI_selector, "Chế độ máy chơi"]
                    }
                    for name, infor in buttons.items():
                        button = infor[0]
                        text = infor[1]
                        if name in mouse_event_in_scene and mouse_event_in_scene.get(name) == self.index_frame_video_bg and button:
                            if button.check_collided(pos):
                                button.change_image(1)
                                self.text_detail_mode.change_text(text)
                                break
                            else:
                                button.change_image()
                                self.text_detail_mode.change_text()

                if "TextDetailLevel" in mouse_event_in_scene and mouse_event_in_scene.get("TextDetailLevel") == self.index_frame_video_bg and self.text_detail_level:
                    buttons = {
                        "ButtonLevel1" : [self.button_level_1, "Cấp độ dễ"],
                    }
                    for name, infor in buttons.items():
                        button = infor[0]
                        text = infor[1]
                        if name in mouse_event_in_scene and mouse_event_in_scene.get(name) == self.index_frame_video_bg and button:
                            if button.check_collided(pos):
                                button.change_color_text((255, 0, 0))
                                self.text_detail_level.change_text(text)
                                break
                            else:
                                button.change_color_text()
                                self.text_detail_level.change_text()

        return True

    def set_background(self, video_path):
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(video_path)
        self.last_frame_surface = None

        if self.width != int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or self.height != int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)):
            self.width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.window.set_data("screen_size", (self.width, self.height))

    def draw_background(self):

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            if self.index_frame_video_bg is None:
                self.index_frame_video_bg = 0
            else:
                self.index_frame_video_bg += 1
            self.last_frame_surface = frame
        else:
            frame = self.last_frame_surface
            self.index_frame_video_bg = -1

        if frame is not None:
            self.screen.blit(frame, (0, 0))

    def draw_ui(self):
        t = time.perf_counter()*1000

        text_list = [
            self.text_continue, 
            self.text_esc, 
            self.text_detail_mode, 
            self.text_detail_level, 
            self.text_play
        ]
        for text in text_list:
            if text:
                text.draw(t)

        buttons = {
            self.button_start : None,
            self.button_exit : self.fps,
            self.button_human_selector : None,
            self.button_AI_selector : None,
            self.button_level_1 : None
        }
        for button, para in buttons.items():
            if button and para:
                button.effect_movement(para)
            elif button:
                button.effect_movement()

    def run(self):
        self.draw_background()
        self.transition_object()
        self.draw_ui()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def update_object(self, name, type, object):
        current_scene_config = self.scenes[self.index_scene]
        if type == "button":
            if name in current_scene_config["init"] and self.index_frame_video_bg == current_scene_config["init"][name] and object is None:
                if name == "ButtonStart":
                    object = ButtonStart(self.window)
                elif name == "ButtonExit":
                    object = ButtonExit(self.window)
                elif name == "ButtonHumanSelector":
                    object = ButtonHumanSelector(self.window)
                elif name == "ButtonAISelector":
                    object = ButtonAISelector(self.window)
                elif name == "ButtonLevel1":
                    object = ButtonLevel(self.window, 1, 80)
            elif name in current_scene_config["remove"] and object is not None and object.out_screen:
                object = None
        elif type == "text":
            if name in current_scene_config["init"] and self.index_frame_video_bg == current_scene_config["init"][name] and object is None:
                if name == "TextContinue":
                    object = TextContinue(self.window)
                elif name == "TextEsc":
                    object = TextEsc(self.window)
                elif name == "TextDetailMode":
                    object = TextDetailMode(self.window)
                elif name == "TextDetailLevel":
                    object = TextDetailLevel(self.window)
                elif name == "TextPlay":
                    object = TextPlay(self.window)
                
            elif name in current_scene_config["remove"] and object is not None:
                object = None

        return object

    def transition_object(self):

        self.button_start = self.update_object("ButtonStart", "button", self.button_start)
        self.button_exit = self.update_object("ButtonExit", "button", self.button_exit)
        
        self.text_continue = self.update_object("TextContinue", "text", self.text_continue)
        self.text_esc = self.update_object("TextEsc", "text", self.text_esc)
        self.text_detail_mode = self.update_object("TextDetailMode", "text", self.text_detail_mode)
        self.text_detail_level = self.update_object("TextDetailLevel", "text", self.text_detail_level)
        self.text_play = self.update_object("TextPlay", "text", self.text_play)

        self.button_human_selector = self.update_object("ButtonHumanSelector", "button", self.button_human_selector)
        self.button_AI_selector = self.update_object("ButtonAISelector", "button", self.button_AI_selector)
        
        self.button_level_1 = self.update_object("ButtonLevel1", "button", self.button_level_1)

    def release(self):
        if self.cap is not None:
            self.cap.release()

class ButtonStart():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.image_main_ori = pygame.image.load(image_button_start_paths[0]).convert_alpha()
        self.image_main_size = (120, 120)
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect()

        self.scenes = None

        self.image_around_ori = pygame.image.load(image_button_start_paths[1]).convert_alpha()
        self.image_around_size = (180, 180)

        self.image_around = pygame.transform.scale(self.image_around_ori, self.image_around_size)
        self.rect_around = self.image_around.get_rect()
        
        self.pos_init_center = (-100, 160)
        self.pos_goal_center = (200, 160)
        self.pos_current_center = self.pos_init_center

        self.rect_main.center = self.pos_current_center
        self.rect_around.center = self.rect_main.center

        self.angle = 0

        self.zoom_init_rate = 0.7
        self.zoom_goal_rate = 1.0
        self.zoom_current_rate = self.zoom_init_rate

        self.image_around_rotated = self.image_around
        self.image_around_rotated_rect = self.image_around_rotated.get_rect()

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)
        self.out_screen = True

    def set_out_screen(self):
        if self.pos_current_center[0] <= - (self.image_around.get_size()[0] / 2):
            self.out_screen = True
        else:
            self.out_screen = False

    def escape_action(self):
        self.clicked()

    def clicked(self):
        self.pos_init_center, self.pos_goal_center = self.pos_goal_center, self.pos_init_center
        self.zoom_init_rate, self.zoom_goal_rate = self.zoom_goal_rate, self.zoom_init_rate

    def check_collided(self, pos):
        return self.rect_main.collidepoint(pos)
    
    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self, speed=10, speed_angle=4, speed_zoom=0.01):
        speed = extra_func.normalize_speed(extra_func.distance(self.pos_init_center, self.pos_goal_center), speed)
        distance_zoom = round(abs(self.zoom_goal_rate - self.zoom_init_rate), 5)
        speed_zoom = extra_func.normalize_speed(distance_zoom, speed_zoom)
        
        dx = round(self.pos_goal_center[0] - self.rect_main.centerx, 5)
        d = extra_func.direction(dx)
        self.rect_main.centerx += speed*d
        self.rect_around.centerx = self.rect_main.centerx

        self.pos_current_center = self.rect_main.center

        dz = round(self.zoom_goal_rate - self.zoom_current_rate, 5)
        d = extra_func.direction(dz)
        self.zoom_current_rate += speed_zoom*d


        if self.angle >= 360:
            self.angle = 0
        self.angle += speed_angle

        self.image_around = pygame.transform.scale(self.image_around_ori, (int(self.image_around_size[0]*self.zoom_current_rate), int(self.image_around_size[1]*self.zoom_current_rate)))
        self.rect_around = self.image_around.get_rect(center=self.rect_around.center)

        self.set_out_screen()
        
        self.image_around_rotated = pygame.transform.rotate(self.image_around, self.angle)
        self.image_around_rotated_rect = self.image_around_rotated.get_rect(center=self.rect_around.center)

        self.screen.blit(self.image_around_rotated, self.image_around_rotated_rect)
        self.screen.blit(self.image_main, self.rect_main)

class ButtonExit():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.gif_path = gif_button_exit_path
        self.size = (100, 100)
        self.frames = self.load_gif_frames()
        self.frame_index = 0

        self.fps = 10
        self.counter = 0

        self.pos_goal_center = (60, 650)
        self.init_pos = (-100, 650)
        self.pos_current_center = self.init_pos

        self.out_screen = True

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)
        self.font = pygame.font.SysFont("Arial", 18, True)
        self.text_exit = self.font.render("Exit", True, (255,255,255))
        self.text_exit_rect = self.text_exit.get_rect(center=self.pos_current_center)
        self.rect = self.frames[0].get_rect(center=(self.pos_current_center[0], self.pos_current_center[1]))

    def change_color_text(self, color=None):
        if color is None:
            color = (255,255,255)
        self.text_exit = self.font.render("Exit", True, color)
        self.text_exit_rect = self.text_exit.get_rect(center=self.pos_current_center)

    def set_out_screen(self):
        if self.pos_current_center[0] <= - (self.size[0] / 2):
            self.out_screen = True
        else:
            self.out_screen = False

    def space_action(self):
        self.init_pos, self.pos_goal_center = self.pos_goal_center, self.init_pos

    def effect_movement(self, fps, speed=10):
        self.counter += 1
        if self.counter >= round(fps / self.fps):
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        dx = round(self.pos_goal_center[0] - self.pos_current_center[0], 5)
        d = extra_func.direction(dx)

        speed = extra_func.normalize_speed(extra_func.distance(self.init_pos, self.pos_goal_center), speed)

        self.rect.centerx += speed*d

        self.pos_current_center = self.rect.center

        self.set_out_screen()

        rect = self.frames[self.frame_index].get_rect(center=self.rect.center)
        self.text_exit_rect = self.text_exit.get_rect(center=self.rect.center)

        self.screen.blit(self.frames[self.frame_index], rect)
        self.screen.blit(self.text_exit, self.text_exit_rect)
    
    def run_music(self):
        self.clicked_sound.play()
    
    def check_collided(self, pos):
        return self.rect.collidepoint(pos) or self.text_exit_rect.collidepoint(pos)
    
    def load_gif_frames(self):
        pil_img = Image.open(self.gif_path)
        frames = []
        try:
            while True:
                frame = pil_img.convert("RGBA")
                mode = frame.mode
                frame = frame.resize(self.size)
                data = frame.tobytes()
                surface = pygame.image.fromstring(data, frame.size, mode)
                frames.append(surface.copy())
                pil_img.seek(pil_img.tell() + 1)
        except EOFError:
            pass
        return frames

class TextContinue():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.text = "Nhấn SPACE để tiếp tục..."
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (650, 690)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self, t, speed_time=500):
        if (t // speed_time) % 2 == 0:
            self.screen.blit(self.image, self.rect)

class TextEsc():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.text = "Nhấn ESC để quay lại..."
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (1180, 20)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self, t, speed_time=500):
        if (t // speed_time) % 2 == 0:
            self.screen.blit(self.image, self.rect)

class TextDetailMode():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.text_ori = "Chọn chế độ"
        self.text = self.text_ori
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (650, 690)
        self.rect = self.image.get_rect(center=self.pos_center)

    def change_text(self, text=None):
        if text:
            self.text = text
        else:
            self.text = self.text_ori
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self, t, speed_time=500):
        if (t // speed_time) % 2 == 0:    
            self.screen.blit(self.image, self.rect)

class ButtonHumanSelector():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        
        self.index = 0
        
        self.image_main_ori = pygame.image.load(image_human_selector_paths[self.index]).convert_alpha()
        self.image_main_size = (80, 80)
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect()

        self.image_around_ori = pygame.image.load(image_human_selector_paths[2]).convert_alpha()
        self.image_around_size = (150, 150)
        self.image_around = pygame.transform.scale(self.image_around_ori, self.image_around_size)
        self.rect_around = self.image_around.get_rect()

        self.pos_init_center = (720, -80)
        self.pos_goal_center = (720, 120)
        self.pos_current_center = self.pos_init_center
        self.rect_main.center = self.pos_current_center
        self.rect_around.center = self.rect_main.center

        self.zoom_init_rate = 0.8
        self.zoom_goal_rate = 1.0
        self.zoom_current_rate = self.zoom_init_rate

        self.image_around_rotated = self.image_around
        self.image_around_rotated_rect = self.image_around_rotated.get_rect()

        self.angle = 0

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)

        self.out_screen = True

    def escape_action(self):
        self.clicked()

    def set_out_screen(self):
        if self.pos_current_center[1] <= -(self.image_around_size[1] / 2):
            self.out_screen = True
        else:
            self.out_screen = False

    def clicked(self):
        self.pos_init_center, self.pos_goal_center = self.pos_goal_center, self.pos_init_center
        self.zoom_init_rate, self.zoom_goal_rate = self.zoom_goal_rate, self.zoom_init_rate

    def set_data(self):
        self.window.set_data("mode", "human")

    def change_image(self, index=0):
        self.index = index
        self.image_main_ori = pygame.image.load(image_human_selector_paths[self.index]).convert_alpha()
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect(center=self.rect_main.center)

    def check_collided(self, pos):
        return self.rect_main.collidepoint(pos)

    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self, speed=10, speed_angle=4, speed_zoom=0.01):
        speed = extra_func.normalize_speed(extra_func.distance(self.pos_init_center, self.pos_goal_center), speed)
        distance_zoom = round(abs(self.zoom_goal_rate - self.zoom_init_rate), 5)
        speed_zoom = extra_func.normalize_speed(distance_zoom, speed_zoom)

        dx = round(self.pos_goal_center[1] - self.rect_main.centery, 5)
        d = extra_func.direction(dx)
        self.rect_main.centery += speed*d
        self.rect_around.centery = self.rect_main.centery

        self.pos_current_center = self.rect_main.center

        dz = round(self.zoom_goal_rate - self.zoom_current_rate, 5)
        d = extra_func.direction(dz)
        self.zoom_current_rate += speed_zoom*d


        if self.angle >= 360:
            self.angle = 0
        self.angle += speed_angle

        self.image_around = pygame.transform.scale(self.image_around_ori, (int(self.image_around_size[0]*self.zoom_current_rate), int(self.image_around_size[1]*self.zoom_current_rate)))
        self.rect_around = self.image_around.get_rect(center=self.rect_around.center)

        self.set_out_screen()
        
        self.image_around_rotated = pygame.transform.rotate(self.image_around, self.angle)
        self.image_around_rotated_rect = self.image_around_rotated.get_rect(center=self.rect_around.center)

        self.screen.blit(self.image_around_rotated, self.image_around_rotated_rect)
        self.screen.blit(self.image_main, self.rect_main)

class ButtonAISelector():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        
        self.index = 0
        
        self.image_main_ori = pygame.image.load(image_AI_selector_paths[self.index]).convert_alpha()
        self.image_main_size = (80, 80)
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect()

        self.image_around_ori = pygame.image.load(image_AI_selector_paths[2]).convert_alpha()
        self.image_around_size = (150, 150)
        self.image_around = pygame.transform.scale(self.image_around_ori, self.image_around_size)
        self.rect_around = self.image_around.get_rect()

        self.pos_init_center = (1150, 800)
        self.pos_goal_center = (1150, 600)
        self.pos_current_center = self.pos_init_center
        self.rect_main.center = self.pos_current_center
        self.rect_around.center = self.rect_main.center

        self.zoom_init_rate = 0.8
        self.zoom_goal_rate = 1.0
        self.zoom_current_rate = self.zoom_init_rate

        self.image_around_rotated = self.image_around
        self.image_around_rotated_rect = self.image_around_rotated.get_rect()

        self.angle = 0

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)

        self.out_screen = True

    def escape_action(self):
        self.clicked()

    def set_out_screen(self):
        sizey = round(self.screen.get_size()[1] + (self.image_around_size[1] / 2))
        if self.pos_current_center[1] >= sizey:
            self.out_screen = True
        else:
            self.out_screen = False

    def clicked(self):
        self.pos_init_center, self.pos_goal_center = self.pos_goal_center, self.pos_init_center
        self.zoom_init_rate, self.zoom_goal_rate = self.zoom_goal_rate, self.zoom_init_rate

    def set_data(self):
        self.window.set_data("mode", "AI")

    def change_image(self, index=0):
        self.index = index
        self.image_main_ori = pygame.image.load(image_AI_selector_paths[self.index]).convert_alpha()
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect(center=self.rect_main.center)

    def check_collided(self, pos):
        return self.rect_main.collidepoint(pos)

    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self, speed=10, speed_angle=4, speed_zoom=0.01):
        speed = extra_func.normalize_speed(extra_func.distance(self.pos_init_center, self.pos_goal_center), speed)
        distance_zoom = round(abs(self.zoom_goal_rate - self.zoom_init_rate), 5)
        speed_zoom = extra_func.normalize_speed(distance_zoom, speed_zoom)

        dx = round(self.pos_goal_center[1] - self.rect_main.centery, 5)
        d = extra_func.direction(dx)
        self.rect_main.centery += speed*d
        self.rect_around.centery = self.rect_main.centery

        self.pos_current_center = self.rect_main.center

        dz = round(self.zoom_goal_rate - self.zoom_current_rate, 5)
        d = extra_func.direction(dz)
        self.zoom_current_rate += speed_zoom*d


        if self.angle >= 360:
            self.angle = 0
        self.angle += speed_angle

        self.image_around = pygame.transform.scale(self.image_around_ori, (int(self.image_around_size[0]*self.zoom_current_rate), int(self.image_around_size[1]*self.zoom_current_rate)))
        self.rect_around = self.image_around.get_rect(center=self.rect_around.center)

        self.set_out_screen()
        
        self.image_around_rotated = pygame.transform.rotate(self.image_around, self.angle)
        self.image_around_rotated_rect = self.image_around_rotated.get_rect(center=self.rect_around.center)

        self.screen.blit(self.image_around_rotated, self.image_around_rotated_rect)
        self.screen.blit(self.image_main, self.rect_main)

class ButtonLevel():
    def __init__(self, window, level, centerx):
        self.window = window
        self.screen = self.window.screen
        self.level = level
        self.centerx = centerx

        self.image_main_size = (90, 90)
        self.image_main_ori = pygame.image.load(image_button_level_paths[0]).convert_alpha()
        self.image_main = pygame.transform.scale(self.image_main_ori, self.image_main_size)
        self.rect_main = self.image_main.get_rect()

        self.image_around_size = (120, 120)
        self.image_around_ori = pygame.image.load(image_button_level_paths[1]).convert_alpha()
        self.image_around = pygame.transform.scale(self.image_around_ori, self.image_around_size)
        self.rect_around = self.image_around.get_rect()

        self.font = pygame.font.SysFont("Arial", 22, True)
        self.text = f"{self.level}"
        self.image_text = self.font.render(self.text, True, (255,255,255))
        self.text_rect = self.image_text.get_rect()

        self.pos_init_center = (self.centerx, -90)
        self.pos_goal_center = (self.centerx, 90)
        self.pos_current_center = self.pos_init_center

        self.rect_main.center = self.pos_current_center
        self.rect_around.center = self.rect_main.center
        self.text_rect.center = self.rect_main.center

        self.angle = 0

        self.zoom_init_rate = 0.8
        self.zoom_goal_rate = 1.0
        self.zoom_current_rate = self.zoom_init_rate

        self.image_around_rotated = self.image_around
        self.image_around_rotated_rect = self.image_around_rotated.get_rect()

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)
        self.out_screen = True

    def set_out_screen(self):
        if self.pos_current_center[1] <= -(self.image_around_size[1] / 2):
            self.out_screen = True
        else:
            self.out_screen = False

    def change_color_text(self, color=None):
        if color is None:
            color = (255,255,255)
        self.image_text = self.font.render(self.text, True, color)
        self.text_rect = self.image_text.get_rect(center=self.pos_current_center)


    def escape_action(self):
        self.clicked()

    def clicked(self):
        self.pos_init_center, self.pos_goal_center = self.pos_goal_center, self.pos_init_center
        self.zoom_init_rate, self.zoom_goal_rate = self.zoom_goal_rate, self.zoom_init_rate
        self.set_data()

    def set_data(self):
        self.window.set_data("level", self.level)

    def check_collided(self, pos):
        return self.rect_main.collidepoint(pos)

    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self, speed=10, speed_angle=4, speed_zoom=0.01):
        speed = extra_func.normalize_speed(extra_func.distance(self.pos_init_center, self.pos_goal_center), speed)
        distance_zoom = round(abs(self.zoom_goal_rate - self.zoom_init_rate), 5)
        speed_zoom = extra_func.normalize_speed(distance_zoom, speed_zoom)

        dx = round(self.pos_goal_center[1] - self.rect_main.centery, 5)
        d = extra_func.direction(dx)
        self.rect_main.centery += speed*d
        self.rect_around.centery = self.rect_main.centery

        self.pos_current_center = self.rect_main.center

        dz = round(self.zoom_goal_rate - self.zoom_current_rate, 5)
        d = extra_func.direction(dz)
        self.zoom_current_rate += speed_zoom*d


        if self.angle >= 360:
            self.angle = 0
        self.angle += speed_angle

        self.image_around = pygame.transform.scale(self.image_around_ori, (int(self.image_around_size[0]*self.zoom_current_rate), int(self.image_around_size[1]*self.zoom_current_rate)))
        self.rect_around = self.image_around.get_rect(center=self.rect_around.center)

        self.text_rect.center = self.pos_current_center

        self.set_out_screen()
        
        self.image_around_rotated = pygame.transform.rotate(self.image_around, self.angle)
        self.image_around_rotated_rect = self.image_around_rotated.get_rect(center=self.rect_around.center)

        self.screen.blit(self.image_around_rotated, self.image_around_rotated_rect)
        self.screen.blit(self.image_main, self.rect_main)
        self.screen.blit(self.image_text, self.text_rect)

class TextDetailLevel():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.text_ori = "Chọn cấp độ chơi"
        self.text = self.text_ori
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (650, 690)
        self.rect = self.image.get_rect(center=self.pos_center)

    def change_text(self, text=None):
        if text:
            self.text = text
        else:
            self.text = self.text_ori
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self, t, speed_time=500):
        if (t // speed_time) % 2 == 0:    
            self.screen.blit(self.image, self.rect)

class TextPlay():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.text_ori = "Nhấn Enter để chơi"
        self.text = self.text_ori
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (650, 690)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self, t, speed_time=500):
        if (t // speed_time) % 2 == 0:    
            self.screen.blit(self.image, self.rect)
