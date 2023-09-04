"""
Python File für die ChooseIfOnlie Scene
"""

import pygame as pg
from . import Scene, Text, TextButton

class ChooseOnlineModeScene(Scene):
    """
    Scene, in der der Nutzer auswählt, ob er online gegen einen Kodierer oder
    offline als Rater oder Kodierer spielen will.
    """
    __slots__ = Scene.slots + ("background", "title", "mehrspieler_button", "einzelspieler_button", "buttons")

    def __init__(self, gui_controller):
        super().__init__(gui_controller)
  
        self.title = Text("Wähle deinen Spielmodus:", 1/2, 0.25, 100, align="center")

        self.mehrspieler_button = TextButton(
            #PARAM1 func
            lambda: self.gui_controller.set_is_online(True),
            "Mehrspieler", 
            # x-offset
            1/3,
            # y-offset
            0.60,
            50,
            scale=3,
            align="center"
        )
        self.einzelspieler_button = TextButton(
            lambda: self.gui_controller.set_is_online(False),
            "Einzelspieler",
            # x
            2/3,
            # y
            0.60,
            50,
            scale=3,
            align="center"
        )
        self.buttons = (self.mehrspieler_button, self.einzelspieler_button)

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
        for i in self.sprites:
            print(i)
            self.wnd.blit(i)