from sense_hat import SenseHat, ACTION_PRESSED
import random
import signal
import time
import copy

sense = SenseHat()
sense.clear()
sense.low_light = True

snake_colour = (0, 255, 0)
snake_body_colour = (0, 255, 125)
food_colour = (255, 0, 0)
snake_coords = {}
food_coords = {}
snake_direction = ''
previous_snake_direction = ''
snake_movement_shadow = []
coord_limit = 7
coord_start = 0
score = 0
step_timer = 1
step_timer_lower_limit = 0.1

enable_debug = False


def init():
    global snake_coords
    global food_coords

    food_coords = random_coords()
    snake_coords = random_coords()

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

    if snake_direction != '':
        for i, coord in enumerate(snake_movement_shadow, start=1):
            colour = snake_body_colour
            if i == 0:
                colour = snake_colour
            debug('Drawing snake tail at: ' + str(coord['x']) + ',' + str(coord['y']))
            sense.set_pixel(coord['x'], coord['y'], colour)


def draw_food():
    debug('Drawing food at: ' + str(food_coords['x']) + ',' + str(food_coords['y']))
    sense.set_pixel(food_coords['x'], food_coords['y'], food_colour)


def update_score():
    global score

    score += 1
    print('You have scored: ' + str(score) + ' points!')


def set_direction(event):
    global snake_direction
    global previous_snake_direction

    if event.action == ACTION_PRESSED:
        previous_snake_direction = snake_direction

        # Prevent snake moving backwards over itself
        if score > 0:
            if event.direction == 'up' and previous_snake_direction == 'down':
                return

            if event.direction == 'down' and previous_snake_direction == 'up':
                return

            if event.direction == 'left' and previous_snake_direction == 'right':
                return

            if event.direction == 'right' and previous_snake_direction == 'left':
                return

        snake_direction = event.direction


def move_snake():
    global snake_coords

    debug('Moving ' + snake_direction)

    update_movement_shadow()

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


def update_movement_shadow():
    snake_movement_shadow.insert(0, copy.deepcopy(snake_coords))

    while len(snake_movement_shadow) >= score + 1:
        snake_movement_shadow.pop(-1)


def update_step_timer():
    global step_timer

    if step_timer >= step_timer_lower_limit:
        step_timer = step_timer * 0.9
        debug('Updating step timer to: ' + str(step_timer))


def make_new_food():
    global food_coords

    new_coords = random_coords()

    if new_coords in snake_movement_shadow:
        make_new_food()
    else:
        food_coords = new_coords


def end_game():
    print('Game Over!\nFinal Score: ' + str(score))
    o = (255, 69, 0)
    b = (0, 0, 0)
    skull_art = [
        b, b, o, o, o, o, b, b,
        b, o, o, o, o, o, o, b,
        o, o, b, o, o, b, o, o,
        o, b, b, o, o, b, b, o,
        o, o, o, o, o, o, o, o,
        b, o, o, b, b, o, o, b,
        b, b, o, o, o, o, b, b,
        b, b, o, b, b, o, b, b,
    ]

    i = 0
    while i <= 1:
        sense.set_pixels([(255, 255, 255)] * 64)
        time.sleep(0.2)
        sense.set_pixels([food_colour] * 64)
        time.sleep(0.2)
        i += 1

    sense.set_pixels(skull_art)
    time.sleep(2)
    sense.show_message('You scored: ' + str(score), 0.08)
    sense.clear()

    raise SystemExit(0)


def refresh():
    debug('Refreshing...')
    sense.clear()
    draw_snake()
    draw_food()
    time.sleep(step_timer)


def run_game():
    move_snake()

    if snake_coords in snake_movement_shadow:
        end_game()

    if snake_coords == food_coords:
        update_score()
        update_step_timer()
        make_new_food()

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
