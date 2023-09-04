import pygame as pg
from . import Scene, Sprite, Text, TextButton
from . import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BACKGROUND_PATH
from mastermind import Role


class ChooseRoleScene(Scene):
    __slots__ = Scene.slots + ("background", "title", "coder_button", "breaker_button", "buttons")

    def __init__(self, gui_controller):
        super().__init__(gui_controller)

        self.title = Text("Wähle deine Rolle: ", 1/2, 0.25, 100, align="center")

        self.coder_button = TextButton(
            #PARAM1 func
            lambda: self.gui_controller.set_role(Role.MAKER),
            "Kodierer", 
            # x
            1/4,
            # y
            0.6,
            50,
            align="center"
        )
        self.breaker_button = TextButton(
            lambda: self.gui_controller.set_role(Role.BREAKER),
            "Rater", 
            # x-offset
            3/4,
            # y-offset
            0.6,
            50,
            align="center"
        )
        self.buttons = (self.coder_button, self.breaker_button)

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