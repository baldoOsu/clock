from dataclasses import dataclass, field

@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int
    thickness: int

    coords: tuple = field(init=False)

    def __post_init__(self):
        self.coords = ((self.x1, self.y1), (self.x2, self.y2))