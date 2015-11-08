import simubit as _simubit
import microbit as _microbit

from builtins import print as _print


_pixels = [[0, 0, 0, 0, 0] for i in range(5)]


def set_pixel(x, y, glow):
    if not isinstance(x, (int, float)):
        raise TypeError()
    if not isinstance(y, (int, float)):
        raise TypeError()
    if not isinstance(glow, (int, float)):
        raise TypeError()
    _pixels[y][x] = glow
    _simubit.gui_call('set_pixel', (x, y, glow))


def get_pixel(x, y):
    return _pixels[y][x]


def clear():
    global _pixels
    _pixels = [[0, 0, 0, 0, 0] for i in range(5)]
    _simubit.gui_call('clear', ())


def print(msg):
    if hasattr(msg, 'get_pixel'):
        for y in range(5):
            for x in range(5):
                set_pixel(x, y, msg.get_pixel(x, y))
    else:
        _print(msg)


def scroll(msg):
    # TODO: Font.
    _print(msg)


def animate(image, delay, *, stride=5, start=-5, wait=True, loop=False):
    # TODO: full impl.
    for frame in image:
        for y in range(frame.height()):
            for x in range(frame.width()):
                glow = frame.get_pixel(x, y)
                set_pixel(x, y, glow)
        _microbit.sleep(delay)
