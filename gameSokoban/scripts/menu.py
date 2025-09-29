import pygame
import cv2
import math
from PIL import Image

pygame.mixer.init()

video_bg_paths = [
    r"assets\videos\0.mp4",
    r"assets\videos\1.mp4",
    r"assets\videos\2.mp4",
    r"assets\videos\3.mp4"
]
video_bg_rev_paths = [
    r"assets\videos\1_rev.mp4",
    r"assets\videos\2_rev.mp4",
    r"assets\videos\3_rev.mp4"
]

image_button_start_paths = [r"assets\images\startButton.png", r"assets\images\aroundButtonStart.png"]
gif_button_exit_path = r"assets\images\buttonExit.gif"
image_human_selector_paths = [r"assets\images\humanSelector.png", r"assets\images\clickedhumanselector.png"]

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
            "remove" : {},
            "remain" : ["music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : all_frame,
                    "music_bg" : all_frame
                }, 
                "MOUSE1" : {
                    "ButtonExit" : all_frame
                }
            }
        }, {
            "video_bg_path": video_bg_paths[1],
            "init" : {"ButtonStart" : -1, "TextEsc" : 0},
            "remove" : {"ButtonExit" : 0, "TextContinue" : 0},
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
            "init" : {"TextContinue" : 0},
            "remove" : {"ButtonStart" : 0},
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1
                }
            }
        }, {
            "video_bg_path": video_bg_paths[3],
            "init" : {},
            "remove" : {"TextContinue" : 0},
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "K_ESCAPE" : {
                    "scene" : -1
                }
            }
        }]

scenes_rev = [{
            "video_bg_rev_path": video_bg_rev_paths[0],
            "init" : {"ButtonExit" : -1, "TextContinue" : 0},
            "remove" : {"ButtonStart" : 0, "TextEsc" : 0},
            "remain" : ["music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : -1
                },
                "MOUSE1" : {
                    "ButtonExit" : -1
                }
            }
        }, {
            "video_bg_rev_path": video_bg_rev_paths[1],
            "init" : {"ButtonStart" : -1},
            "remove" : {"TextContinue" : 0},
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
            "init" : {"TextContinue" : 0},
            "remove" : {},
            "remain" : ["TextEsc", "music_bg"],
            "event" : {
                "K_SPACE" : {
                    "scene" : -1
                },
                "K_ESCAPE" : {
                    "scene" : -1
                }
            }
        }]

def select_scenes(index):
    if index >= 0:
        return scenes
    else:
        return scenes_rev

class Menu():
    def __init__(self, window):
        self.window = window
        self.screen = window.screen
        self.window.set_data("status_screen", "menu")

        self.cap = None
        self.last_frame_surface = None
        self.width = self.height = 0

        self.clock = pygame.time.Clock()

        self.scenes = scenes
        self.index_scene = 0

        self.index_frame_video_bg = None

        self.button_start = None
        self.button_exit = ButtonExit(self.screen, None)
        self.text_continue = TextContinue(self.screen)
        self.text_esc = None

        self.music_bg_is_running = False

        self.set_background(self.scenes[self.index_scene]["video_bg_path"])

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and "K_SPACE" in self.scenes[self.index_scene]["event"]:
                k_space_event_in_scene = self.scenes[self.index_scene]["event"]["K_SPACE"]
                if "scene" in k_space_event_in_scene and k_space_event_in_scene.get("scene") == self.index_frame_video_bg:
                    self.scenes = scenes
                    self.index_scene += 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_path"])
                if "music_bg" in k_space_event_in_scene and k_space_event_in_scene.get("music_bg") == self.index_frame_video_bg and not self.music_bg_is_running:
                    pygame.mixer.music.play(-1)
                    self.music_bg_is_running = False


            if event.key == pygame.K_ESCAPE and "K_ESCAPE" in self.scenes[self.index_scene]["event"]:
                k_esc_event_in_scene = self.scenes[self.index_scene]["event"]["K_ESCAPE"]
                if "scene" in k_esc_event_in_scene and k_esc_event_in_scene.get("scene") == self.index_frame_video_bg:
                    self.scenes = scenes_rev
                    self.index_scene -= 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_rev_path"])
                if "ButtonStart" in k_esc_event_in_scene and k_esc_event_in_scene.get("ButtonStart") == self.index_frame_video_bg:
                    self.button_start.clicked()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and "MOUSE1" in self.scenes[self.index_scene]["event"]:
                mouse1_event_in_scene = self.scenes[self.index_scene]["event"]["MOUSE1"]
                pos = pygame.mouse.get_pos()
                if "ButtonStart" in mouse1_event_in_scene and mouse1_event_in_scene.get("ButtonStart") == self.index_frame_video_bg and self.button_start.check_collided(pos):
                    self.button_start.run_music()
                    self.button_start.clicked()
                
                if "scene" in mouse1_event_in_scene and mouse1_event_in_scene.get("scene") == self.index_frame_video_bg and self.button_start.check_collided(pos):    
                    self.scenes = scenes
                    self.index_scene += 1
                    self.set_background(self.scenes[self.index_scene]["video_bg_path"])

                if "ButtonExit" in mouse1_event_in_scene and mouse1_event_in_scene.get("ButtonExit") == self.index_frame_video_bg and self.button_exit.check_collided(pos):
                    self.button_exit.run_music()
                    return False
        
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
        t = pygame.time.get_ticks()
        if self.text_continue:
            self.text_continue.draw(t)

        if self.text_esc:
            self.text_esc.draw(t)

        if self.button_start:
            self.button_start.effect_movement(self.scenes)
            #if self.button_start.rect_main.centerx <= self.button_start.pos_goal_center[0] and "ButtonStart" in self.scenes[self.index_scene]["remove"]:
                #self.button_start = None

        if self.button_exit:
            self.button_exit.effect_movement(self.index_scene, self.scenes)
            if self.button_exit.rect.centerx <= self.button_exit.pos_goal_center[0] and "ButtonExit" in self.scenes[self.index_scene]["remove"]:
                self.button_exit = None 

    def run(self):
        self.draw_background()
        self.transition_object()
        self.draw_ui()
        pygame.display.flip()
        self.clock.tick(30)

    def update_object(self, name, type, object):
        current_scene_config = self.scenes[self.index_scene]
        if type == "button":
            if name in current_scene_config["init"] and self.index_frame_video_bg == current_scene_config["init"][name] and object is None:
                if name == "ButtonStart":
                    #object = ButtonStart(self.screen, object)
                    object = ButtonStart(self.screen)
                elif name == "ButtonExit":
                    object = ButtonExit(self.screen, object)
            elif name in current_scene_config["remove"] and object is not None:
                if name == "ButtonStart" and object.out_screen:
                    #object = ButtonStart(self.screen, object)
                    object = None
                elif name == "ButtonExit" and self.index_frame_video_bg == current_scene_config["remove"][name]:
                    object = ButtonExit(self.screen, object)
        elif type == "text":
            if name in current_scene_config["init"] and self.index_frame_video_bg == current_scene_config["init"][name] and object is None:
                if name == "TextContinue":
                    object = TextContinue(self.screen)
                elif name == "TextEsc":
                    object = TextEsc(self.screen)
            elif name in current_scene_config["remove"] and self.index_frame_video_bg == current_scene_config["remove"][name] and object is not None:
                object = None

        return object

    def transition_object(self):

        self.button_start = self.update_object("ButtonStart", "button", self.button_start)
        self.button_exit = self.update_object("ButtonExit", "button", self.button_exit)
        
        self.text_continue = self.update_object("TextContinue", "text", self.text_continue)
        self.text_esc = self.update_object("TextEsc", "text", self.text_esc)

    def release(self):
        if self.cap is not None:
            self.cap.release()

class ButtonStart():
    def __init__(self, screen):
        self.screen = screen
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

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)
        self.out_screen = True

    def set_out_screen(self):
        if self.pos_current_center[0] <= - (self.image_around.get_size()[0] / 2) or self.pos_current_center[1] <= - (self.image_around.get_size()[1] / 2):
            self.out_screen = True
        else:
            self.out_screen = False

    def clicked(self):
        self.pos_init_center, self.pos_goal_center = self.pos_goal_center, self.pos_init_center
        self.zoom_init_rate, self.zoom_goal_rate = self.zoom_goal_rate, self.zoom_init_rate

    def check_collided(self, pos):
        return self.rect_main.collidepoint(pos)
    
    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self, scenes, speed=10, speed_around=4, speed_zoom=0.01):
        self.scenes = scenes
        speed = extra_func.normalize_speed(extra_func.distance(self.pos_init_center, self.pos_goal_center), speed)
        distance_zoom = round(self.pos_goal_center[0] - self.pos_current_center[0], 5)
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
        self.angle += speed_around

        self.image_around = pygame.transform.scale(self.image_around_ori, (int(self.image_around_size[0]*self.zoom_current_rate), int(self.image_around_size[1]*self.zoom_current_rate)))
        self.rect_around = self.image_around.get_rect(center=self.rect_around.center)

        self.set_out_screen()
        
        rotated = pygame.transform.rotate(self.image_around, self.angle)
        rect_rotated = rotated.get_rect(center=self.rect_around.center)

        self.screen.blit(rotated, rect_rotated)
        self.screen.blit(self.image_main, self.rect_main)

class ButtonExit():
    def __init__(self, screen, buttonExit_old):
        self.screen = screen
        self.buttonExit_old = buttonExit_old
        self.gif_path = gif_button_exit_path
        self.size = (100, 100)
        self.frames = self.load_gif_frames()
        self.frame_index = 0
        if self.buttonExit_old:
            self.frame_index = self.buttonExit_old.frame_index
        self.fps = 5
        self.counter = 0
        if self.buttonExit_old:
            self.counter = self.buttonExit_old.counter
        self.pos_goal_center = (60, 650)
        self.init_pos = (-100, 650)
        self.pos_current_center = self.init_pos
        if self.buttonExit_old:
            self.pos_goal_center = self.buttonExit_old.init_pos
            self.init_pos = self.buttonExit_old.pos_goal_center
            self.pos_current_center = self.buttonExit_old.pos_current_center

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)
        self.font = pygame.font.SysFont("Arial", 18)
        self.text_exit = self.font.render("Exit", True, (255,255,255))
        self.text_exit_rect = self.text_exit.get_rect(center=self.pos_current_center)
        self.rect = self.frames[0].get_rect(center=(self.pos_current_center[0], self.pos_current_center[1]))

    def effect_movement(self, index, scenes, speed=10):
        # đổi frame dựa theo fps
        self.counter += 1
        if self.counter >= self.fps:
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        if "ButtonExit" in scenes[index]["init"] and self.rect.centerx <= self.pos_goal_center[0]:
            self.rect.centerx += speed
        elif "ButtonExit" in scenes[index]["remove"] and self.rect.centerx >= self.pos_goal_center[0]:
            self.rect.centerx -= speed

        self.pos_current_center = self.rect.center

        rect = self.frames[self.frame_index].get_rect(center=self.rect.center)
        self.text_exit_rect = self.text_exit.get_rect(center=self.rect.center)

        self.screen.blit(self.frames[self.frame_index], rect)
        self.screen.blit(self.text_exit, self.text_exit_rect)
    
    def run_music(self):
        self.clicked_sound.play()
    
    def check_collided(self, pos):
        return self.rect.collidepoint(pos) or self.text_exit_rect.collidepoint(pos)
    
    def load_gif_frames(self):
        """Trả về danh sách Surface từ một gif"""
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
    def __init__(self, screen):
        self.screen = screen
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
    def __init__(self, screen):
        self.screen = screen
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
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.text = "CHỌN CHẾ ĐỘ"
        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.pos_center = (1180, 20)
        self.rect = self.image.get_rect(center=self.pos_center)

    def draw(self):
        pass

class ButtonhumanSelector():
    def __init__(self, screen, humanSelector_old):
        self.screen = screen
        self.humanSelector = humanSelector_old
        
        self.image_changing = False
        if humanSelector_old:
            self.image_changing = True
        
        self.image_ori = pygame.image.load(image_human_selector_paths[int(self.image_changing)]).convert_alpha()
        self.image_size = (120, 120)
        self.image = pygame.transform.scale(self.image_ori, self.image_size)
        self.rect = self.image.get_rect()

        self.pos_init_center = ()
        self.pos_goal_center = ()
        self.pos_curren_center = self.pos_init_center

        if humanSelector_old:
            self.pos_init_center = self.humanSelector.pos_goal_center
            self.pos_goal_center = self.humanSelector.pos_init_center
            self.pos_curren_center = self.humanSelector.pos_current_center
        self.rect.center = self.pos_curren_center

        self.clicked_sound_path = sound_clicked_button_path
        self.clicked_sound = pygame.mixer.Sound(self.clicked_sound_path)

    def change_image(self):
        self.image_changing = not self.image_changing
        self.image_ori = pygame.image.load(image_human_selector_paths[int(self.image_changing)]).convert_alpha()
        self.image = pygame.transform.scale(self.image_ori, self.image_size)
        self.rect = self.image.get_rect()

    def check_collided(self, pos):
        self.rect.collidepoint(pos)

    def run_music(self):
        self.clicked_sound.play()

    def effect_movement(self):
        pass