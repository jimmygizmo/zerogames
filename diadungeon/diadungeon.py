import turtle
import math
import random

DEBUG = False

# Playing area of grid will be 600 x 600 with 50 padding all around, hence
# the window size of 700 x 700
WINDOW_WIDTH = 840
WINDOW_HEIGHT = 840
UNIT_SIZE = 32  # Individual grid units are 24 x 24 pixels each
UNITS = 25  # Number of grid units in any row or column of the square grid
HALF_GRID_UNITS_WHOLE = int(UNITS / 2)  # int() drops remainder
SPLIT = (HALF_GRID_UNITS_WHOLE * UNIT_SIZE)
if DEBUG:
    print "HALF_GRID_UNITS_WHOLE: {}".format(HALF_GRID_UNITS_WHOLE)
    print "SPLIT: {}".format(SPLIT)

window = turtle.Screen()
window.bgcolor("dark green")
window.title("Dia Dungeon Mazer")
window.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
window.tracer(0)

sprites = [
            "cave_wall32x32.gif",
            "player_right32x32.gif",
            "player_left32x32.gif",
            "cyclops_right32x32.gif",
            "cyclops_left32x32.gif",
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
        newx = player.xcor()
        newy = player.ycor() + UNIT_SIZE
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def dn(self):
        newx = player.xcor()
        newy = player.ycor() - UNIT_SIZE
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def lt(self):
        newx = player.xcor() - UNIT_SIZE
        newy = player.ycor()
        self.shape("player_left32x32.gif")
        if (newx, newy) not in walls:
            self.goto(newx, newy)

    def rt(self):
        newx = player.xcor() + UNIT_SIZE
        newy = player.ycor()
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


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        super(Treasure, self).__init__()
        self.shape("treasure_chest32x32.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.value = 100
        self.goto(x, y)

    def destroy(self):
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
    "X        XXX XX X X   X X",
    "XXXXXXXXXXXX XX X XXXXX X",
    "X    XX    X X  X X   X X",
    "X X      X   X  X     X X",
    "X X      X   X  X X   X X",
    "X    XX    X XXXX XXXXXXX",
    "XXXXXXXXXX X   XX       X",
    "X          X   XXXXXXXX X",
    "X XXXXXX XXXX XXXX X    X",
    "X XXXX     XX X    X XX X",
    "X   XX     XX XXXX   XX X",
    "X   XX T   XX X     XXXXX",
    "XXX XX     XX XXXXX     X",
    "X   XXXXXXXXX XX XXXX X X",
    "X XXX             XXX XXX",
    "X XXXX XX X X X XXXX    X",
    "X    X XX       XX   XX X",
    "XXXX X  X X X X XX XXX  X",
    "X    XX X       XX   X  X",
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
    "X   XX X       XX   X  X",
    "XXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1_25)


def setup_maze(level, walls):
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
            character = level[y][x]
            screen_x = (0 - SPLIT) + (x * UNIT_SIZE)
            screen_y = SPLIT - (y * UNIT_SIZE)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("cave_wall32x32.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))


pen = Pen()
player = Player()

walls = []

setup_maze(levels[1], walls)

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

while True:
    for treasure in treasures:
        if player.collision(treasure):
            player.score += treasure.value
            print("Player gold pieces: {}".format(player.score))
            treasure.destroy()
            treasures.remove(treasure)

    window.update()

##
#
