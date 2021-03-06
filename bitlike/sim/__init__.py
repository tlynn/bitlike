#!/usr/bin/env python3
'''
bitlike, a micro:bit simulator.

It doesn't emulate the hardware, it just runs the Python code.
As a result, it can't handle scripts that include assembler.

This derives bits and pieces from the micro:bit/MicroPython code
(and should really derive much more), so it is under the same MIT license:

The MIT License (MIT)

Copyright (c) 2015 Tom Lynn
Copyright (c) 2015 Damien P. George

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import copy
import json
import queue
import threading


class GUI(threading.Thread):
    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.q2 = queue.Queue()
        # This is really the model, but only the gui is allowed to modify it,
        # so it's safest to only let the gui read it directly too.
        self._device_state = {
            'accelerometer': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'button_a': {
                'pressed': False,
            },
            'button_b': {
                'pressed': False,
            },
            'display': {
                'pixels': [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                ],
            },
        }

    def call(self, op_name, args):
        '''Send a message to the GUI thread and return the response.'''
        self.q.put((op_name, args))
        result = self.q2.get()
        if op_name == 'quit':
            self.join()
        return result

    def run(self):
        q, q2 = self.q, self.q2
        print(json.dumps(self._device_state))

        def loop_until_quit():
            # TODO: exceptions
            while True:
                try:
                    a = q.get(block=True)
                    if a is None:
                        break
                    op, args = a
                    if op == 'quit':
                        q2.put(None)
                        return
                    elif op == 'clear':
                        pixels = self._device_state['display']['pixels']
                        for y in range(5):
                            for x in range(5):
                                pixels[y][x] = 0
                        q2.put(None)
                    elif op == 'set_pixel':
                        x, y, glow = args
                        pixels = self._device_state['display']['pixels']
                        pixels[y][x] = int(glow)
                        print(json.dumps(self._device_state))
                        q2.put(None)
                    elif op == 'get_device_state':
                        q2.put(copy.deepcopy(self._device_state))
                    elif op == 'update_device_state':
                        kwargs, = args
                        self._device_state.update(kwargs)
                        print(json.dumps(self._device_state))
                        q2.put(None)
                    else:
                        print('Unknown op: %r' % op)
                except queue.Empty:
                    break

        loop_until_quit()


_gui = GUI()

# Public API

start_gui = _gui.start
gui_call = _gui.call


def get_device_state():
    return gui_call('get_device_state', ())


def update_device_state(**kwargs):
    gui_call('update_device_state', (kwargs,))
