import math

class QuantumInt():
    def __eq__(self, value):
        return isinstance(value, int)

class ExtraFunc():
    def __init__(self):
        pass
    def normalize_speed(self, d, s):
        if d <= s:
            return d
        frac, interger = math.modf(round(d / s, 5))
        if frac >= 0.5:
            s = d / (interger + 1)
        elif 0 < frac < 0.5:
            s = d / (interger - 1)
        return s
    def direction(self, a):
        if a != 0:
            return a / abs(a)
        else:
            return a
    def distance(self, a, b):
        dx = (b[0] - a[0])**2
        dy = (b[1] - a[1])**2
        d = math.sqrt(dx + dy)
        return round(d, 5)
            