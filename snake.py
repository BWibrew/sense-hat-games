from sense_hat import SenseHat, ACTION_PRESSED
import random
import signal
import time

sense = SenseHat()
sense.clear()
sense.low_light = True

snake_colour = (0, 255, 0)
food_colour = (255, 0, 0)
snake_coords = {}
food_coords = {}
snake_direction = None
coord_limit = 7
coord_start = 0
score = 0
step_time = 1

enable_debug = False


def init():
    global snake_coords
    global food_coords

    snake_coords = random_coords()
    food_coords = random_coords()

    sense.stick.direction_any = direction

    run_game()


def random_coords():
    return {
        'x': random.randint(coord_start, coord_limit),
        'y': random.randint(coord_start, coord_limit),
    }


def draw_snake():
    debug('Drawing snake at: ' + str(snake_coords['x']) + ',' + str(snake_coords['y']))
    sense.set_pixel(snake_coords['x'], snake_coords['y'], snake_colour)


def draw_food():
    debug('Drawing food at: ' + str(food_coords['x']) + ',' + str(food_coords['y']))
    sense.set_pixel(food_coords['x'], food_coords['y'], food_colour)


def eat_food():
    global score
    global food_coords

    score += 1
    food_coords = random_coords()
    print('You have scored: ' + str(score) + ' points!')


def direction(event):
    global snake_direction

    if event.action == ACTION_PRESSED:
        snake_direction = event.direction


def move_up():
    debug('Moving up')
    if snake_coords['y'] == coord_start:
        snake_coords['y'] = coord_limit
    else:
        snake_coords['y'] = snake_coords['y'] - 1


def move_right():
    debug('Moving right')
    if snake_coords['x'] == coord_limit:
        snake_coords['x'] = coord_start
    else:
        snake_coords['x'] = snake_coords['x'] + 1


def move_down():
    debug('Moving down')
    if snake_coords['y'] == coord_limit:
        snake_coords['y'] = coord_start
    else:
        snake_coords['y'] = snake_coords['y'] + 1


def move_left():
    debug('Moving left')
    if snake_coords['x'] == coord_start:
        snake_coords['x'] = coord_limit
    else:
        snake_coords['x'] = snake_coords['x'] - 1


def refresh():
    debug('Refreshing...')
    sense.clear()
    run_game()


def run_game():
    if snake_direction == 'up':
        move_up()
    elif snake_direction == 'right':
        move_right()
    elif snake_direction == 'down':
        move_down()
    elif snake_direction == 'left':
        move_left()

    if snake_coords == food_coords:
        eat_food()

    draw_snake()
    draw_food()
    time.sleep(step_time)
    refresh()


def debug(value=''):
    if enable_debug:
        print(value)


init()
signal.pause()
