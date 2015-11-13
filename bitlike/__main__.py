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

import atexit
import os
import platform
import signal
import sys
import tornado.ioloop
import tornado.iostream
import tornado.process
import tornado.web
import tornado.websocket

if 'bitlike' not in sys.modules:
    # Being run with "python bitlike ..." rather than "python -m bitlike ...".
    path = os.path.dirname(sys.modules[__name__].__file__)
    path = os.path.join(path, '..')
    sys.path.insert(0, path)


def read_file(path, mode='rb'):
    with open(path, mode) as f:
        return f.read()


class MainPageHandler(tornado.web.RequestHandler):
    _html = read_file(os.path.dirname(__file__) + '/static/index.html')

    def get(self):
        self.set_header('Cache-Control', 'public, max-age=31536000')
        self.write(self._html)


class JsHandler(tornado.web.RequestHandler):
    _js = read_file(os.path.dirname(__file__) + '/static/js/bitlike.js')

    def get(self):
        self.set_header('Content-type', 'text/javascript')
        self.set_header('Cache-Control', 'public, max-age=31536000')
        self.write(self._js)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    websocket_connected = False
    retcode = None

    def open(self):
        print("WebSocket opened")

        # Don't accept any more websocket connections.
        WebSocketHandler.websocket_connected = True

        def on_sim_exit(retcode):
            explain = ('ok' if retcode == 0 else 'error')
            print('Simulator ended with retcode %d (%s)' % (retcode, explain))
            WebSocketHandler.retcode = retcode
            # End the program.
            self.close()
            tornado.ioloop.IOLoop.current().stop()

        def read_stdout():
            try:
                sim.stdout.read_until(b'\n', on_stdout_line, max_bytes=8192)
            except tornado.iostream.StreamClosedError:
                pass

        def read_stderr():
            try:
                sim.stderr.read_until(b'\n', on_stderr_line, max_bytes=8192)
            except tornado.iostream.StreamClosedError:
                pass

        def on_stdout_line(data):
            try:
                line = data.decode('utf-8')
                self.write_message(line)
            except tornado.websocket.WebSocketClosedError:
                print('WebSocket closed while writing')
                stop_sim()
            finally:
                read_stdout()

        def on_stderr_line(data):
            try:
                line = data.decode('utf-8')
                print('ERROR: ' + line, end='')
            finally:
                read_stderr()

        def stop_sim():
            if WebSocketHandler.retcode is None:
                print("Stopping simulator")
                # The sim is safe to terminate instantly, so do that.
                if platform.system() == 'Windows':
                    os.kill(sim.pid, signal.CTRL_BREAK_EVENT)
                else:
                    os.kill(sim.pid, signal.SIGKILL)

        sim = start_simulator(sys.argv[2:])
        atexit.register(stop_sim)
        sim.set_exit_callback(on_sim_exit)
        read_stdout()
        read_stderr()

    def on_message(self, message):
        print("WebSocket received message: %r" % (message,))

    def on_close(self):
        print("WebSocket closed")

    def close(self, code=None, reason=None):
        print("WebSocket closing")
        super().close(code=code, reason=reason)

    def check_origin(self, origin):
        return not WebSocketHandler.websocket_connected


def start_simulator(target_script_args):
    cmd = [sys.executable, '-u', '-m', 'bitlike.sim']
    cmd += target_script_args
    sim = tornado.process.Subprocess(
        cmd,
        env={'PYTHONPATH': os.path.dirname(__file__) + '/..'},
        stdin=open(os.devnull, 'rb'),
        stdout=tornado.process.Subprocess.STREAM,
        stderr=tornado.process.Subprocess.STREAM)
    print('Simulator started with pid %d' % sim.pid)
    return sim


def make_app():
    return tornado.web.Application([
        (r"/", MainPageHandler),
        (r"/js/bitlike.js", JsHandler),
        (r"/websocket", WebSocketHandler),
    ])


def main():
    argv0 = sys.argv[0].rstrip('/\\')
    basename = os.path.splitext(os.path.basename(argv0))[0]
    if basename in ['__main__', 'bitlike']:
        # "python <directory> ..." or "python -m <module>" has somehow lost
        # the usual sys.argv[0] ("python").  Put it back.
        sys.argv.insert(0, sys.executable)

    if len(sys.argv) < 2:
        sys.exit('usage: %s SCRIPT [...]' % sys.argv[0])

    app = make_app()
    app.listen(8888)
    print('Serving at http://localhost:8888/')
    tornado.ioloop.IOLoop.current().start()
    sys.exit(WebSocketHandler.retcode)


if __name__ == "__main__":
    main()
