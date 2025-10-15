import sys
from scripts import installLibrary
from scripts import game

def main():
    necessary_libs = {
        "cv2" : "opencv_python", 
        "pygame" : "pygame", 
        "pygame_gui": "pygame_gui", 
        "PIL" : "Pillow",
        "openpyxl" : "openpyxl"
    }
    if installLibrary.check_and_install_libs(necessary_libs):
        Sokoban = game.start()
    else:
        sys.exit()
    
if __name__ == "__main__":
    main()