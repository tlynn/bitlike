import microbit as _microbit


def badaboom():
    bright = [0.0, 1.0/9, 2.0/9, 4.0/9, 6.0/9, 7.0/9, 1.0]

    interval = 25
    hearts = []
    for i in range(len(bright)):
        hearts.append(_microbit.Image.HEART * bright[i])

    for iteration in range(8):
        # pause between double beats of the heart
        if iteration and (iteration & 1) == 0:
            _microbit.sleep(20 * interval)

        # pulse heart to max brightness
        for step in range(len(bright)):
            _microbit.display.print(hearts[step])
            _microbit.sleep(interval)

        # pulse heart to min brightness
        for step in reversed(range(len(bright))):
            _microbit.display.print(hearts[step])
            _microbit.sleep(interval)

    _microbit.display.clear()


badaboom()
