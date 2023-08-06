from typing import Callable
from typing import Optional


def drawCanvas(
    height: int, width: int, color: str, callback: Callable[[float], None]
):
    import js

    js.drawCanvas(height, width, color, callback)


def drawCircle(x: int, y: int, r: int, color: str):
    import js

    return js.drawCircle(x, y, r, color)


def keyPressed(key: str) -> bool:
    import js

    try:
        attr = getattr(js, key)
        return bool(attr)
    except AttributeError:
        return False


def create_proxy(obj):
    from pyodide import create_proxy

    return create_proxy(obj)


def addSong(alias: str, url: str, playOnLoad: bool = False):
    import js

    js.addSong(alias, url, playOnLoad)


def playSong(alias: str):
    import js

    js.playSong(alias)


def stopSong(alias: Optional[str] = None):
    import js

    js.stopSong(alias)
