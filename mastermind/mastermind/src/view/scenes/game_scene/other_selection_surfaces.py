"""
Weiter GUI-Elemente in der GameScene
"""

import pygame as pg
from . import (COLORS, BLACK, DARKBROWN, LIGHTBROWN)

__all__ = ("Pin", "ColorBar", "CluePin")

class Pin:
    """
    Klasse für die Grafische Darstellung von "Pins". Pins sind die Spielsteine
    in Mastermind, mit denen die Kodes gelegt werden.
    """
    def __init__(self, x_coord: int, y_coord: int, color: pg.Color=None, revealed: bool=True,
                 tile_size=50*1.15, x_shift: int=0):
        self.x_coord, self.y_coord = x_coord, y_coord
        self.color = color
        self.revealed = revealed
        self._tile_size = tile_size
        self.x_shift = x_shift

    @property
    def tile_size(self):
        """
        Die Größe eines Tiles auf dem Feld
        """
        return self._tile_size

    def draw(self, surface):
        center = (self.x_coord + (self.tile_size/2), self.y_coord + (self.tile_size/2))
        pin_size = self.tile_size // 3
        if self.color is not None and self.revealed:
            pg.draw.circle(surface,
                           tuple(x * 0.3 for x in self.color),
                           tuple(x + 5 for x in center)
                           ,pin_size)
            pg.draw.circle(surface,
                           tuple(pg.Color(0,0,0,255)),
                           tuple(x + 2 for x in center)
                           ,pin_size)
            pg.draw.circle(surface,
                           self.color,
                           center,
                           pin_size)
            pg.draw.circle(surface,
                           tuple(x + 50 if i < 3 and (x+30) < 255 else x for i, x in enumerate(self.color)),
                           tuple(x - 8 for x in center)
                           ,pin_size//4)
        elif not self.revealed:
            pg.draw.circle(surface, LIGHTBROWN, center, self.tile_size//4)
            pg.draw.circle(surface, BLACK, center, self.tile_size//4, 3)
        
        else:
            pg.draw.circle(surface, BLACK, center, self.tile_size//6 + 2)
            pg.draw.circle(surface, DARKBROWN, center, self.tile_size//6)
            

class CluePin(Pin):
    """
    Pins für die Feedback-Clues
    """
    def draw(self, surface):
        center = (self.x_coord + (self.tile_size/2.5)
                  + self.x_shift, self.y_coord + (self.tile_size/2.5))
        if self.color is not None:
            pg.draw.circle(surface, self.color, center, self.tile_size/10)
        else:
            pg.draw.circle(surface, BLACK, center, self.tile_size/10 + 1)
            pg.draw.circle(surface, DARKBROWN, center, self.tile_size/10)

class ColorBar:
    """
    Klasse für die Anzeige, in der man Seine Farben für die Kodierung
    oder den Rateversuch auswählen kann.
    """
    def __init__(self, color_amount: int, tile_size=50*1.15, offset=None):
        self.offset = offset
        self.colors = COLORS[0:color_amount]
        self.color_amount = color_amount
        self._tile_size = tile_size
        self._width = color_amount * self.tile_size
        self._height = self.tile_size
        self.color_selection_surface = pg.Surface((self.width, self.tile_size)).convert_alpha()

        self._color_selection = []
        self.create_selection_pins()

    @property
    def tile_size(self):
        """
        Die Größe eines Tiles auf dem Feld
        """
        return self._tile_size

    def create_selection_pins(self):
        for i, x in enumerate(self.colors):
            self.color_selection.append(Pin(
                i*self.tile_size,
                0,
                pg.Color(x),
                tile_size=self.tile_size
            ))

    def draw(self, surface):
        """
        Zeichne die Colorbar
        """
        self.color_selection_surface.fill((0, 0, 0, 0))

        for pin in self.color_selection:
            pin.draw(self.color_selection_surface)

        surface.blit(self.color_selection_surface, (0, 0))

    @property
    def color_selection(self):
        return self._color_selection

    @color_selection.setter
    def color_selection(self, value):
        if isinstance(value, list):
            self._color_selection = value
        else:
            raise ValueError("color_selection must be a list")

    @property
    def width(self):
        """
        Breite der ColorBar
        """
        return self._width
    
    @property
    def height(self):
        """
        Höhe der ColorBar
        """
        return self._height