from structs import Line
from math import cos, sin, pi, prod
from datetime import datetime


class Clock:
    hand_types = ["hour", "minute", "second"]
    # max values on the clock: [hour, minute, seconds]
    ht_max_values = [12, 60, 60]

    hand_thicknesses = {"second": 2, "minute": 5, "hour": 10}

    # scales self.radius
    hand_length_scales = {"second": 0.85, "minute": 0.85, "hour": 0.4}

    # a list of time values: [second, minute, hour]
    _current_times = [0, 0, 0]

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def get_ticks(self) -> list[Line]:
        """
        Constructs the ticks for the clock
        """

        n_ticks = 60
        ticks = []

        # will render the ticks all around the clock
        for sign in [-1, 1]:
            for i in range(n_ticks):
                thickness = 10 if i % 5 == 0 else 1

                # angle
                a = pi * i / (n_ticks / 2)

                # start and end point
                r1 = self.radius * 0.9
                r2 = self.radius * 0.95

                # gets the cartesian vectors
                c1 = self._polar_to_cartesian(sign * r1, a)
                c2 = self._polar_to_cartesian(sign * r2, a)

                # centers around clock center
                x1, y1 = self._add_tuples(c1, self.pos)
                x2, y2 = self._add_tuples(c2, self.pos)

                ticks.append(Line(x1, y1, x2, y2, thickness))

        return ticks

    def get_clock_hands(self) -> list[Line]:
        """
        Constructs all the clock's hands for the current time
        """

        # updates the current time
        dt = datetime.now()
        self._current_times = [
            getattr(dt, ht) if i != 0 else getattr(dt, ht) % 12
            for i, ht in enumerate(self.hand_types)
        ]

        return [self._get_hand(i) for i in range(len(self.hand_types))]

    def _get_hand(self, ht_idx: int) -> Line:
        """
        Constructs a single hand for the current time, taken from the state.
        The minute & hour hands will move continuously, while the seconds hand will move discretely
        """

        hand_type = self.hand_types[ht_idx]
        # will contain how much the second/minute hands have traveled
        scaled_fractions = []

        for i, time in enumerate(self._current_times):
            # ensures only seconds are considered for the minute hand
            # and both minutes & seconds are considered for the hour hand
            if i < ht_idx:
                continue

            # gets & scales the fractions properly
            frac = time / prod(self.ht_max_values[3 - len(scaled_fractions) :])
            scaled_fractions.append(frac)

        # gets the distance to the next tick
        frac_summed = 2 * sum(scaled_fractions) / self.ht_max_values[ht_idx]

        # calculates the hand coordinates, similar to the ticks construction
        a = pi * frac_summed - pi / 2
        r = self.radius * self.hand_length_scales[hand_type]
        c = self._polar_to_cartesian(r, a)
        x1, y1 = self.pos
        x2, y2 = self._add_tuples(c, self.pos)

        return Line(x1, y1, x2, y2, self.hand_thicknesses[hand_type])

    def _polar_to_cartesian(self, r: float, a: float) -> tuple:
        """
        Converts polar vectors to cartesian coordinates
        """

        return (r * cos(a), r * sin(a))

    def _add_tuples(self, t1: tuple, t2: tuple) -> tuple:
        """
        Sums two tuples together element-wise
        """

        return [x + y for x, y in zip(t1, t2)]
