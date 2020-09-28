#! /usr/bin/env python
# This program is intended to use Python 2 and modules installed under Python 2


import math
import random
import signal
import sys
import time

import turtle

DEBUG = True


# TODO; This signal handler does allow CTRL-C to exit the game when it is
# pressed in the turtle/tkinter window (when it is is focus) whis is part of
# the improvements to 'quitting' we were looking for. BUT there is still an
# ugly tkinter error thrown to the console when quitting this way. A somewhat
# separate problem is that the same or a similar ugly tkinter error is thrown
# to the console when the MacOS red window close button is clicked. The problem
# comse from tkinter attempting to dispose of objects that no longer exist.
# It seems the final solution will be to work directly with tkinter in some
# way. We need to be able to simply close the window and have the game quit
# cleanly, as well as hit CTRL-C. NOTE: When the game is running and the game
# window is in focus, the Macos Menu Bar shows a very basic set of menu items
# and the File -> Quit menu item does not do anthing. So actually, there is
# currently no clean way to exit the game excpet for getting killed. Thus
# we need to look at why getting killed allows a clean exit and the other
# ways do not. The first thing to consider is what is happening and what
# objects are in play in the different parts of code in play in these
# different scenarios.
def signal_handler(signal, frame):
    if DEBUG:
        print "SIGNAL: {}  FRAME: {}".format(signal, frame)
    print "EXITING for keyboard interrupt (CTRL-C)."
    # try:
    #     if window is not None:
    #         window.bye()
    # except Exception:
    #     pass
    # sys.exit(0)


# See comments above as we are still looking for a total clean-exit solution.
signal.signal(signal.SIGINT, signal_handler)

# Playing area of grid will be 600 x 600 with 50 padding all around, hence
# the window size of 700 x 700
WINDOW_WIDTH = 840
WINDOW_HEIGHT = 840
WINDOW_STARTX = 0
WINDOW_STARTY = 0

UNIT_SIZE = 32  # Individual grid units are 24 x 24 pixels each
UNITS = 25  # Number of grid units in any row or column of the square grid
HALF_GRID_UNITS_WHOLE = int(UNITS / 2)  # int() drops remainder
SPLIT = (HALF_GRID_UNITS_WHOLE * UNIT_SIZE)
if DEBUG:
    print "HALF_GRID_UNITS_WHOLE: {}".format(HALF_GRID_UNITS_WHOLE)
    print "SPLIT: {}".format(SPLIT)

window = turtle.Screen()
window.colormode(255)
window.bgcolor(10, 71, 4)
window.title("Dia Dungeon Mazer")
window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
             startx=WINDOW_STARTX, starty=WINDOW_STARTY)
window.tracer(0)

# Access Tkinter canvas object to bring Turtle window to the foreground.
# TODO: This brings window to front BUT DOES NOT give focus so the keys
# have no effect until you click on the window. Only half the problem solved.
# To to also give windoe focus.
canvas = window.getcanvas().winfo_toplevel()
canvas.call("wm", "attributes", ".", "-topmost", "1")
canvas.call("wm", "attributes", ".", "-topmost", "0")

sprites = [
            "cave_wall32x32.gif",
            "grey_stone32x32.gif",
            "stairs_dn_left32x32.gif",
            "stairs_dn_right32x32.gif",
            "player_left32x32.gif",
            "player_right32x32.gif",
            "cyclops_left32x32.gif",
            "cyclops_right32x32.gif",
            "dragon_left32x32.gif",
            "dragon_right32x32.gif",
            "treasure_chest32x32.gif"
            ]

for sprite in sprites:
    turtle.register_shape(sprite)


class Pen(turtle.Turtle):
    def __init__(self):
        # turtle.Turtle.__init__(self)  # Equivalent to following line
        super(Pen, self).__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):
    def __init__(self):
        # turtle.Turtle.__init__(self)  # Equivalent to following line
        super(Player, self).__init__()
        self.shape("player_right32x32.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.score = 0

    def up(self):
        newx = self.xcor()
        newy = self.ycor() + UNIT_SIZE
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def dn(self):
        newx = self.xcor()
        newy = self.ycor() - UNIT_SIZE
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def lt(self):
        newx = self.xcor() - UNIT_SIZE
        newy = self.ycor()
        self.shape("player_left32x32.gif")
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def rt(self):
        newx = self.xcor() + UNIT_SIZE
        newy = self.ycor()
        self.shape("player_right32x32.gif")
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        d = math.sqrt((a ** 2) + (b ** 2))
        if d < 5:
            return True
        else:
            return False


class Monster(turtle.Turtle):
    def __init__(self, x, y, mon_type,
                 mon_shape_left, mon_shape_right, mon_max_pause):
        # turtle.Turtle.__init__(self)  # Equivalent to following line
        super(Monster, self).__init__()
        self.type = mon_type
        self.shape_left = mon_shape_left
        self.shape_right = mon_shape_right
        self.max_pause = mon_max_pause
        self.shape(self.shape_right)
        self.color("red")
        self.penup()
        self.speed(0)
        self.booty = 50
        self.goto(x, y)
        self.direction = random.choice(["up", "dn", "lt", "rt"])

    def move(self):
        if self.direction == "up":
            deltax = 0
            deltay = UNIT_SIZE
        elif self.direction == "dn":
            deltax = 0
            deltay = 0 - UNIT_SIZE
        elif self.direction == "lt":
            deltax = 0 - UNIT_SIZE
            deltay = 0
            self.shape(self.shape_left)
        elif self.direction == "rt":
            deltax = UNIT_SIZE
            deltay = 0
            self.shape(self.shape_right)
        else:  # For completeness of logic here even though it looks like
                # a direction will always be set and this else block may
                # never be hit. Maybe in the future monsters can stand
                # still, meaning they have no direction and in that case
                # we might want this else block. Even then we might not
                # explicitly need it for the code to work but it is more
                # correct to have it in place.
            deltax = 0
            deltay = 0

        if self.nearby(player):
            if player.xcor() < self.xcor():
                self.direction = "lt"
            elif player.xcor() > self.xcor():
                self.direction = "rt"
            elif player.ycor() < self.ycor():
                self.direction = "dn"
            elif player.ycor() > self.ycor():
                self.direction = "up"
            # NOTE: The above is biased such that horizantal following always
            # occurs before vertical following

        newx = self.xcor() + deltax
        newy = self.ycor() + deltay

        if (newx, newy) not in walls:
            self.goto(newx, newy)
        else:
            self.direction = random.choice(["up", "dn", "lt", "rt"])

        turtle.ontimer(self.move, t=random.randint(100, self.max_pause))

    def nearby(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def dispose(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        super(Treasure, self).__init__()
        self.shape("treasure_chest32x32.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.value = 100
        self.goto(x, y)

    def dispose(self):
        self.goto(2000, 2000)
        self.hideturtle()


treasures = []

levels = [""]

level_1_25 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP                      X",
    "X  XXXXX XXX XXXX XXXXX X",
    "X XXX    XXX XXXX XT  X X",
    "X X   XXXX      X X     X",
    "X       CXXX XX X X  CX X",
    "XXXXXXXXXXXX XX X XXXXX X",
    "X    XX    X X  X X   X X",
    "X X      X   X  X     X X",
    "X X      X   X  X X   X X",
    "X    XX    X XXXX XXXXXXX",
    "XXXXXXXXXX X   XX       X",
    "X          X   XXXXXXXX X",
    "X XXXXXX XXXX XXXX X    X",
    "X XXXX     XX XD   X XX X",
    "X   XX     XX XXXX   XX X",
    "X  CXX T   XX XC    XXXXX",
    "XXX XX     XX XXXXX     X",
    "X   XXXXXXXXX XX XXXX X X",
    "X XXX             XXX XXX",
    "X XXXX XX X X X XXXXD   X",
    "X    X XX       XX   XX X",
    "XXXX X  X X X X XX XXX  X",
    "XC   XX X    C  XX   X =X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Just for testing
level_1_24 = [
    "XXXXXXXXXXXXXXXXXXXXXXXX",
    "XP                     X",
    "X XXXXX XXX XXXX XXXXX X",
    "X XX    XXX XXXX XT  X X",
    "X X  XXXX      X X     X",
    "X       XXX XX X X   X X",
    "XXXXXXXXXXX XX X XXXXX X",
    "X   XX    X X  X X   X X",
    "X X     X   X  X X   X X",
    "X   XX    X XXXX XXXXXXX",
    "XXXXXXXXX X   XX       X",
    "X         X   XXXXXXXX X",
    "X XXXXX XXXX XXXX X    X",
    "X XXX     XX X    X XX X",
    "X  XX     XX XXXX   XX X",
    "X  XX T   XX X     XXXXX",
    "XX XX     XX XXXXX     X",
    "X  XXXXXXXXX XX XXXX X X",
    "X XX             XXX XXX",
    "X XXX XX X X X XXXX    X",
    "X   X XX       XX   XX X",
    "XXX X  X X X X XX XXX  X",
    "X   XX X       XX   X =X",
    "XXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1_25)


def validate_maze(level):
    rows = len(level)
    if not rows == UNITS:
        print "FATAL ERROR: Maze/level data row count does not match global " \
            "configuration for UNITS. The level contains {} rows but it " \
            "should contain exactly {} rows.".format(rows, UNITS)
        exit(1)
    for y in range(rows):
        row = level[y]
        row_units = len(row)
        if not row_units == UNITS:
            print "FATAL ERROR: Maze/level data row UNITS in row " \
                "{} (0 indexed) does not match global configuration " \
                "for UNITS. Row contains {} units but it should contain " \
                "exactly {} units.".format(y, row_units, UNITS)
            exit(1)
        for x in range(row_units):
            unit = level[y][x]
            if not unit in "X =TCDP":
                print "WARNING: Unrecognized unit type in maze/level data " \
                    "at (0 indexed) position {} and row {}".format(x, y)


def setup_maze(level, walls):
    rows = len(level)
    for y in range(rows):
        row = level[y]
        row_units = len(row)
        for x in range(row_units):
            unit = level[y][x]
            screen_x = (0 - SPLIT) + (x * UNIT_SIZE)
            screen_y = SPLIT - (y * UNIT_SIZE)

            if unit == "=":
                pen.goto(screen_x, screen_y)
                pen.shape("stairs_dn_right32x32.gif")
                pen.stamp()

            if unit == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("cave_wall32x32.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))


def setup_beings(level):
    rows = len(level)
    for y in range(rows):
        row = level[y]
        row_units = len(row)
        for x in range(row_units):
            unit = level[y][x]
            screen_x = (0 - SPLIT) + (x * UNIT_SIZE)
            screen_y = SPLIT - (y * UNIT_SIZE)

            if unit == "T":
                treasures.append(Treasure(screen_x, screen_y))

            if unit == "C":
                monsters.append(Monster(screen_x, screen_y, "cyclops",
                                        "cyclops_left32x32.gif",
                                        "cyclops_right32x32.gif",
                                        450))

            if unit == "D":
                monsters.append(Monster(screen_x, screen_y, "dragon",
                                        "dragon_left32x32.gif",
                                        "dragon_right32x32.gif",
                                        150))

            if unit == "P":
                player.goto(screen_x, screen_y)


pen = Pen()
player = Player()

walls = []

monsters = []

validate_maze(levels[1])
setup_maze(levels[1], walls)
setup_beings(levels[1])

turtle.listen()
turtle.onkey(player.lt, "Left")
turtle.onkey(player.rt, "Right")
turtle.onkey(player.up, "Up")
turtle.onkey(player.dn, "Down")

turtle.onkey(player.lt, "a")
turtle.onkey(player.rt, "d")
turtle.onkey(player.up, "w")
turtle.onkey(player.dn, "s")

window.tracer(0)

for monster in monsters:
    turtle.ontimer(monster.move, t=250)

loop = True
try:
    while (loop is True):
        for treasure in treasures:
            if player.collision(treasure):
                player.score += treasure.value
                print("Player gold pieces: {}".format(player.score))
                treasure.dispose()
                treasures.remove(treasure)

        for monster in monsters:
            if player.collision(monster):
                print "You died a horrible death " \
                    "at the hands of a {}!".format(monster.type)
                loop = False

        window.update()
except Exception as e:
    e_string = str(e)
    if DEBUG:
        print "Main loop caught Exception: {}".format(e_string)
    if e_string == "turtle.Terminator":
        print "EXITING."
        time.sleep(1)
        sys.exit(0)

# TODO: Can't do window.bye() here for the case of a mouse-click-closed
# macos window. this worked fine for ending the game from code, but throws
# an ugly error for exception-caight exiting because there is no longer
# a window object to call bye() against. Solution is to exit correctly,
# perhaps using window.bye() but DO SO IN THE CODE WHERE GAME IS ENDING,
# not here as a catchall the is hit whe the exception handling falls through.
window.bye()
sys.exit(0)

##
#
