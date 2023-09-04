"""
Vorlage für Buttons auf der Pygame Oberfläche
"""

import pygame as pg
from .window import Window
from . import (Text, BUTTON_HOVER_COLOR, BUTTON_COLOR, STANDARD_BORDER,
               STANDARD_TEXT, MAX_USERNAME)

class TextButton():
    """
    Klasse für Text-Buttons, die auf der Oberfläche angezeigt werden
    :param action: Funktion des Buttons func
    :param body: Der Text str
    :param x_offset: x_offset float, der Multiplikator für die relative Screen-Position
    :param y_offset: y_offset float, der Multiplikator für die relative Screen-Position
    :param size: Die Textgröße int
    :optional param align: pg.Alignment, standarmäßig "topleft"
    :optional param scale: die größe des Buttons kann hiermit skalliert werden.
    Standardmäßig 2.4
    :optinal param text_color: Die Farbe des Texts pg.color.Color
    :optinal param border_color: Die Farbe des Randes pg.color.Color
    :optinal param button_color: Die Farbe des Buttons pg.color.Color
    :optinal param button_hover_color: Die Farbe des Buttons on Hover pg.color.Color
    """
    __slots__ = ("_current_button_color","_current_border_color","_button_border_color",
                 "_button_color", "_button_hover_color", "_border_hover_color",
                 "_input_text_color", "text", "action", "hovering",
                 "renders", "_clicked" ,"scale", "_width", "_height", "_surface",
                 "parent_offset", "type")

    def __init__(self, action, body, x_offset, y_offset, size, align="topleft",
                 text_color=STANDARD_TEXT, input_text_color=STANDARD_TEXT, border_color=STANDARD_BORDER, 
                 button_color=BUTTON_COLOR, button_hover_color=BUTTON_HOVER_COLOR,
                 border_hover_color=STANDARD_BORDER, scale=2.4, parent_offset: tuple[int, int]=(0,0)):
        
        self.text = Text(body, x_offset, y_offset, size, align, text_color)
        #self.text.render = lambda a: 0
        self.action = action
        self.hovering = False
        self._clicked = False
        self.scale = scale
        self._button_color = button_color
        self._current_button_color = button_color
        self._button_hover_color = button_hover_color
        self._button_border_color = border_color
        self._current_border_color = border_color
        self._border_hover_color = border_hover_color
        self._input_text_color = input_text_color
        self._width = self.text.size*2 + Window.get_sc_unit() * self.scale
        self._height = Window.get_sc_unit()
        self.renders = []
        self.type = body
        self._surface = None
        self.parent_offset = parent_offset
        self.render()

    @property
    def clicked(self) -> bool:
        """
        Property, ob der Button geclicked wurde
        :return: True, wenn ja, sonst nein
        """
        return self._clicked

    def click(self) -> None:
        """
        Clicke den button
        """
        self._clicked = not self.clicked

    @property
    def align(self) -> str:
        """
        Gebe den PG-Alignment Typen zurück
        """
        return self.text.align

    @property
    def offset(self) -> tuple[int, int]:
        """
        Offset on the screen
        """
        return(self.text.x_offset, self.text.y_offset)

    @offset.setter
    def offset(self, offset: tuple[int, int]):
        """
        Setze das Offset
        """
        self.text.x_offset, self.text.y_offset = offset

    @property
    def button_color(self):
        """
        Getter für die Knopffarbe
        """
        return self._button_color
   
    @button_color.setter
    def button_color(self, value):
        """
        Setter für die Knopffarbe
        :param pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._button_color = value
        else:
            self._button_color = pg.color.Color(value)


    @property
    def current_button_color(self):
        """
        Getter für die Knopffarbe
        """
        return self._current_button_color
   
    @current_button_color.setter
    def current_button_color(self, value):
        """
        Setter für die Knopffarbe
        :param pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._current_button_color = value
        else:
            self._current_button_color = pg.color.Color(value)

    @property
    def current_border_color(self):
        """
        Getter für die Knopffarbe
        """
        return self._current_border_color
   
    @current_border_color.setter
    def current_border_color(self, value):
        """
        Setter für die Knopffarbe
        :param pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._current_border_color = value
        else:
            self._current_border_color = pg.color.Color(value)

    @property
    def button_hover_color(self):
        """
        Getter für die Knopffarbe on Hover
        """
        return self._button_hover_color
   
    @button_hover_color.setter
    def button_hover_color(self, value):
        """
        Setter für die Knopffarbe on Hover
        :param value: pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._button_hover_color = value
        else:
            self._button_hover_color = pg.color.Color(value)

    @property
    def border_hover_color(self):
        """
        Getter für die Knopffarbe on Hover
        """
        return self._border_hover_color
   
    @border_hover_color.setter
    def border_hover_color(self, value):
        """
        Setter für die Knopffarbe on Hover
        :param pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._border_hover_color = value
        else:
            self._border_hover_color = pg.color.Color(value)

    @property
    def button_border_color(self):
        """
        Getter für die Knopfrandfarbe
        """
        return self._button_border_color
   
    @button_border_color.setter
    def button_border_color(self, value):
        """
        Setter für die Knopfrandfarbe
        :param pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._button_border_color = value
        else:
            self._button_border_color = pg.color.Color(value)

    @property
    def surface(self):
        """
        Gibt die aktuelle Oberfläche zurück.
        """
        return self._surface

    @surface.setter
    def surface(self, value):
        """
        Setzt die Oberfläche auf den angegebenen Wert.
        
        :param value: Die neue Oberfläche.
        """
        self._surface = value

    def is_under_mouse(self, pos):
        """
        Gibt true zurück, wenn die Maus über dem Button hovered. 
        Benutzt dafür Pygames Funktion "collidepoint" für surfaces.

        :param pos aktuelle Mausposition
        :return wahr, wenn collision, sonst falsch
        """
        return self.renders[0][1].collidepoint(pos)

    def on_hover(self, *args, **kwargs):
        """
        Ist verantwortlich für das Neu-Rendering, wenn die Maus auf dem Button hovered
        """
        setattr(self, "current_button_color", self.button_hover_color)
        setattr(self, "current_border_color", self.border_hover_color)
        self.hovering = True
        self.render()

    def on_unhover(self, *args, **kwargs):
        """
        Wird aufgerufen, wenn die Maus nicht mehr hovered und aktualisiert wieder die Anzeige
        """
        setattr(self, "current_button_color", self.button_color)
        setattr(self, "current_border_color", self.button_border_color)
        #self.body = self.body[1:]
        self.hovering = False
        self.render()

    def on_click(self, *args, **kwargs):
        """
        Wird aufgerufen, wenn der Button geklickt wird. Ruft die vordefinierte Aktion 
        des Buttons auf.
        param: *args die unbenannten Paramater für die Funktion des Buttons
        param: **kwargs die benannten Paramater für die Funktion des Buttons
        """
        self.action(*args, **kwargs)

    @property
    def input_text_color(self):
        """
        Getter für die ALT-Text-Color
        """
        return self._input_text_color
   
    @input_text_color.setter
    def input_text_color(self, value):
        """
        Setter für die ALT-Text-Color
        :param value: pg.Color
        """
        if isinstance(value, pg.color.Color):
            self._input_text_color = value
        else:
            self._input_text_color = pg.color.Color(value)

    @property
    def height(self):
        """
        Getter für die height des Buttons
        """
        return self._height

    def render(self):
        """
        Wichtige Methode, die für die Erzeugung des Buttons auf der Pygame Oberfläche zuständig ist.
        """
        self.renders.clear()

        # Create a surface for the button
        self._width = self.text.size*2 + Window.get_sc_unit() * self.scale
        self._height = Window.get_sc_unit()

        button_surface = pg.Surface((self._width, self._height), pg.SRCALPHA).convert_alpha()
        button_surface_rect = button_surface.get_rect()
        self.surface = button_surface

        # Draw the button background
        bt_color = self.current_button_color  # Choose your button background color
        pg.draw.rect(button_surface, bt_color, button_surface_rect)

        # Draw the border on the button surface
        border_color = self.current_border_color  # Choose your border color
        border_width = 4  # Choose your border width
        pg.draw.rect(button_surface, border_color, button_surface_rect, border_width)

        # Blit the text surface onto the button surface
        text_surface, text_rect = self.text.renders[0]
        text_rect.center = button_surface_rect.center
        button_surface.blit(text_surface, text_rect)

        # Calculate the final button rect
        button_rect = button_surface_rect.copy()
        button_rect.center = (self.text.x_cord, self.text.y_cord)

        if self.parent_offset != (0,0):
            button_rect.center = (self.text.x_cord + self.parent_offset[0], self.text.y_cord + self.parent_offset[1])

        # Store the rendered surface and rect
        self.renders.append((button_surface, button_rect))
