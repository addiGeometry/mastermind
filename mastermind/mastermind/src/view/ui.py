"""
Klasse in der simple UI-Komponenten definiert werden
"""
import pygame as pg

from . import GVTIME_FONT_PATH

class Text():
    """
    Klasse für Text, der auf der Oberfläche angezeigt wird
    :param body: Der Text str
    :param x_offset: x_offset float, der Multiplikator für die relative Screen-Position
    :param y_offset: y_offset float, der Multiplikator für die relative Screen-Position
    :param size: Die Textgröße int
    :optional param align: pg.Alignment, standarmäßig "topleft"
    :optinal param color: Die Farbe pg.Color
    """
    __slots__ = ("_body","_color","x_cord","x_offset", "y_offset", "y_cord","width","height","size", "_align", "font", "renders")

    def __init__(self, body, x_offset, y_offset, size, align="topleft", color=(255, 255, 255)):
        self._body = body.splitlines()
        self._color = pg.color.Color(color)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_cord = 0
        self.y_cord = 0
        self.width = 0
        self.height = 0
        self.size = size
        self._align = align

        self.font = pg.font.Font(GVTIME_FONT_PATH, size)
        self.renders = []
        self.render()

    @property
    def align(self) -> None:
        """
        Gebe den PG-Alignment Typen zurück
        """
        return self._align

    @property
    def position(self) -> tuple[int, int]:
        """
        Position on the screen
        """
        return(self.x_cord, self.y_cord)

    @position.setter
    def position(self, pos: tuple[int, int]) -> None:
        """
        Setze die Position
        :param pos: Die neue Position
        """
        self.x_cord, self.y_cord = pos

    @property
    def offset(self) -> tuple[float, float]:
        """
        Offset on the screen
        """
        return(self.x_offset, self.y_offset)

    @offset.setter
    def offset(self, offset: tuple[float, float]) -> None:
        """
        Setze das Offset
        """
        self.x_offset, self.y_offset = offset

    @property
    def body(self) -> str:
        """
        Body (Text)
        """
        return "\n".join(self._body)

    @body.setter
    def body(self, value):
        """
        Setze den Text
        """
        self._body = value.split("\n")
        self.render()

    @property
    def color(self) -> pg.color.Color:
        """
        Text color
        """
        return self._color

    @color.setter
    def color(self, value) -> None:
        """
        Setze die Farbe
        :param value: Wert
        """
        if isinstance(value, pg.color.Color):
            self._color = value
        else:
            self._color = pg.color.Color(value)

    def render(self) -> None:
        """
        Rendere den Text auf der Pygame-Oberfläche
        """
        self.renders.clear()
        self.width = 0
        self.height = 0

        surface = self.font.render(self.body, True, self._color).convert_alpha()
        self.width = surface.get_width()
        self.height = surface.get_height()

        rect = surface.get_rect()
        setattr(rect, self.align, (self.x_cord, self.y_cord))
        self.renders.append((surface, rect))


def remove_event(events: list[pg.event.Event], event: pg.event.Event) -> list[pg.event.Event]:
    """
    Entferne ein event aus den PG-Events.
    Methode ist das, um Bugs in der Event-Verarbeitung zu Fixen.
    """
    if event in events:
        events.remove(event)
    return events
