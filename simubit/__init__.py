#!/usr/bin/env python3
'''
A very hacky and incomplete micro:bit simulator using Tkinter.

That's "simulator" as in, it behaves roughly the same, rather than behaving
actually the same, which I'd call an "emulator".  (Some people prefer to use
those terms the other way around).  As a result, it can't handle scripts that
include assembler.

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

import os
import platform
import queue
import signal
import threading
import tkinter


class GUI(threading.Thread):
    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.q2 = queue.Queue()

    def call(self, op_name, args):
        '''Send a message to the GUI thread and return the response.'''
        self.q.put((op_name, args))
        return self.q2.get()

    def run(self):
        q, q2 = self.q, self.q2
        window = tkinter.Tk()
        window.config(bg='black')
        pixel_labels = []
        for y in range(5):
            row_labels = []
            for x in range(5):
                label = tkinter.Label(window, text='  ')
                label.grid(row=y, column=x)
                label.config(fg='black', bg='black')
                row_labels.append(label)
            pixel_labels.append(row_labels)

        def do_queued_calls():
            while True:
                try:
                    a = q.get(block=False)
                    if a is None:
                        break
                    op, args = a
                    if op == 'quit':
                        q2.put(window.quit())
                        return
                    elif op == 'clear':
                        for row in pixel_labels:
                            for label in row:
                                label.config(bg='black')
                        q2.put(None)
                    elif op == 'set_pixel':
                        x, y, glow = args
                        bg = '#%02x0000' % min(255, max(0, int((glow*255)/9.)))
                        pixel_labels[y][x].config(bg=bg)
                        q2.put(None)
                    else:
                        print('Unknown op: %r' % op)
                except queue.Empty:
                    break
            window.after(1, do_queued_calls)

        window.after(1, do_queued_calls)

        def on_closing():
            if platform.system() == 'Windows':
                os.kill(0, signal.CTRL_C_EVENT)
            else:
                os.kill(os.getpid(), signal.SIGINT)

        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.mainloop()


_gui = GUI()

# public
start_gui = _gui.start
gui_call = _gui.call
