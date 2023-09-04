"""
Python File für die Game Scene
"""
from pubsub import pub
import pygame as pg

from . import Scene, Text, ColorBar, BoardView, TextButton
from ... import BUTTON_HOVER_COLOR, DARK_GREEN_BUTTON, GREEN_BUTTON
# constants:
from . import InGameGuiControl

class BreakerGameScene(Scene):
    """
    Klasse für die Scene in der die Spielpartie aus sicht des Raters dargestellt wird.
    """
    __slots__ = Scene.slots + ("background", "ingame_gui_controller", "title",
                               "board", "color_bar", "__selected_color",
                               "send_button", "surrender_button")

    def __init__(self, gui_controller, board_reihen: int, code_length: int, color_amount: int):
        """
        :param gui_controller: Bekommt den gui_controller übergeben, um dessen Funktionen über die
        Buttons zu benutzen
        :param board_reihen: Wie viele Reihen soll das Bord haben? (Anzahl Züge)
        :param board_spalte: Wie viele Spalten soll das Bord haben? (Kodelänge)
        :param color_amount: Wie viele verschiedene Farben soll es geben?   
        """
        super().__init__(gui_controller)

        self.board = BoardView(board_reihen, code_length, color_amount, self.wnd.tile_size)
        self.color_bar = ColorBar(color_amount, tile_size=self.wnd.tile_size)
        self.ingame_gui_controller = InGameGuiControl(self)

        self.send_button = TextButton(lambda: self.ingame_gui_controller.send_guessing_attempt(),
                                      "senden",
                                      0.01, 0.55, 40, button_hover_color=DARK_GREEN_BUTTON,
                                      button_color=GREEN_BUTTON
                                      )
        
        self.surrender_button = TextButton(lambda: self.ingame_gui_controller.surrender(),
                                      "aufgeben",
                                      0.01, 0.7, 40)
        
        self.buttons = [self.send_button, self.surrender_button]

    def handle_events(self, events):
        """
        Routine in der das Hauptmenü Events bearbeitet
        """
        events = self.ingame_gui_controller.handle_button_events(events, self.buttons)
        events = self.ingame_gui_controller.handle_events(events)
        return events


    def update(self, delta):
        """
        Damit updated sich der Screen
        TODO: Wird eventuell noch verworfen
        """

    def draw(self):
        """
        Mit dieser Methode wird die Scene geblitted (auf dem Pygame Canvas erzeugt)
        """
        self.wnd.clear()

        self.wnd.blit(self.wnd.background)
        for i in self.buttons:
            self.wnd.blit_ui(i)

        #self.wnd.rescale_bg(self.background)

        board_x_offset, board_y_offset = self.wnd.board_offset
        boardsurf = self.wnd.subsurface(
            (board_x_offset, board_y_offset, self.board.width, self.board.height))
        self.board.draw(boardsurf)

        colorbar_x_offset, colorbar_y_offset = self.wnd.colorbar_offset
        colorbarsurf = self.wnd.subsurface(
            (colorbar_x_offset, colorbar_y_offset, self.color_bar.width, self.color_bar.height))
        self.color_bar.draw(colorbarsurf)

        for i in self.sprites:
            i.draw(self.wnd)