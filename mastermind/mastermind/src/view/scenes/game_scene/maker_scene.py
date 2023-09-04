"""
Python File für die Maker Scene
"""
import pygame as pg
from ...ui import remove_event
from . import Scene, Text, ColorBar, BoardView, TextButton
from ... import BUTTON_HOVER_COLOR, TRANSPARENT, GREEN_BUTTON, DARK_GREEN_BUTTON
# constants:
from . import InGameGuiControl

__all__ = ["MakerMakeScene", "MakerGameScene"]

class MakerMakeScene(Scene):
    """
    Klasse für die Scene in der der Maker den Code erstellt
    """
    __slots__ = Scene.slots + ("background", "ingame_gui_controller", "title",
                               "board", "color_bar", "__selected_color",
                               "send_button", "surrender_button", "boards")

    def __init__(self, gui_controller, board_spalten: int, color_amount: int):
        """
        :param gui_controller: Bekommt den gui_controller übergeben, um dessen Funktionen über die
        Buttons zu benutzen
        :param board_spalte: Wie viele Spalten soll das Bord haben? (Kodelänge)
        :param color_amount: Wie viele verschiedene Farben soll es geben?   
        """
        super().__init__(gui_controller)
        self.title = Text("Wähle den Kode für das Spiel", 1/2, 0.32, 80, align="center")
        self.board = BoardView(0, board_spalten, color_amount, self.wnd.tile_size, feedback=False, offset="mmb_offset")
        self.color_bar = ColorBar(color_amount, tile_size=self.wnd.tile_size, offset="mmm_cbar")
        self.ingame_gui_controller = InGameGuiControl(self)

        self.send_button = TextButton(lambda: self.ingame_gui_controller.create_code(),
                                      "Code Erstellen",
                                      1/5, 0.8, 40, button_hover_color=DARK_GREEN_BUTTON,
                                      button_color=GREEN_BUTTON, scale=3.6
                                      )
        
        self.surrender_button = TextButton(lambda: self.ingame_gui_controller.surrender(),
                                      "Aufgeben",
                                      3/5, 0.8, 40)
        
        self.clear_button = TextButton(lambda: self.board.clear_board(),
                                       "Clear",
                                       3.1/5, 0.495, 30, scale=1.8,
                                       border_color=TRANSPARENT)
        
        self.buttons = [self.send_button, self.surrender_button, self.clear_button]
        self.boards = [self.board]

    def handle_events(self, events):
        """
        Routine in der das Hauptmenü Events bearbeitet
        """
        #events = self.gui_controller.handle_button_events(events, self.buttons)
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
        for i in (self.title, *self.buttons):
            self.wnd.blit_ui(i)

        #self.wnd.rescale_bg(self.background)

        board_x_offset, board_y_offset = self.wnd.maker_make_bar_offset(self.board.spalten)
        boardsurf = self.wnd.subsurface(
            (board_x_offset, board_y_offset, self.board.width, self.board.height))
        self.board.draw(boardsurf)

        colorbar_x_offset, colorbar_y_offset = self.wnd.makermake_colorbar_offset(self.color_bar.color_amount)
        colorbarsurf = self.wnd.subsurface(
            (colorbar_x_offset, colorbar_y_offset, self.color_bar.width, self.color_bar.height))
        self.color_bar.draw(colorbarsurf)

class MakerGameScene(Scene):
    """
    Klasse für die Scene in der die Spielpartie dargestellt wird.
    """
    __slots__ = Scene.slots + ("background", "ingame_gui_controller", "title",
                            "board", "color_bar", "__selected_color",
                            "send_button", "surrender_button", "draw_buttons",
                            "next_button", "clear_button")

    def __init__(self, gui_controller, board_reihen: int, board_spalten: int, color_amount: int):
        """
        :param gui_controller: Bekommt den gui_controller übergeben, um dessen Funktionen über die
        Buttons zu benutzen
        :param board_reihen: Wie viele Reihen soll das Bord haben? (Anzahl Züge)
        :param board_spalte: Wie viele Spalten soll das Bord haben? (Kodelänge)
        :param color_amount: Wie viele verschiedene Farben soll es geben?   
        """
        super().__init__(gui_controller)
        self.title = Text("Mastermind", 1/2, 0.32, 100, align="center")
        self.fremd_board = BoardView(board_reihen, board_spalten, color_amount, self.wnd.tile_size, offset="mg_main")
        self.board = BoardView(0, board_spalten, color_amount, self.wnd.tile_size, feedback=False, offset="mg_rs")
        print(self.board.versuche)
        self.color_bar = ColorBar(2, tile_size=self.wnd.tile_size, offset="mmg_rate")
        self.ingame_gui_controller = InGameGuiControl(self)

        self.send_button = TextButton(lambda: self.ingame_gui_controller.send_rating_attempt(),
                                      "Feedback geben",
                                      1/30, 0.8, 40, button_hover_color=DARK_GREEN_BUTTON,
                                      button_color=GREEN_BUTTON, scale=3.6
                                      )
        
        self.surrender_button = TextButton(lambda: self.ingame_gui_controller.surrender(),
                                      "Aufgeben",
                                      1/3, 0.8, 40)
        
        self.clear_button = TextButton(lambda: self.board.clear_board(),
                                       "Clear",
                                       1/30, 1/70, 30, scale=1.8,
                                       border_color=TRANSPARENT)
        self.next_button = TextButton(lambda: self.ingame_gui_controller.next_guess(),
                                       "Next guess",
                                       1/30, 1/8, 30, scale=2.2,
                                       border_color=TRANSPARENT,
                                       button_color=GREEN_BUTTON, button_hover_color=DARK_GREEN_BUTTON)
        
        self.buttons = [self.send_button, self.surrender_button, self.clear_button, self.next_button]
        self.draw_buttons = self.buttons.copy()

    def handle_events(self, events):
        """
        Routine in der das Hauptmenü Events bearbeitet
        """
        if self.sprites:
            for event in events:
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons:
                        if button.is_under_mouse(event.pos):
                            button.on_hover()
                            #Jedes mal nachdem ein Event verabreitet wurde, wird es aus der Liste entfernt.
                            #Wenn wieder in den gui_controller gewechselt wird, wird dadurch die Liste an zu prüfenden
                            #Events verringert.
                            #remove_event(events, event)
                        elif button.hovering:
                            button.on_unhover()
                            remove_event(events, event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_under_mouse(event.pos):
                            button.on_click()
                            remove_event(events, event)
        events = self.ingame_gui_controller.handle_events(events)
        #TODO REMOVE REDUNDANCY
        
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
        for i in (self.title, *self.draw_buttons):
            self.wnd.blit_ui(i)

        board_x_offset, board_y_offset = self.wnd.board_offset
        boardsurf = self.wnd.subsurface(
            (board_x_offset, board_y_offset, self.fremd_board.width, self.fremd_board.height))
        self.fremd_board.draw(boardsurf)

        rating_x_offset, rating_y_offset = self.wnd.maker_game_rate_slot_offset()
        rating_boardsurf = self.wnd.subsurface(
            (rating_x_offset, rating_y_offset, self.board.width, self.board.height))
        self.board.draw(rating_boardsurf)

        colorbar_x_offset, colorbar_y_offset = self.wnd.maker_game_colorbar_offset()
        colorbarsurf = self.wnd.subsurface(
            (colorbar_x_offset, colorbar_y_offset, self.color_bar.width, self.color_bar.height))
        self.color_bar.draw(colorbarsurf)

        for i in self.sprites:
            i.draw(self.wnd)
    
