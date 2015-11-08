import time as _time
import random as _random

from . import accelerometer
from . import button_a
from . import button_b
from . import display


_start_time = _time.time()


def random(n):
    return _random.randrange(n)


def sleep(ms):
    return _time.sleep(ms * 0.001)


def running_time():
    return 1000 * (_time.time() - _start_time)


class Image:
    def __init__(self, *args):
        if len(args) == 1:
            text = args[0].strip()
            self._pixels = [[0, 0, 0, 0, 0] for i in range(5)]
            for y, line in enumerate(text.splitlines()):
                for x, word in enumerate(line.rstrip(',').split(',')):
                    self.set_pixel(x, y, int(word) * 9)
        elif len(args) == 2:
            w, h = args
            self._pixels = [[0] * w for i in range(h)]
        elif len(args) == 3:
            # TODO: TEST THIS
            w, h, values = args
            it = iter(values)
            self._pixels = [[0] * w for i in range(h)]
            for y in range(h):
                for x in range(w):
                    self.set_pixels(x, y, next(it))
        else:
            raise TypeError('Image() takes 0 to 3 arguments')

    def crop(self, x, y, w, h):
        ix0, iy0, w, h = max(0, x), max(0, y), max(0, w), max(0, h)
        ix1, iy1 = min(self.width(), x+w), min(self.height(), y+h)
        result = self.__class__(w, h)
        for i in range(ix0, ix1):
            for j in range(iy0, iy1):
                glow = self.get_pixel(i, j)
                result.set_pixel(i-x, j-y, glow)
        return result

    def set_pixel(self, x, y, glow):
        if not isinstance(x, (int, float)):
            raise TypeError()
        if not isinstance(y, (int, float)):
            raise TypeError()
        if not isinstance(glow, (int, float)):
            raise TypeError()
        self._pixels[y][x] = glow

    def get_pixel(self, x, y):
        return self._pixels[y][x]

    def width(self):
        return len(self._pixels[0]) if self._pixels else 0

    def height(self):
        return len(self._pixels)

    def __add__(self, other):
        result = self.crop(0, 0, self.width(), self.height())
        for y in range(self.height()):
            for x in range(self.width()):
                glow = self.get_pixel(x, y)
                if isinstance(other, self.__class__):
                    glow += other.get_pixel(x, y)
                else:
                    glow += other
                self.set_pixel(x, y, glow)
        return result

    def __mul__(self, other):
        result = self.crop(0, 0, self.width(), self.height())
        for y in range(self.height()):
            for x in range(self.width()):
                glow = self.get_pixel(x, y)
                if isinstance(other, self.__class__):
                    glow *= other.get_pixel(x, y)
                else:
                    glow *= other
                self.set_pixel(x, y, glow)
        return result

    def __sub__(self, other):
        # TODO: does this exist?
        result = self.crop(0, 0, self.width(), self.height())
        for y in range(self.height()):
            for x in range(self.width()):
                glow = self.get_pixel(x, y)
                if isinstance(other, self.__class__):
                    glow -= other.get_pixel(x, y)
                else:
                    glow -= other
                self.set_pixel(x, y, glow)
        return result

    def __div__(self, other):
        # TODO: does this exist?
        result = self.crop(0, 0, self.width(), self.height())
        for y in range(self.height()):
            for x in range(self.width()):
                glow = self.get_pixel(x, y)
                if isinstance(other, self.__class__):
                    glow /= other.get_pixel(x, y)
                else:
                    glow /= other
                self.set_pixel(x, y, glow)
        return result

    def __idiv__(self, other):
        # TODO: does this exist?
        result = self.crop(0, 0, self.width(), self.height())
        for y in range(self.height()):
            for x in range(self.width()):
                glow = self.get_pixel(x, y)
                if isinstance(other, self.__class__):
                    glow //= other.get_pixel(x, y)
                else:
                    glow //= other
                self.set_pixel(x, y, glow)
        return result

Image.HEART = Image('''
    0,1,0,1,0,
    1,1,1,1,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,0,1,0,0
''')

Image.HEART_SMALL = Image('''
    0,0,0,0,0,
    0,1,0,1,0,
    0,1,1,1,0,
    0,0,1,0,0,
    0,0,0,0,0
''')

# smilies

Image.HAPPY = Image('''
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    1,0,0,0,1,
    0,1,1,1,0
''')

Image.SMILE = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    1,0,0,0,1,
    0,1,1,1,0
''')

Image.SAD = Image('''
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    0,1,1,1,0,
    1,0,0,0,1
''')

Image.CONFUSED = Image('''
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    0,1,0,1,0,
    1,0,1,0,1
''')

Image.ANGRY = Image('''
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,0,0,0,
    1,1,1,1,1,
    1,0,1,0,1
''')

Image.ASLEEP = Image('''
    0,0,0,0,0,
    1,1,0,1,1,
    0,0,0,0,0,
    0,1,1,1,0,
    0,0,0,0,0
''')

Image.SURPRISED = Image('''
    0,1,0,1,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    0,0,1,0,0
''')

Image.SILLY = Image('''
    1,0,0,0,1,
    0,0,0,0,0,
    1,1,1,1,1,
    0,0,1,0,1,
    0,0,1,1,1
''')

Image.FABULOUS = Image('''
    1,1,1,1,1,
    1,1,0,1,1,
    0,0,0,0,0,
    0,1,0,1,0,
    0,1,1,1,0
''')

Image.MEH = Image('''
    0,1,0,1,0,
    0,0,0,0,0,
    0,0,0,1,0,
    0,0,1,0,0,
    0,1,0,0,0
''')

# yes/no

Image.YES = Image('''
    0,0,0,0,0,
    0,0,0,0,1,
    0,0,0,1,0,
    1,0,1,0,0,
    0,1,0,0,0
''')

Image.NO = Image('''
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1
''')

# clock hands

Image.CLOCK12 = Image('''
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK1 = Image('''
    0,0,0,1,0,
    0,0,0,1,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK2 = Image('''
    0,0,0,0,0,
    0,0,0,1,1,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK3 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,1,1,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK4 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,1,1,
    0,0,0,0,0
''')

Image.CLOCK5 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,1,0,
    0,0,0,1,0
''')

Image.CLOCK6 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0
''')

Image.CLOCK7 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,0,0,
    0,1,0,0,0
''')

Image.CLOCK8 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    1,1,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK9 = Image('''
    0,0,0,0,0,
    0,0,0,0,0,
    1,1,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK10 = Image('''
    0,0,0,0,0,
    1,1,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

Image.CLOCK11 = Image('''
    0,1,0,0,0,
    0,1,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0
''')

# arrows

Image.ARROW_N = Image('''
    0,0,1,0,0,
    0,1,1,1,0,
    1,0,1,0,1,
    0,0,1,0,0,
    0,0,1,0,0
''')

Image.ARROW_NE = Image('''
    0,0,1,1,1,
    0,0,0,1,1,
    0,0,1,0,1,
    0,1,0,0,0,
    1,0,0,0,0
''')

Image.ARROW_E = Image('''
    0,0,1,0,0,
    0,0,0,1,0,
    1,1,1,1,1,
    0,0,0,1,0,
    0,0,1,0,0
''')

Image.ARROW_SE = Image('''
    1,0,0,0,0,
    0,1,0,0,0,
    0,0,1,0,1,
    0,0,0,1,1,
    0,0,1,1,1
''')

Image.ARROW_S = Image('''
    0,0,1,0,0,
    0,0,1,0,0,
    1,0,1,0,1,
    0,1,1,1,0,
    0,0,1,0,0
''')

Image.ARROW_SW = Image('''
    0,0,0,0,1,
    0,0,0,1,0,
    1,0,1,0,0,
    1,1,0,0,0,
    1,1,1,0,0
''')

Image.ARROW_W = Image('''
    0,0,1,0,0,
    0,1,0,0,0,
    1,1,1,1,1,
    0,1,0,0,0,
    0,0,1,0,0
''')

Image.ARROW_NW = Image('''
    1,1,1,0,0,
    1,1,0,0,0,
    1,0,1,0,0,
    0,0,0,1,0,
    0,0,0,0,1
''')

# geometry

Image.TRIANGLE = Image('''
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    1,1,1,1,1,
    0,0,0,0,0
''')

Image.TRIANGLE_LEFT = Image('''
    1,0,0,0,0,
    1,1,0,0,0,
    1,0,1,0,0,
    1,0,0,1,0,
    1,1,1,1,1
''')

Image.CHESSBOARD = Image('''
    0,1,0,1,0,
    1,0,1,0,1,
    0,1,0,1,0,
    1,0,1,0,1,
    0,1,0,1,0
''')

Image.DIAMOND = Image('''
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,1,0,0
''')

Image.DIAMOND_SMALL = Image('''
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    0,0,1,0,0,
    0,0,0,0,0
''')

Image.SQUARE = Image('''
    1,1,1,1,1,
    1,0,0,0,1,
    1,0,0,0,1,
    1,0,0,0,1,
    1,1,1,1,1
''')

Image.SQUARE_SMALL = Image('''
    0,0,0,0,0,
    0,1,1,1,0,
    0,1,0,1,0,
    0,1,1,1,0,
    0,0,0,0,0
''')

# animals

Image.RABBIT = Image('''
    1,0,1,0,0,
    1,0,1,0,0,
    1,1,1,1,0,
    1,1,0,1,0,
    1,1,1,1,0
''')

Image.COW = Image('''
    1,0,0,0,1,
    1,0,0,0,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,0,1,0,0
''')

# musical notes

Image.MUSIC_CROTCHET = Image('''
    0,0,1,0,0,
    0,0,1,1,0,
    0,0,1,0,1,
    1,1,1,0,0,
    1,1,1,0,0
''')

Image.MUSIC_QUAVERS = Image('''
    0,1,1,1,1,
    0,1,0,0,1,
    0,1,0,0,1,
    1,1,0,1,1,
    1,1,0,1,1
''')

# other icons

Image.PITCHFORK = Image('''
    1,0,1,0,1,
    1,0,1,0,1,
    1,1,1,1,1,
    0,0,1,0,0,
    0,0,1,0,0
''')

Image.XMAS = Image('''
    0,0,1,0,0,
    0,1,1,1,0,
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,1,1,1
''')

Image.PACMAN = Image('''
    0,1,1,1,1,
    1,1,0,1,0,
    1,1,1,0,0,
    1,1,1,1,0,
    0,1,1,1,1
''')

Image.TARGET = Image('''
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,0,1,1,
    0,1,1,1,0,
    0,0,1,0,0
''')
