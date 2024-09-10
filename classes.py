from structs import Line
from math import cos, sin, pi
from datetime import datetime

class Clock:
    _hand_thicknesses = {
        'second': 2,
        'minute': 5,
        'hour': 5
    }

    _hand_length_scales = {
        'second': 0.85,
        'minute': 0.85,
        'hour': 0.4
    }

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def get_ticks(self) -> list[Line]:
        n_ticks = 60
        ticks = []

        for sign in [-1, 1]:
            for i in range(n_ticks):
                thickness = 10 if i % 5 == 0 else 1;

                a = pi * i / (n_ticks/2)
                
                r1 = self.radius * 0.9
                r2 = self.radius * 0.95

                c1 = self._polar_to_cartesian(sign * r1, a)
                c2 = self._polar_to_cartesian(sign * r2, a)

                x1, y1 = self._add_tuples(c1, self.pos)
                x2, y2 = self._add_tuples(c2, self.pos)

                ticks.append(Line(x1, y1, x2, y2, thickness))

        return ticks

    def get_clock_hands(self) -> list[Line]:
        dt = datetime.now()
        
        hand_types = ['second', 'minute', 'hour']
        return [self._get_hand(dt, ht) for ht in hand_types]

    def _get_hand(self, time, hand_type) -> Line:
        t = getattr(time, hand_type)
        a = None

        if hand_type in ['second', 'minute']:
            a = pi * t / (30) - pi / 2
        else:
            a = pi * (t % 12) / (6) - pi / 2

        r = self.radius * self._hand_length_scales[hand_type]

        c = self._polar_to_cartesian(r, a)
        x1, y1 = self.pos
        x2, y2 = self._add_tuples(c, self.pos)

        return Line(x1, y1, x2, y2, self._hand_thicknesses[hand_type])


    def _polar_to_cartesian(self, r, a):
        return (r * cos(a), r * sin(a))

    def _add_tuples(self, t1, t2):
        return [x + y for x, y in zip(t1, t2)]