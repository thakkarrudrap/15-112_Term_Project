from cmu_112_graphics import *
import random, string, math, time, copy

def appStarted(app):
    app.rows = 32
    app.cols = 32
    app.roomTileList = []
    # app.roomList = []
    # populateRoomList(app)
    for row in range(app.rows):
        for col in range(app.cols):
            app.roomTileList.append((col, row))
    for i in range(100):
        x = random.randint(0, app.cols - 1)
        y = random.randint(0, app.rows - 1)
        try:
            app.roomTileList.remove((x, y))
        except:
            continue
        print(app.roomTileList)

# class Room(object):
#     def __init__(self, app):
#         self.x0 = random.randint(0, app.cols - 4)
#         self.y0 = random.randint(0, app.rows - 4)
#         self.x1 = self.x0 + random.randint(3, 5)
#         self.y1 = self.y0 + random.randint(3, 5)
#         self.tiles = []
#         for x in range(self.x0, self.x1 + 1):
#             for y in range(self.y0, self.y1 + 1):
#                 self.tiles.append((x, y))


# def populateRoomList(app):
#     for i in range(100):
#         room = Room(app)
#         if inAvailableLocation(room, app):
#             for (x, y) in room.tiles:
#                 app.roomTileList.append((x, y))
#             app.roomList.append(room)
#     print(app.roomTileList)


# credit to https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
# def inAvailableLocation(room, app):
#     for otherRoom in app.roomList:
#         if not(room.x0 > otherRoom.x1 or room.x1 < otherRoom.x0 or room.y0 > otherRoom.y1 or room.y1 < otherRoom.y0):
#             return False
#     return True



# def invalid(x, y, app):
#     if x < 2 or x > app.cols - 3 or y < 2 or y > app.rows:
#         return True
#     return False


    

def getCellBounds(row, col, app):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    x0 = col * cellWidth
    y0 = row * cellHeight
    x1 = x0 + cellWidth
    y1 = y0 + cellHeight
    return x0, y0, x1, y1

def mousePressed(app, event):
    pass

def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(row, col, app)
            canvas.create_rectangle(x0, y0, x1, y1,)
    for (x, y) in app.roomTileList:
        x0, y0, x1, y1 = getCellBounds(x, y, app)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')

    

def main():
    runApp(width=1024, height=1024)

if __name__ == '__main__':
    main()