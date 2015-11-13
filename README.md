bitlike, a micro:bit simulator
==============================

It's not complete, but a few of the [micro:bit examples][1] work.
It runs in your browser.

[1]: https://github.com/bbcmicrobit/micropython/tree/master/examples

This is not the official Touch Develop simulator, which is described
[here][2], and is doubtless more capable in every way :-).  In particular, it
probably emulates the hardware, which is a much more reliable approach.

[2]: https://www.touchdevelop.com/microbit/

This is just a toy.


How to install
--------------

Create and activate a Python 3 [virtualenv directory], then run:

    pip install -U -r prereqs.txt
    pip install -U -r requirements.txt

[virtualenv directory]: https://github.com/tlynn/virtualenv-guide


How to use
----------

    python3 -m bitlike examples/snake.py

It will print "`Serving at http://localhost:8888/`".
Follow the link, or copy it into your browser.

You can stop the simulator by holding down Ctrl and pressing 'c' (Ctrl-C).

You can keep the browser window open and reuse it if you run another
simulation.
