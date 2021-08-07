import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')

import math, copy, random

from cmu_112_graphics import *

'''
opengameart credits:
    MScull
    Georges "TRak" Grondin

'''



class Entity(object):
    def __init__(self, maxHealth, strength):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.strength = strength
        self.alive = True

    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    # def dealDamage(self, other):
        # if isinstance(other, Enemy):
        #     other.takeDamage(self.strength)

    def __repr__(self):
        return f'{type(self).__name__} with current health {self.health}, max health {self.maxHealth}, and strength {self.strength}'


class Player(Entity):
    def __init__(self, maxHealth, strength):
        super().__init__(maxHealth, strength)
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth


class Sniper(Player):
    def __init__(self, maxHealth, strength):
        super().__init__(maxHealth, strength)
        self.x = app.width / 2
        self.y = app.height / 2

    def mouseMoved(self, app, event):
        pass

    def mousePressed(self, app, event):
        pass




class Enemy(Entity):
    def __init__(self, maxHealth, strength, x, y): # x and y refer to the top left corner.
        super().__init__(maxHealth, strength)




    


def appStarted(app):
    app.mode = 'start'
    app.startButtonBounds = (app.width / 2 - 100, .7 * app.height, app.width / 2 + 100, .8 * app.height)
    app.gameBackgroundImage = app.loadImage('gameBackgroundImage.jpg')
    app.gameBackgroundImage = app.scaleImage(app.gameBackgroundImage, 4)
    app.gameWallImage = app.loadImage('gameWallImage.png')
    app.wallsList = []
    populateWallsList(app)


def start_mousePressed(app, event):
    x0, y0, x1, y1 = app.startButtonBounds
    if event.x >= x0 and event.x <= x1 and event.y >= y0 and event.y <= y1:
        app.mode = 'game'

# Change this later
def populateWallsList(app):
    app.wallsList.append((512, 620))
    app.wallsList.append((512, 652))
    app.wallsList.append((512, 684))
    app.wallsList.append((544, 620))
    app.wallsList.append((544, 652))

def start_redrawAll(app, canvas):
    start_drawTitle(app, canvas)

def start_drawTitle(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = '#9e9072')
    canvas.create_text(app.width / 2, app.height / 2, text = 'Game Title', fill = 'black', font = 'Times 20')
    x0, y0, x1, y1 = app.startButtonBounds
    canvas.create_rectangle(x0, y0, x1, y1, fill = '#db817f')
    canvas.create_text(app.width / 2, .75 * app.height, text = 'Start', fill = 'black', font = 'Times 14')

def game_mousePressed(app, event):
    pass

def game_redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2,  image = ImageTk.PhotoImage(app.gameBackgroundImage))
    game_drawWall(app, canvas)

def game_drawWall(app, canvas):
    for (x, y) in app.wallsList:
        canvas.create_image(x, y, image = ImageTk.PhotoImage(app.gameWallImage))


runApp(width = 1024, height = 1024)

