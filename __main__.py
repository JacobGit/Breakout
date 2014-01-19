# __main__.py
# Walker M. White (wmw2)
# November 12, 2012
"""__main__ module for Breakout

This is the module with the script code to start up the App.  Make
sure that this module is in a folder with the following files:

    controller.py  (the primary controller class)
    model.py       (the model classes)
    game2d.py      (the view classes)

In addition, you should have the following subfolders

    Fonts          (fonts to use for GLabel)
    Sounds         (sound effects for the game)
    Images         (image files to use in the game)

Moving any of these folders or files will prevent the game from 
working properly. You are free to add new files into these 
folders as you wish."""
from constants import *
from controller import *

# Application code
if __name__ == '__main__':
    Breakout(width=GAME_WIDTH,height=GAME_HEIGHT).run()
