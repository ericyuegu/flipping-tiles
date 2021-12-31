# import modules
import random
import time
from turtle import *

# Board dimensions
HEIGHT = 6
WIDTH = 6
NUM_TILES = HEIGHT * WIDTH
# Pixel width of square tiles
TILE_SIZE = 60


screen = Screen()
screen.bgcolor("black")


def Square(x, y):
    up()
    goto(x, y)
    down()
    color('black', 'lavender')
    begin_fill()
    for count in range(4):
        forward(TILE_SIZE)
        left(90)
    end_fill()


def Numbering(x, y):
    """Get tile index for x, y coordinate."""
    return int((x + (TILE_SIZE * WIDTH / 2)) // TILE_SIZE +
               ((y + (TILE_SIZE * HEIGHT / 2)) // TILE_SIZE) * HEIGHT)


def Coordinates(n):
    """Get x, y coordinates for nth tile."""
    return (n % WIDTH) * TILE_SIZE - (TILE_SIZE * WIDTH / 2), \
           (n // HEIGHT) * TILE_SIZE - (TILE_SIZE * HEIGHT / 2)


def click(x, y):
    if abs(x) > (TILE_SIZE * WIDTH / 2) or abs(y) > (TILE_SIZE * HEIGHT / 2):
        return
    spot = Numbering(x, y)
    mark = state['mark']

    if mark is None or mark == spot:
        state['mark'] = spot
    elif deleted[spot]:
        pass
    else:
        state['prev'] = state['mark']
        state['mark'] = spot


def animate_match(a, b):
    deleted[a] = True
    deleted[b] = True


def clear_state():
    state['prev'] = None
    state['mark'] = None


def write_tile(tile, x, y):
    up()
    goto(x + TILE_SIZE // 4, y + TILE_SIZE // 4)
    color('black')
    write(tiles[tile], font=('Arial', 30, 'normal'))


def draw():
    clear()
    goto(0, 0)
    stamp()

    for count in range(NUM_TILES):
        if hide[count] and not deleted[count]:
            x, y = Coordinates(count)
            Square(x, y)

    mark = state['mark']
    prev = state['prev']

    if prev:
        x, y = Coordinates(prev)
        write_tile(prev, x, y)

    if mark:
        x, y = Coordinates(mark)
        write_tile(mark, x, y)

    if mark and prev:
        if tiles[mark] != tiles[prev]:
            hide[prev] = True
            hide[mark] = True
            clear_state()
            time.sleep(1)
        elif tiles[mark] == tiles[prev]:
            animate_match(mark, prev)
            clear_state()
            time.sleep(1)

    update()
    ontimer(draw, 10)


def load_vocabulary(fp: str):
    with open(fp) as f:
        tiles = [line.rstrip(',\n') for line in f]
    return tiles


vocab = load_vocabulary('top500.txt')
tiles = random.sample(vocab, NUM_TILES // 2) * 2
state = {'mark': None, 'prev': None}
hide = [True] * NUM_TILES
doomed = [False] * NUM_TILES
deleted = [False] * NUM_TILES


tracer(False)
hideturtle()
onscreenclick(click)
draw()
done()