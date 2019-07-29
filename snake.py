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
snake_direction = ''
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

    sense.stick.direction_any = set_direction

    while True:
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
    global step_time

    score += 1
    if step_time >= 0.1:
        step_time = step_time*0.9
    food_coords = random_coords()
    print('You have scored: ' + str(score) + ' points!')


def set_direction(event):
    global snake_direction

    if event.action == ACTION_PRESSED:
        snake_direction = event.direction


def move_snake():
    debug('Moving ' + snake_direction)
    if snake_direction == 'up' or snake_direction == 'down':
        axis = 'y'
    else:
        axis = 'x'

    if snake_direction == 'up' or snake_direction == 'left':
        if snake_coords[axis] == coord_start:
            snake_coords[axis] = coord_limit
        else:
            snake_coords[axis] = snake_coords[axis] - 1

    if snake_direction == 'down' or snake_direction == 'right':
        if snake_coords[axis] == coord_limit:
            snake_coords[axis] = coord_start
        else:
            snake_coords[axis] = snake_coords[axis] + 1


def refresh():
    debug('Refreshing...')
    sense.clear()
    draw_snake()
    draw_food()
    time.sleep(step_time)


def run_game():
    move_snake()

    if snake_coords == food_coords:
        eat_food()

    refresh()


def debug(value=''):
    if enable_debug:
        print(value)


if __name__ == '__main__':
    try:
        init()
        signal.pause()
    except KeyboardInterrupt:
        sense.clear()
