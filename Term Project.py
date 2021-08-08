import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')

import math, copy, random

from cmu_112_graphics import *

'''
opengameart credits:
    MScull
    Georges "TRak" Grondin

reddit credits:
    u/S-Flo

pixilart credits:
    StandLight https://www.pixilart.com/art/evil-wizard-577f3a0ba49d8ee

other credits:
    https://pompomthymine.tumblr.com/post/118489741420/a-mummy-done-for-pixel-dailies-last-month/amp
'''



class Entity(object):
    def __init__(self, maxHealth, strength, app):
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
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.x = app.width / 2 # refers to the center left (coordinate 15)
        self.y = app.height / 2 # refers to the center top (coordinate 15)
        self.dx = 0
        self.dy = 0
        self.weaponRotation = 0

    def mouseMoved(self, app, event):
        dx = event.x - self.x
        dy = event.y - self.y
        try:
            angle = math.atan(dy / dx)
        except:
            angle = math.pi / 2
        self.weaponRotation = abs(angle) * 180 / math.pi
        if dx < 0 and dy < 0:
            self.weaponRotation = 180 - self.weaponRotation
        elif dx <= 0 and dy > 0:
            self.weaponRotation += 180
        elif dx >= 0 and dy > 0:
            self.weaponRotation = 360 - self.weaponRotation
        if dx > 0:
            self.playerImage = self.personImage
        else:
            self.playerImage = self.personImageFlipped
        self.rotatedWeaponImage = self.weaponImage.rotate(self.weaponRotation)

    def keyPressed(self, app, event):
        if event.key == 'Up':
            self.dy = -4
        elif event.key == 'Down':
            self.dy = 4
        elif event.key == 'Left':
            self.dx = -4
        elif event.key == 'Right':
            self.dx = 4

    def keyReleased(self, app, event):
        if event.key == 'Up' or event.key == 'Down':
            self.dy = 0
        elif event.key == 'Left' or event.key == 'Right':
            self.dx = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # if self.dx != 0 and self.dy != 0:
        #     self.x += self.dx / math.sqrt(2)
        #     self.y += self.dy / math.sqrt(2)
        # else:
        #     self.x += self.dx
        #     self.y += self.dy


    def redrawAll(self, app, canvas):
        self.drawPlayer(app, canvas)
        self.drawWeapon(app, canvas)

    def drawWeapon(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.rotatedWeaponImage))

    def drawPlayer(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.playerImage))
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth


class Sniper(Player):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.weaponImage = app.loadImage('spr_sniper.png')
        self.rotatedWeaponImage = self.weaponImage
        self.personImageFlipped = app.loadImage('Sniper_person.png')
        self.personImageFlipped = app.scaleImage(self.personImageFlipped, 64/240)
        self.personImage = self.personImageFlipped.transpose(Image.FLIP_LEFT_RIGHT)
        self.playerImage = self.personImage

    def mousePressed(self, app, event):
        Bullet.bulletList.append(Bullet(self.x, self.y, self.weaponRotation, self.strength, app))


class Bullet(object):
    bulletList = []

    def __init__(self, x, y, angleDegrees, damage, app):
        self.x = x
        self.y = y
        self.damage = damage
        self.angleDegrees = angleDegrees
        self.angleRadians = angleDegrees * math.pi / 180
        self.dx = 10 * math.cos(self.angleRadians)
        self.dy = -10 * math.sin(self.angleRadians)

    def move(self, app):
        if self.invalidMove(app):
            Bullet.bulletList.remove(self)
            del self
            return
        self.x += self.dx
        self.y += self.dy


    def drawBullet(self, app, canvas):
        tempImage = app.bulletImage.rotate(self.angleDegrees)
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(tempImage))

    def invalidMove(self, app):
        if self.x >= app.width or self.x <= 0 or self.y >= app.height or self.y <= 0:
            return True
        return False

class EnemyBullet(Bullet):
    enemyBulletList = []

    def __init__(self, x, y, angleDegrees, damage, app):
        super().__init__(x, y, angleDegrees, damage, app)

    def move(self, app):
        if self.invalidMove(app):
            EnemyBullet.enemyBulletList.remove(self)
            del self
            return
        self.x += self.dx
        self.y += self.dy

    def drawBullet(self, app, canvas):
        tempImage = self.image.rotate(self.angleDegrees)
        canvas.create_image(self.x, self.y, image = imageTk.PhotoImage(tempImage))

class WizardEnemyFireball(EnemyBullet):
    def __init__(self, x, y, angleDegrees, damage, app):
        super().__init__(x, y, angleDegrees, damage, app)
        self.image = app.loadImage('enemy_wizard_fireball.png')


    




class Enemy(object):
    enemyList = []

    def __init__(self, maxHealth, strength, image, app):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.strength = strength
        self.counter = 0
        self.x = random.randint(0, app.width)
        self.y = random.randint(0, app.height)
        self.image = image

    def drawEnemy(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.image))


# class Mummy(Enemy):
#     def __init__(self, maxHealth, strength):
#         super().__init__(maxHealth, strength)

    
class WizardEnemy(Enemy):
    def __init__(self, maxHealth, strength, image, app):
        super().__init__(maxHealth, strength, image, app)

    def attack(self, app):
        dx = 0 - self.x
        dy = 0 - self.y
        try:
            angle = math.atan(dy / dx)
        except:
            angle = math.pi / 2
        angle = abs(angle) * 180 / math.pi
        if dx < 0 and dy < 0:
            angle = 180 - angle
        elif dx <= 0 and dy > 0:
            angle += 180
        elif dx >= 0 and dy > 0:
            angle = 360 - angle
            

    def timerFired(self, app):
        self.counter += 1
        print(self.counter)
        if self.counter == 10:
            print('attack')
            self.attack(self)
            self.counter = 0




    


def appStarted(app):
    app.mode = 'start'
    app.startButtonBounds = (app.width / 2 - 100, .7 * app.height, app.width / 2 + 100, .8 * app.height)
    app.gameBackgroundImage = app.loadImage('gameBackgroundImage.jpg')
    app.gameBackgroundImage = app.scaleImage(app.gameBackgroundImage, 4)
    app.gameWallImage = app.loadImage('gameWallImage.png')
    app.wallsList = []
    populateWallsList(app)
    app.player = Sniper(5, 2, app)
    app.timerDelay = 20
    app.bulletImage = app.loadImage('spr_sniper_bullet.png')
    app.wizardEnemyImage = app.loadImage('wizard_enemy_single_frame.png')
    app.wizardEnemyFireball = app.loadImage('enemy_wizard_fireball.png')
    Enemy.enemyList.append(WizardEnemy(10, 3, app.wizardEnemyImage, app))
    Enemy.enemyList.append(WizardEnemy(10, 3, app.wizardEnemyImage, app))


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

def game_mouseMoved(app, event):
    app.player.mouseMoved(app, event)

def game_mousePressed(app, event):
    app.player.mousePressed(app, event)

def game_keyPressed(app, event):
    app.player.keyPressed(app, event)

def game_keyReleased(app, event):
    app.player.keyReleased(app, event)

def game_timerFired(app):
    app.player.move()
    for bullet in Bullet.bulletList:
        bullet.move(app)
    for enemy in Enemy.enemyList:
        enemy.timerFired(app)

def game_redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2,  image = ImageTk.PhotoImage(app.gameBackgroundImage))
    game_drawWall(app, canvas)
    app.player.redrawAll(app, canvas)
    for bullet in Bullet.bulletList:
        bullet.drawBullet(app, canvas)
    for enemy in Enemy.enemyList:
        enemy.drawEnemy(app, canvas)
    for enemyBullet in EnemyBullet.enemyBulletList:
        enemyBullet.drawBullet(app, canvas)

def game_drawWall(app, canvas):
    for (x, y) in app.wallsList:
        canvas.create_image(x, y, image = ImageTk.PhotoImage(app.gameWallImage))


runApp(width = 1024, height = 1024)

