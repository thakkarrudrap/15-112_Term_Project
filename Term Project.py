import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')

import math, copy, random

from cmu_112_graphics import *

'''
opengameart credits:
    MScull - sniper rifle - https://opengameart.org/content/sniper-and-ak-47
    Georges "TRak" Grondin - game background - https://opengameart.org/content/dark-stone-tile

reddit credits:
    u/S-Flo - sniper person - https://www.reddit.com/r/PixelArt/comments/1mgg5n/occc_cyborg_girl/

pixilart credits:
    StandLight https://www.pixilart.com/art/evil-wizard-577f3a0ba49d8ee

tumblr credits:
    mummy - https://pompomthymine.tumblr.com/post/118489741420/a-mummy-done-for-pixel-dailies-last-month/amp

other credits:
    sniper person alternate - https://www.pngegg.com/en/search?q=cyborg+Art
'''



# class Entity(object):
#     def __init__(self, maxHealth, strength, app):
#         self.health = maxHealth
#         self.maxHealth = maxHealth
#         self.strength = strength
#         self.alive = True

#     def takeDamage(self, amount):
#         self.health -= amount
#         if self.health <= 0:
#             self.alive = False

#     # def dealDamage(self, other):
#         # if isinstance(other, Enemy):
#         #     other.takeDamage(self.strength)

#     def __repr__(self):
#         return f'{type(self).__name__} with current health {self.health}, max health {self.maxHealth}, and strength {self.strength}'


class Player(object):
    def __init__(self, maxHealth, strength, app):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.strength = strength
        self.x = app.width / 2 # refers to the center left (coordinate 15)
        self.y = app.height / 2 # refers to the center top (coordinate 15)
        self.dx = 0
        self.dy = 0
        self.weaponRotation = 0
        self.alive = True

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


    # change weapon rotation here also.
    def keyPressed(self, app, event):
        if event.key == 'Up':
            self.dy = -4
            
            self.dy = -32
            self.move()
            self.dy = 0
        elif event.key == 'Down':
            self.dy = 4

            self.dy = 32
            self.move()
            self.dy = 0
        elif event.key == 'Left':
            self.dx = -4

            self.dx = -32
            self.move()
            self.dx = 0
        elif event.key == 'Right':
            self.dx = 4

            self.dx = 32
            self.move()
            self.dx = 0


    def keyReleased(self, app, event):
    #     if event.key == 'Up' or event.key == 'Down':
    #         self.dy = 0
    #     elif event.key == 'Left' or event.key == 'Right':
    #         self.dx = 0
        pass


    def move(self):
        self.x += self.dx
        self.y += self.dy
        # if self.dx != 0 and self.dy != 0:
        #     self.x += self.dx / math.sqrt(2)
        #     self.y += self.dy / math.sqrt(2)
        # else:
        #     self.x += self.dx
        #     self.y += self.dy

    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
        print(self.health, self.alive)


    def redrawAll(self, app, canvas):
        self.drawPlayer(app, canvas)
        self.drawWeapon(app, canvas)

    def drawWeapon(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.rotatedWeaponImage))

    def drawPlayer(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.playerImage))
        # canvas.create_rectangle(self.x - self.playerImage.size[0] / 2, self.y - self.playerImage.size[1] / 2, self.x + self.playerImage.size[0] / 2, self.y + self.playerImage.size[1] / 2)
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth


class Sniper(Player):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.weaponImage = app.loadImage('spr_sniper.png')
        self.rotatedWeaponImage = self.weaponImage
        self.personImage = app.loadImage('sniper_person_alternate.png')
        # self.personImageFlipped = app.scaleImage(self.personImageFlipped, 64/240)
        self.personImageFlipped = self.personImage.transpose(Image.FLIP_LEFT_RIGHT)
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
        self.x += self.dx
        self.y += self.dy
        if self.invalidMove(app):
            Bullet.bulletList.remove(self)
            del self
            return
        self.checkEnemyHits(app)


    def drawBullet(self, app, canvas):
        tempImage = app.bulletImage.rotate(self.angleDegrees)
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(tempImage))

    def invalidMove(self, app):
        if self.x >= app.width or self.x <= 0 or self.y >= app.height or self.y <= 0:
            return True
        return False

    def checkEnemyHits(self, app):
        for enemy in Enemy.enemyList:
            dx = self.x - max(enemy.x - enemy.image.size[0] / 4, min(self.x, enemy.x + enemy.image.size[0] / 4))
            dy = self.y - max(enemy.y - enemy.image.size[1] / 4, min(self.y, enemy.y + enemy.image.size[1] / 4))
            radius = 2
            if dx**2 + dy**2 <= radius**2:
                Enemy.enemyList
                enemy.takeDamage(self.damage)
                Bullet.bulletList.remove(self)
                del self
                break



class EnemyBullet(object):
    enemyBulletList = []

    def __init__(self, x, y, angleDegrees, damage, app):
        self.x = x
        self.y = y
        self.damage = damage
        self.angleDegrees = angleDegrees
        self.angleRadians = angleDegrees * math.pi / 180
        self.dx = 10 * math.cos(self.angleRadians)
        self.dy = -10 * math.sin(self.angleRadians)
        self.image = app.wizardEnemyFireball

    def move(self, app):
        self.x += self.dx
        self.y += self.dy
        if self.invalidMove(app):
            EnemyBullet.enemyBulletList.remove(self)
            del self
            return
        if self.checkPlayerHit(app):
            app.player.takeDamage(self.damage)
            EnemyBullet.enemyBulletList.remove(self)
            del self
            return


    def drawBullet(self, app, canvas):
        tempImage = self.image.rotate(self.angleDegrees)
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(tempImage))

    def invalidMove(self, app):
        if self.x >= app.width or self.x <= 0 or self.y >= app.height or self.y <= 0:
            return True
        return False

    def checkPlayerHit(self, app):
        dx = self.x - max(app.player.x - app.player.playerImage.size[0] / 10000, min(self.x, app.player.x + app.player.playerImage.size[0] / 10000))
        dy = self.y - max(app.player.y - app.player.playerImage.size[1] / 4, min(self.y, app.player.y + app.player.playerImage.size[1] / 4))
        radius = self.image.size[0] / 2
        return dx**2 + dy**2 <= radius**2

class WizardEnemyFireball(EnemyBullet):
    def __init__(self, x, y, angleDegrees, damage, app):
        super().__init__(x, y, angleDegrees, damage, app)

    # credit to https://yal.cc/rectangle-circle-intersection-test/
    def checkPlayerHit(self, app):
        dx = self.x - max(app.player.x - app.player.playerImage.size[0], min(self.x, app.player.x + app.player.playerImage.size[0]))
        dy = self.y - max(app.player.y - app.player.playerImage.size[1], min(self.y, app.player.y + app.player.playerImage.size[1]))
        radius = self.image.size[0] / 2
        return (dx**2 + dy**2) < (radius**2)


    




class Enemy(object):
    enemyList = []

    def __init__(self, maxHealth, strength, app):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.strength = strength
        self.counter = 0
        self.x = random.randint(0, app.width)
        self.y = random.randint(0, app.height)

    def takeDamage(self, amount):
        self.health -= amount
        print(self.health)
        if self.health <= 0:
            Enemy.enemyList.remove(self)
            del self

    def drawEnemy(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.image))


class MummyEnemy(Enemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.image = app.mummyEnemyImage

    def attack(self, app):
        app.player.takeDamage(self.strength)

    def timerFired(self, app):
        if distance(self.x, self.y, app.player.x, app.player.y) <= 20:
            app.counter = (app.counter + 1) % 5
            if app.counter == 0:
                self.attack(app)
        else:
            app.counter = 0


            
            


    
class WizardEnemy(Enemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.image = app.wizardEnemyImage

    def attack(self, app):
        dx = app.player.x - self.x
        dy = app.player.y - self.y
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
        x = self.x
        y = self.y
        damage = self.strength
        EnemyBullet.enemyBulletList.append(EnemyBullet(x, y, angle, damage, app))
            

    def timerFired(self, app):
        self.counter += 1
        # print(self.counter)
        if self.counter == 25:
            # print('attack')
            self.attack(app)
            self.counter = 0



# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f


    


def appStarted(app):
    app.mode = 'start'
    app.startButtonBounds = (app.width / 2 - 100, .7 * app.height, app.width / 2 + 100, .8 * app.height)
    app.gameBackgroundImage = app.loadImage('gameBackgroundImage.jpg')
    app.gameBackgroundImage = app.scaleImage(app.gameBackgroundImage, 4)
    app.gameWallImage = app.loadImage('gameWallImage.png')
    app.player = Sniper(5, 2, app)
    app.timerDelay = 20
    app.bulletImage = app.loadImage('spr_sniper_bullet.png')
    app.wizardEnemyImage = app.loadImage('wizard_enemy_single_frame.png')
    app.wizardEnemyFireball = app.loadImage('enemy_wizard_fireball.png')
    app.mummyEnemyImage = app.loadImage('mummy_enemy_single.png')
    Enemy.enemyList.append(WizardEnemy(10, 3, app))
    Enemy.enemyList.append(WizardEnemy(10, 3, app))
    Enemy.enemyList.append(MummyEnemy(10, 1, app))
    app.rows = 32
    app.cols = 32
    # populateWallsList(app)
    app.tilesList = [[0 for col in range(app.cols)] for row in range(app.rows)]
    populateTilesList(app)
    print(app.tilesList, Enemy.enemyList[1].y)
    path = astar(app.tilesList, (app.player.x, app.player.y), (Enemy.enemyList[1].x, Enemy.enemyList[1].y))
    print(path)

# Change this later
def populateTilesList(app):
    app.tilesList[5][6] = 1
    app.tilesList[5][7] = 1
    app.tilesList[5][8] = 1
    app.tilesList[5][9] = 1

def getCellBounds(row, col, app):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    x0 = col * cellWidth
    y0 = row * cellHeight
    x1 = x0 + cellWidth
    y1 = y0 + cellHeight
    return x0, y0, x1, y1

def getCell(x, y, app):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    
def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # add start node to open list
    open_list.append(start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          return return_path(current_node)       
        
        # Get the current node and append it to closed list

        current_node = smallestNode(open_list)
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)

    return None

def smallestNode(L):
    smallestF = 10000000000000
    smallestNode = L[0]
    for node in L:
        if node.f < smallestF:
            smallestF = node.f
            smallestNode = node
    return smallestNode

def start_mousePressed(app, event):
    x0, y0, x1, y1 = app.startButtonBounds
    if event.x >= x0 and event.x <= x1 and event.y >= y0 and event.y <= y1:
        app.mode = 'game'
    

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
    for enemyBullet in EnemyBullet.enemyBulletList:
        enemyBullet.move(app)
    

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
    for row in range(len(app.tilesList)):
        for col in range(len(app.tilesList[0])):
            if app.tilesList[row][col] == 1:
                x0, y0, x1, y1 = getCellBounds(row, col, app)
                canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, image = ImageTk.PhotoImage(app.gameWallImage))


runApp(width = 1024, height = 1024)

