from dataclasses import dataclass, field


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    thickness: int

    coords: tuple = field(init=False)

    def __post_init__(self):
        self.coords = ((self.x1, self.y1), (self.x2, self.y2))

    def get_coords(self):
        return self.coords
