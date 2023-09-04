"""
Klasse für Input-Fields. In dieser Architektur ein Button, der
dekoriert wurde,
"""
import pygame as pg
from . import TextButton
from . import (Text, BUTTON_HOVER_COLOR, BUTTON_COLOR, STANDARD_BORDER,
               STANDARD_TEXT, MAX_USERNAME)
from . import Window

class InputField(TextButton):
    """
    Input-Felder sind zur Aufnahme von User-Input in Form von Text geignet.
    """
    __slots__ = TextButton.__slots__ + ("filled", "tbd")

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
        self.filled = False
        self.type = body
        self._surface = None
        self.parent_offset = parent_offset
        self.render()

    def input_field_on_click(self):
        """
        Diese Methode wird nur für Text-Input-Fields verwendet,
        um gänges verhalten zu ermöglichen.
        Verhalten bei der Auswahl des Input-Fields
        """
        self.current_border_color = self.border_hover_color
        if not self.filled:
            self.text.body = ""
        self.text.color = self.input_text_color
        self.render()
        # self.click()

    def input_field_on_delesect(self):
        """
        Diese Methode wird nur für Text-Input-Fields verwendet,
        um gänges verhalten zu ermöglichen.
        Verhalten des Input-Fields, wenn der user irgendwo anders
        hin klickt.
        """
        self.current_border_color = self.button_border_color
        if not self.text.body:
            self.text.body = self.type
        self.text.color = self.input_text_color

    def handle_key_input(self, event: pg.event.Event, max=MAX_USERNAME) -> None:
        """
        Just for the Input Field
        :return: Alle Events, außer, dass verarbeitete
        """
        if self.clicked:
            if event.key == pg.K_BACKSPACE and len(self.text.body) > 0:
                self.text.body = self.text.body[:-1]
                if len(self.text.body):
                    self.filled =  False
                self.render()
            else:
                if len(self.text.body) < max:
                    self.filled = True
                    self.text.body += event.unicode
                    self.render()

    def on_hover(self, *args, **kwargs):
        """
        Ist verantwortlich für das Neu-Rendering, wenn die Maus auf dem Button hovered
        """
        if not self.clicked:
            setattr(self, "current_button_color", self.button_hover_color)
            setattr(self, "current_border_color", self.border_hover_color)
            self.hovering = True
            self.render()

    def on_unhover(self, *args, **kwargs):
        """
        Wird aufgerufen, wenn die Maus nicht mehr hovered und aktualisiert wieder die Anzeige
        """
        if not self.clicked:
            setattr(self, "current_button_color", self.button_color)
            setattr(self, "current_border_color", self.button_border_color)
            #self.body = self.body[1:]
            self.hovering = False
            self.render()
