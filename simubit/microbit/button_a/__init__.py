_counter = 0


def is_pressed():
    global _counter
    _counter = (_counter + 1) % 11
    return _counter == 0
