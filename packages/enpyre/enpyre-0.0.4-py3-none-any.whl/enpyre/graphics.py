from typing import Callable

from . import js_interface


class Graphics:
    @staticmethod
    def draw_canvas(
        height: int, width: int, color: str, callback: Callable[[float], None]
    ):
        js_interface.drawCanvas(height, width, color, callback)

    @staticmethod
    def draw_circle(x: int, y: int, r: int, color: str):
        return js_interface.create_proxy(
            js_interface.drawCircle(x, y, r, color)
        )
