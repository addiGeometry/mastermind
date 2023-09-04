import pygame as pg

from mastermind import GameMode
from . import Scene, Text, TextButton


class ChooseGameModeScene(Scene):
    __slots__ = Scene.slots + ("background", "title", "super_button", "original_button", "buttons")

    def __init__(self, gui_controller):
        super().__init__(gui_controller)

        self.title = Text("Waehle deine Variante:", 1/2, 0.25, 100, align="center")

        self.super_button = TextButton(
            #PARAM1 func
            lambda: self.gui_controller.set_gamemode(GameMode.SUPER_MASTERMIND),
            "Super Superhirn", 
            # x
            1/4,
            # y
            0.6,
            50,
            scale=3.7,
            align="center"
        )
        self.original_button = TextButton(
            lambda: self.gui_controller.set_gamemode(GameMode.MASTERMIND),
            "Original",
            # x
            3/4,
            # y
            0.6,
            50,
            scale=3.7,
            align="center"
        )
        self.buttons = (self.super_button, self.original_button)

    def handle_events(self, events):
        """
        TEMPLATE PATTERN
        Routine in der das Hauptmenü Events bearbeitet
        HINWEIS: Aufgabe des controllers, aber bestimmte
        Scenes benötigen extra events.
        """

        return events

    def update(self, delta):
        pass

    def draw(self):
        self.wnd.blit(self.wnd.background)
        for i in (self.title, *self.buttons):
           self.wnd.blit_ui(i)
