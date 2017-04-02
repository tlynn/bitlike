"""
A snake that chases around the outside and responds to the buttons.

The tail being darker made it more complicated than I expected.
"""

import microbit
import random

# "pixels" are the glowing lights on the display (also called "LEDs").
pixel_names = 'ABCDEFGHIJKLMNOPQRSTUVWXY'
pixel_name_rows = ['ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY']
pixel_positions = {pixel_name: (x, y) for y, row in enumerate(pixel_name_rows)
                                      for x, pixel_name in enumerate(row)}

glows = [0, 2, 4, 6, 7, 7, 9]  # Brightnesses along the snake, going ->.
path  = 'ABCDEJOTYXWVUPKF'     # The path for the snake to follow.
snake = 'ABCDEJO'              # The snake, or the last places its head went.
clockwise = True

while True:
    # Change 'clockwise' if any buttons are pressed.
    A = microbit.button_a.is_pressed()
    B = microbit.button_b.is_pressed()
    if A and not B:
        clockwise = True
    if B and not A:
        clockwise = False
    if A and B:
        clockwise = random.choice([True, False])

    # Find where the snake's head (snake[-1]) should move to along the path.
    head_pos = path.index(snake[-1])
    head_pos = head_pos + (1 if clockwise else -1)
    if head_pos == len(path):
        head_pos = 0
    elif head_pos < 0:
        head_pos = head_pos + len(path)
    # Add that pixel to the snake.
    snake += path[head_pos]
    # Remove snake[0], so the snake doesn't grow.
    snake = snake[1:]

    snake_pixel_glows = {}
    # For each pixel along 'snake', set the matching brightness from 'glows'.
    for pixel_name, brightness in zip(snake, glows):
        # Only ever make the snake brighter at each pixel,
        # so the snake's dark tail doesn't look like a hole in the snake
        # if it turns around and goes back on itself.
        old_brightness = snake_pixel_glows.get(pixel_name)
        if old_brightness is None or brightness > old_brightness:
            snake_pixel_glows[pixel_name] = brightness

    # Draw the snake.
    # The zero at the snake's tail (glows[0]) is what erases it.
    for pixel_name in snake_pixel_glows:
        x, y = pixel_positions[pixel_name]
        microbit.display.set_pixel(x, y, snake_pixel_glows[pixel_name])

    microbit.sleep(50)
