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
        self.x = app.width / 2
        self.y = app.height / 2
        row, col = getCell(self.x, self.y, app)
        print(row, col)
        while(app.tilesList[row][col] == 1):
            self.x += 32
            row += 1
        self.dx = 0
        self.dy = 0
        self.weaponRotation = 0
        self.alive = True
        self.moveTimer = 0

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
        if self.moveTimer == 0:
            self.moveTimer = 1
            if event.key == 'Up':
                # self.dy = -4
                
                self.dy = -16
                self.move(app)
                self.dy = 0
            elif event.key == 'Down':
                # self.dy = 4

                self.dy = 16
                self.move(app)
                self.dy = 0
            elif event.key == 'Left':
                # self.dx = -4

                self.dx = -16
                self.move(app)
                self.dx = 0
            elif event.key == 'Right':
                # self.dx = 4

                self.dx = 16
                self.move(app)
                self.dx = 0


    def keyReleased(self, app, event):
        self.moveTimer = 0

    def invalidMove(self, app):
        cellWidth = app.width / app.cols
        cellHeight = app.height / app.rows


        # if self.x % cellWidth != 0:
        #     if self.x > 0:
        #         print('yes')
        #         x = self.x + 16
        # if self.y % cellHeight != 0:
        #     if not self.dy < 0:
        #         print('yes2')
        #         y = self.y + 16
        row, col = getCell(self.x, self.y, app)
        if row >= app.rows or col >= app.cols or row < 0 or col < 0 or app.tilesList[row][col] == 1:
            return True
        x, y = self.x, self.y
        if self.x % cellWidth != 0:
            if self.dx > 0 or self.dy < 0 or self.dy > 0:
                x = self.x + 16
        if self.y % cellHeight != 0:
            if self.dy > 0 or self.dx  < 0 or self.dx > 0:
                y = self.y + 16
        row, col = getCell(x, y, app)
        if app.tilesList[row][col] == 1:
            return True
        # else:
        #     if self.dx > 0:
        #         if app.tilesList[row + 1][col] == 1 or app.tilesList[row + 1][col + 1] == 1 or app.tilesList[row + 1][col - 1] == 1:
        #             print('yes')
        #             return True
        #     if self.dy > 0:
        #         if app.tilesList[row][col + 1] == 1:
        #             print('yes2')
        #             return True
        return False

    def move(self, app):
        self.x += self.dx
        self.y += self.dy
        if self.invalidMove(app):
            self.x -= self.dx
            self.y -= self.dy
        # if self.dx != 0 and self.dy != 0:
        #     self.x += self.dx / math.sqrt(2)
        #     self.y += self.dy / math.sqrt(2)
        # else:
        #     self.x += self.dx
        #     self.y += self.dy

    def takeDamage(self, amount, app):
        self.health -= amount
        if self.health <= 0:
            app.mode = 'gameOver'


    def redrawAll(self, app, canvas):
        self.drawHealth(app, canvas)
        self.drawPlayer(app, canvas)
        self.drawWeapon(app, canvas)

    def drawWeapon(self, app, canvas):
        canvas.create_image(self.x + 16, self.y + 16, image = ImageTk.PhotoImage(self.rotatedWeaponImage))

    def drawPlayer(self, app, canvas):
        canvas.create_image(self.x + 16, self.y + 16, image = self.playerImage)
        # canvas.create_rectangle(self.x - self.playerImage.size[0] / 2, self.y - self.playerImage.size[1] / 2, self.x + self.playerImage.size[0] / 2, self.y + self.playerImage.size[1] / 2)
    
    def drawHealth(self, app, canvas):
        width = app.width * .2
        height = app.height * .02
        canvas.create_rectangle(0, 0, width, height, outline = 'white', width = 5)
        canvas.create_rectangle(0, 0, width * self.health / self.maxHealth, height, fill = 'red', outline = '')

    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth


class Sniper(Player):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.bulletSpeed = 30
        self.weaponImage = app.loadImage('spr_sniper.png')
        self.rotatedWeaponImage = self.weaponImage
        self.personImage = app.loadImage('sniper_person_alternate.png')
        # self.personImageFlipped = app.scaleImage(self.personImageFlipped, 64/240)
        self.personImageFlipped = ImageTk.PhotoImage(self.personImage.transpose(Image.FLIP_LEFT_RIGHT))
        self.personImage = ImageTk.PhotoImage(self.personImage)
        self.playerImage = self.personImage

    def mousePressed(self, app, event):
        Bullet.bulletList.append(Bullet(self.x + 16, self.y + 16, self.weaponRotation, self.strength, app))


class Bullet(object):
    bulletList = []

    def __init__(self, x, y, angleDegrees, damage, app):
        self.x = x
        self.y = y
        self.damage = damage
        self.angleDegrees = angleDegrees
        self.angleRadians = angleDegrees * math.pi / 180
        self.dx = app.player.bulletSpeed * math.cos(self.angleRadians)
        self.dy = -app.player.bulletSpeed * math.sin(self.angleRadians)

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
        row, col = getCell(self.x, self.y, app)
        if app.tilesList[row][col] == 1:
            return True
        return False

    def checkEnemyHits(self, app):
        for enemy in Enemy.enemyList:
            dx = self.x - max(enemy.x - enemy.image.size[0] / 2, min(self.x, enemy.x + enemy.image.size[0] / 2))
            dy = self.y - max(enemy.y - enemy.image.size[1] / 2, min(self.y, enemy.y + enemy.image.size[1] / 2))
            radius = 2
            if dx**2 + dy**2 <= radius**2:
                Enemy.enemyList
                enemy.takeDamage(self.damage, app)
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
        self.radius = 2

    def move(self, app):
        self.x += self.dx
        self.y += self.dy
        if self.invalidMove(app):
            EnemyBullet.enemyBulletList.remove(self)
            del self
            return
        if self.checkPlayerHit(app):
            app.player.takeDamage(self.damage, app)
            EnemyBullet.enemyBulletList.remove(self)
            del self
            return


    def drawBullet(self, app, canvas):
        canvas.create_image(self.x, self.y, image = self.image)

    def invalidMove(self, app):
        if self.x >= app.width or self.x <= 0 or self.y >= app.height or self.y <= 0:
            return True
        row, col = getCell(self.x, self.y, app)
        if app.tilesList[row][col] == 1:
            return True
        return False

    # credit to https://yal.cc/rectangle-circle-intersection-test/
    def checkPlayerHit(self, app):
        # dx = self.x - max(app.player.x - app.player.playerImage.size[0] / 10000, min(self.x, app.player.x + app.player.playerImage.size[0] / 10000))
        # dy = self.y - max(app.player.y - app.player.playerImage.size[1] / 4, min(self.y, app.player.y + app.player.playerImage.size[1] / 4))
        dx = self.x - max(app.player.x - 32 / 10000, min(self.x, app.player.x + 32 / 100000))
        dy = self.y - max(app.player.y - 32 / 4, min(self.y, app.player.y + 32 / 4))
        radius = 16
        return dx**2 + dy**2 <= radius**2

class WizardEnemyFireball(EnemyBullet):
    def __init__(self, x, y, angleDegrees, damage, app):
        super().__init__(x, y, angleDegrees, damage, app)
        self.radius = 16

    # def checkPlayerHit(self, app):
    #     dx = self.x - max(app.player.x - app.player.playerImage.size[0], min(self.x, app.player.x + app.player.playerImage.size[0]))
    #     dy = self.y - max(app.player.y - app.player.playerImage.size[1], min(self.y, app.player.y + app.player.playerImage.size[1]))
    #     radius = 16
    #     return (dx**2 + dy**2) < (radius**2)


    




class Enemy(object):
    enemyList = []

    def __init__(self, maxHealth, strength, app):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.strength = strength
        self.counter = 1
        self.x = random.randint(0, app.width - 1)
        self.y = random.randint(0, app.height - 1)
        row, col = getCell(self.x, self.y, app)
        while row >= app.rows or row < 0 or col >= app.cols or col < 0:
                self.x = random.randint(0, app.width)
                self.y = random.randint(0, app.height)
                row, col = getCell(self.x, self.y, app)
        while(app.tilesList[row][col]) == 1:
            self.x = random.randint(0, app.width)
            self.y = random.randint(0, app.height)
            row, col = getCell(self.x, self.y, app)
        self.moveCounter = 0
        self.movePath = astar(app.tilesList, getCell(self.x, self.y, app), getCell(app.player.x, app.player.y, app))

    def takeDamage(self, amount, app):
        self.health -= amount
        if self.health <= 0:
            Enemy.enemyList.remove(self)
            del self
        if len(Enemy.enemyList) == 0:
            app.mode = 'newLevel'

    def drawEnemy(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.image))





class MeleeEnemy(Enemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
    
    def attack(self, app):
        app.player.takeDamage(self.strength, app)

    def timerFired(self, app):
        self.moveCounter = (self.moveCounter + 1) % self.pathUpdateTicks
        if self.moveCounter == 0:
            self.movePath = astar(app.tilesList, getCell(self.x, self.y, app), getCell(app.player.x, app.player.y, app))
        if self.moveCounter % self.moveTicks == 0:
            self.move(app)

    def move(self, app):
        if len(self.movePath) >= 2:
            dx = (self.movePath[1][0] - self.movePath[0][0]) * self.speed
            dy = (self.movePath[1][1] - self.movePath[0][1]) * self.speed
            self.x += dx
            self.y += dy
            if getCell(self.x, self.y, app) == self.movePath[1]:
                self.movePath.pop(0)
        else:
            if self.inRange(app):
                self.counter = (self.counter + 1) % self.attackTicks
                if self.counter == 0:
                    self.attack(app)
            else:
                self.counter = 0

    def inRange(self, app):
        dx = getCell(app.player.x, app.player.y, app)[0] - getCell(self.x, self.y, app)[0]
        dy = getCell(app.player.x, app.player.y, app)[1] - getCell(self.x, self.y, app)[1]
        if dx**2 + dy**2 <= 2:
            return True
        return False

class MummyEnemy(MeleeEnemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.image = app.mummyEnemyImage
        self.pathUpdateTicks = 30
        self.moveTicks = 1
        self.attackTicks = 5
        self.speed = 6
            
class RangedEnemy(Enemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)

    def timerFired(self, app):
        self.moveCounter = (self.moveCounter + 1) % self.pathUpdateTicks
        if self.moveCounter == 0:
            self.movePath = astar(app.tilesList, getCell(self.x, self.y, app), self.getTarget(app))
        if self.moveCounter % self.moveTicks == 0:
            self.move(app)
        
        self.counter = (self.counter + 1) % self.attackTicks
        if self.counter == 0:
            self.attack(app)
        


    def move(self, app):
        if len(self.movePath) >= 2:
            dx = (self.movePath[1][0] - self.movePath[0][0]) * self.speed
            dy = (self.movePath[1][1] - self.movePath[0][1]) * self.speed
            self.x += dx
            self.y += dy
            if getCell(self.x, self.y, app) == self.movePath[1]:
                self.movePath.pop(0)

    def getTarget(self, app):
        cellWidth = app.width / app.cols
        cellHeight = app.height / app.rows
        l = [i for i in range(self.minRange, self.maxRange + 1)]
        l.extend([-i for i in range(self.minRange, self.maxRange + 1)])
        dx = random.choice(l)
        dy = random.choice(l)
        newX = app.player.x + dx*cellWidth
        newY = app.player.y + dy*cellHeight
        if newX >= app.width:
            newX = app.width
        elif newX <= 0:
            newX = 0
        if newY >= app.height:
            newY = app.height
        elif newY <= 0:
            newY = 0
        for row in range(getCell(app.player.x, app.player.y, app)[1], getCell(newX, newY, app)[1]):
            for col in range(getCell(app.player.x, app.player.y, app)[0], getCell(newX, newY, app)[0]):
                if app.tilesList[row][col] == 1:
                    newX, newY = app.player.x, app.player.y
        return getCell(newX, newY, app)


    
class WizardEnemy(RangedEnemy):
    def __init__(self, maxHealth, strength, app):
        super().__init__(maxHealth, strength, app)
        self.image = app.wizardEnemyImage
        self.minRange = 5
        self.maxRange = 8
        self.pathUpdateTicks = 70
        self.moveTicks = 1
        self.attackTicks = 20
        self.speed = 4

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
        EnemyBullet.enemyBulletList.append(EnemyBullet(self.x, self.y, angle, self.strength, app))
            



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
    app.rows = 32
    app.cols = 32
    app.mode = 'start'
    app.startButtonBounds = (app.width / 2 - 100, .7 * app.height, app.width / 2 + 100, .8 * app.height)
    app.gameBackgroundImage = app.loadImage('gameBackgroundImage.jpg')
    app.gameBackgroundImage = app.scaleImage(app.gameBackgroundImage, 4)
    app.gameWallImage = ImageTk.PhotoImage(app.loadImage('gameWallImage.png'))
    app.timerDelay = 20
    app.bulletImage = app.loadImage('spr_sniper_bullet.png')
    app.wizardEnemyImage = app.loadImage('wizard_enemy_single_frame.png')
    app.wizardEnemyFireball = ImageTk.PhotoImage(app.loadImage('enemy_wizard_fireball.png'))
    app.mummyEnemyImage = app.loadImage('mummy_enemy_single.png')
    Enemy.enemyList = []
    Bullet.bulletList = []
    EnemyBullet.enemyBulletList = []
    app.tilesList = [[1 for col in range(app.cols)] for row in range(app.rows)]
    app.roomList = []
    populateRoomList(app)
    generateNodeList(app)
    app.player = Sniper(15, 3, app)
    # populateTilesList(app)
    app.meleeTypes = ['mummy']
    app.rangedTypes = ['wizard']
    app.level = 1
    newLevel(app)


class Room(object):
    def __init__(self, app):
        self.x0 = random.randint(0, app.cols - 4)
        self.y0 = random.randint(0, app.rows - 4)
        self.x1 = self.x0 + random.randint(3, 5)
        self.y1 = self.y0 + random.randint(3, 5)
        cellWidth = app.width / app.cols
        cellHeight = app.height / app.rows
        self.cx = cellWidth * (self.x0 + self.x1) / 2
        self.cy = cellHeight * (self.y0 + self.y1) / 2
        self.tiles = []
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                if x < app.cols and x > 0 and y < app.rows and y > 0:
                    self.tiles.append((x, y))


def populateRoomList(app):
    for i in range(150):
        room = Room(app)
        if inAvailableLocation(room, app):
            for (row, col) in room.tiles:
                if col < app.cols - 1 and col >= 1 and row < app.rows - 1  and row > 1:
                    app.tilesList[row][col] = 0
            app.roomList.append(room)

def generateNodeList(app):
    nodeList = [[0 for col in range(len(app.roomList))] for row in range(len(app.roomList))]
    for room1 in range(len(app.roomList)):
        for room2 in range(len(app.roomList)):
            nodeList[room1][room2] = distance(app.roomList[room1].cx, app.roomList[room1].cy, app.roomList[room2].cx, app.roomList[room2].cy)
    generateTerrain(app, nodeList)
    # for room1 in app.roomList:
    #     for room2 in app.roomList:
    #         connectRooms(room1, room2, app)


# credit to https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
def inAvailableLocation(room, app):
    for otherRoom in app.roomList:
        if not(room.x0 > otherRoom.x1 or room.x1 < otherRoom.x0 or room.y0 > otherRoom.y1 or room.y1 < otherRoom.y0):
            return False
    return True

def generateTerrain(app, nodeList):
    # Prim's Algorithm in Python


    INF = 9999999
    # number of vertices in graph
    V = len(app.roomList)
    # create a 2d array of size 5x5
    # for adjacency matrix to represent graph
    G = nodeList
    # create a array to track selected vertex
    # selected will become true otherwise false
    
    selected = [0 for i in range(V)]

    '''
    selected = [0, 0, 0, 0, 0]
    '''
    # set number of edge to 0
    no_edge = 0
    # the number of egde in minimum spanning tree will be
    # always less than(V - 1), where V is number of vertices in
    # graph
    # choose 0th vertex and make it true
    selected[0] = True
    # print for edge and weight
    
    
    '''
    print("Edge : Weight\n")
    '''

    while (no_edge < V - 1):
        # For every vertex in the set S, find the all adjacent vertices
        #, calculate the distance from the vertex selected at step 1.
        # if the vertex is already in the set S, discard it otherwise
        # choose another vertex nearest to selected vertex  at step 1.
        minimum = INF
        x = 0
        y = 0
        for i in range(V):
            if selected[i]:
                for j in range(V):
                    if ((not selected[j]) and G[i][j]):  
                        # not in selected and there is an edge
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            x = i
                            y = j
                            
        
        print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
        connectRooms(app.roomList[x], app.roomList[y], app)
        
        selected[y] = True
        no_edge += 1


def connectRooms(room1, room2, app):

    cellWidth = int(app.width / app.cols)
    cellHeight = int(app.height / app.rows)
    cRow1 = int(room1.cy / cellWidth)
    cCol1 = int(room1.cx / cellHeight)
    cRow2 = int(room2.cy / cellWidth)
    cCol2 = int(room2.cx / cellWidth)
    print(cRow1, cCol1, cRow2, cCol2)
    # dx = cCol2 - cCol1
    # dy = cRow2 - cRow1
    # for i in range(dx):
    #     app.tilesList[i + cCol1][cRow1] = 0
    # for i in range(dy):
    #     app.tilesList[cCol2][i + cRow1] = 0
    dx = cCol2 - cCol1
    dy = cRow2 - cRow1
    if dx >= 0:
        for i in range(dx):
            app.tilesList[i + cCol1][cRow1] = 0
            app.tilesList[i + cCol1][cRow1 + 1] = 0
            app.tilesList[i + cCol1][cRow1 - 1] = 0
    else:
        for i in range(dx, 0):
            app.tilesList[i + cCol1][cRow1] = 0
            app.tilesList[i + cCol1][cRow1 + 1] = 0
            app.tilesList[i + cCol1][cRow1 - 1] = 0
    if dy >= 0:
        for i in range(dy):
            app.tilesList[cCol2][i + cRow1] = 0
            app.tilesList[cCol2 + 1][i + cRow1] = 0
            app.tilesList[cCol2 - 1][i + cRow1] = 0
    else:
        for i in range(dy, 0):
            app.tilesList[cCol2][i + cRow1] = 0
            app.tilesList[cCol2 + 1][i + cRow1] = 0
            app.tilesList[cCol2 - 1][i + cRow1] = 0
    # cRow1 = (room1.y0 + room1.y1) // 2
    # cCol1 = (room1.x0 + room1.x1) // 2
    # cRow2 = (room2.y0 + room2.y1) // 2
    # cCol2 = (room2.x0 + room2.x1) // 2


    # # dx = cCol2 - cCol1
    # # dy = cRow2 - cRow1
    # # for i in range(dx):
    # #     app.tilesList[i + cCol1][cRow1] = 0
    # # for i in range(dy):
    # #     app.tilesList[cCol2][i + cRow1] = 0
    

    # # if dx >= 0:
    # #     for i in range(dx):
    # #         app.tilesList[i + cCol1][cRow1] = 0
    # # else: 
    # #     for i in range(dx, 0):
    # #         app.tilesList[i + cCol1][cRow1] = 0
    # # if dy >= 0:
    # #     for i in range(dy):
    # #         app.tilesList[cCol2][i + cRow1] = 0
    # # else:
    # #     for i in range(dy, 0):
    # #         app.tilesList[cCol2][i + cRow1] = 0

    
    
    # dx = cCol2 - cCol1
    # dy = cRow2 - cRow1
    # if dx >= 0 and dy >= 0:
    #     for i in range(-2, dx + 2):
    #         if i + cCol1 < app.cols and i + cCol1 >= 0:
    #             app.tilesList[i + cCol1][cRow1] = 0
    #         if cRow1 - 1 < app.rows and cRow1 - 1 >= 0:
    #             app.tilesList[i + cCol1][cRow1 - 1] = 0
    #         if cRow1 + 1 < app.rows and cRow1 + 1 >= 0:
    #             app.tilesList[i + cCol1][cRow1 + 1] = 0
    #     for j in range(-2, dy + 2):
    #         if j + cRow1 < app.rows and i + cRow1 >= 0:
    #             app.tilesList[cCol2][j + cRow1] = 0
    #         if cCol2 - 1 < app.rows and cCol2 - 1 >= 0:
    #             app.tilesList[cCol2 - 1][j + cRow1] = 0
    #         if cCol2 + 1 < app.rows and cCol2 + 1 >= 0:
    #             app.tilesList[cCol2 + 1][j + cRow1] = 0
    # elif dx >= 0 and dy <= 0:
    #     for i in range(-2, dx + 2):
    #         if i + cCol1 < app.cols and i + cCol1 >= 0:
    #             app.tilesList[i + cCol1][cRow2] = 0
    #         if cRow2 - 1 < app.rows and cRow2 - 1 >= 0:
    #             app.tilesList[i + cCol1][cRow2 - 1] = 0
    #         if cRow2 + 1 < app.rows and cRow2 + 1 >= 0:
    #             app.tilesList[i + cCol1][cRow2 + 1] = 0
    #     for j in range(-2, dy + 2):
    #         if j + cRow2 < app.rows and j + cRow2 >= 0:
    #             app.tilesList[cCol2][j + cRow2] = 0
    #         if cCol2 - 1 < app.rows and cCol2 - 1 >= 0:
    #             app.tilesList[cCol2 - 1][j + cRow1] = 0
    #         if cCol2 + 1 < app.rows and cCol2 + 1 >= 0:
    #             app.tilesList[cCol2 + 1][j + cRow1] = 0
    # elif dx <= 0 and dy >= 0:
    #     for i in range(-2, dx + 2):
    #         if i + cCol2 < app.cols and i + cCol2 >= 0:
    #             app.tilesList[i + cCol2][cRow1] = 0
    #         if cRow1 - 1 < app.rows and cRow1 - 1 >= 0:
    #             app.tilesList[i + cCol1][cRow1 - 1] = 0
    #         if cRow1 + 1 < app.rows and cRow1 + 1 >= 0:
    #             app.tilesList[i + cCol1][cRow1 + 1] = 0
    #     for j in range(-2, dy + 2):
    #         if j + cRow1 < app.rows and j + cRow1 >= 0:
    #             app.tilesList[cCol1][j + cRow1] = 0
    #         if cCol1 - 1 < app.cols and cCol1 - 1 >= 0:
    #             app.tilesList[cCol1 - 1][j + cRow1] = 0
    #         if cCol1 + 1 < app.cols and cCol1 + 1 >= 0:
    #             app.tilesList[cCol1 + 1][j + cRow1] = 0
    # elif dx <= 0 and dy <= 0:
    #     for i in range(-2, dx + 2):
    #         if i + cCol2 < app.cols and i + cCol2 >= 0:
    #             app.tilesList[i + cCol2][cRow2] = 0
    #         if cRow2 - 1 < app.rows and cRow2 - 1 >= 0:
    #             app.tilesList[i + cCol1][cRow2 - 1] = 0
    #         if cRow2 + 1 < app.rows and cRow2 + 1 >= 0:
    #             app.tilesList[i + cCol1][cRow2 + 1] = 0
    #     for j in range(-2, dy + 2):
    #         if j + cRow2 < app.rows and j + cRow2 >= 0:
    #             app.tilesList[cCol1][j + cRow2] = 0
    #         if cCol1 - 1 < app.cols and cCol1 - 1 >= 0:
    #             app.tilesList[cCol1 - 1][j + cRow1] = 0
    #         if cCol1 + 1 < app.cols and cCol1 + 1 >= 0:
    #             app.tilesList[cCol1 + 1][j + cRow1] = 0

# Change this later
def populateTilesList(app):
    app.tilesList[5][5] = 1
    app.tilesList[5][6] = 1
    app.tilesList[5][7] = 1
    app.tilesList[5][8] = 1
    app.tilesList[5][9] = 1
    app.tilesList[6][5] = 1
    app.tilesList[6][6] = 1
    app.tilesList[6][7] = 1

def newLevel(app):
    for bullet in Bullet.bulletList:
        del bullet
    Bullet.bulletList = []
    for enemy in Enemy.enemyList:
        del enemy
    Enemy.enemyList = []
    for enemyBullet in EnemyBullet.enemyBulletList:
        del enemyBullet
    Enemy.enemyBulletList = []
    # generateNodeList(app)
    meleeHealth = 5 + app.level
    meleeStrength = 1 + int(app.level/2)
    rangedHealth = 10 + app.level
    rangedStrength = 1 + int(app.level/3)
    numMelee = 2 + int(app.level/3)
    numRanged = 2 + int(app.level/3)
    for i in range(numMelee):
        enemyType = random.choice(app.meleeTypes)
        if enemyType == 'mummy':
            Enemy.enemyList.append(MummyEnemy(meleeHealth, meleeStrength, app))
    for i in range(numRanged):
        enemyType = random.choice(app.rangedTypes)
        if enemyType == 'wizard':
            Enemy.enemyList.append(WizardEnemy(rangedHealth, rangedStrength, app))


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
    row = int(x / cellHeight)
    col = int(y / cellWidth)
    return row, col
    
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
    app.player.move(app)
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
                canvas.create_image((y0 + y1) / 2, (x0 + x1) / 2, image = app.gameWallImage)
                # canvas.create_rectangle(y0, x0, y1, x1, fill = 'grey')

def newLevel_mousePressed(app, event):
    if .4 * app.width <= event.x <= .6 * app.width and .7 * app.height <= event.y <= .8 * app.height:
        app.mode = 'game'
        app.level += 1
        newLevel(app)

def newLevel_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = '#9e9072', outline = '')
    canvas.create_text(app.width / 2, app.height / 2, text = f'Level {app.level} Completed!', font = 'Arial 25')
    canvas.create_rectangle(.4 * app.width, .7 * app.height, .6 * app.width, .8 * app.height, fill = 'red')
    canvas.create_text(app.width / 2, .75 * app.height, text = 'Next Level', font = 'Arial 14')

def gameOver_mousePressed(app, event):
    if .4 * app.width <= event.x <= .6 * app.width and .7 * app.height <= event.y <= .8 * app.height:
        appStarted(app)

def gameOver_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black', outline = '')
    canvas.create_text(app.width / 2, app.height / 2, text = 'Game Over', fill = 'red', font = 'Arial 25')
    canvas.create_rectangle(.4 * app.width, .7 * app.height, .6 * app.width, .8 * app.height, fill = 'red')
    canvas.create_text(app.width / 2, .75 * app.height, text = 'Click here to continue', font = 'Arial 14')


runApp(width = 1024, height = 1024)