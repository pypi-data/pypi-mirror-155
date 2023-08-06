from typing import Callable

from .core import Core
from .graphics import Graphics


class Enpyre(Core, Graphics):
    KEY_UP = "ArrowUp"
    KEY_LEFT = "ArrowLeft"
    KEY_DOWN = "ArrowDown"
    KEY_RIGHT = "ArrowRight"

    def __init__(self):
        self.time = 0.0
        self.frame = 0
        Core.__init__(self)
        Graphics.__init__(self)

    def run(
        self,
        height: int,
        width: int,
        color: str,
        update: Callable[[float], None],
    ):
        self.time = 0.0
        self.frame = 0
        self.draw_canvas(height, width, color, self.get_update(update))
