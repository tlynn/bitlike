#!/usr/bin/env python3
'''
bitlike, a micro:bit simulator.

See __init__.py for license.
'''

import sys
import os
import runpy

from . import start_gui, gui_call


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: %s SCRIPT [...]' % sys.argv[0])

    start_gui()

    path = os.path.dirname(sys.modules[__name__].__file__)
    sys.path.insert(0, path)

    try:
        sys.argv = sys.argv[1:]
        runpy.run_path(sys.argv[0])
    except KeyboardInterrupt:
        pass
    finally:
        gui_call('quit', ())


if __name__ == '__main__':
    main()
