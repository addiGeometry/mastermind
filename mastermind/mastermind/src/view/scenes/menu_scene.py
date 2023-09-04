"""
Python File für die Menu Scene
"""

import pygame as pg

from . import Scene, Text, TextButton
# constants:


class MenuScene(Scene):
    """
    Hauptmenü Scene in der das Programm auch startet.
    """
    __slots__ = Scene.slots + ("title", "play_button", "quit_button", "buttons")

    def __init__(self, gui_controller):
        """
        Bekommt den gui_controller übergeben, um dessen Funktion über die
        Buttons zu benutzen  
        """
        super().__init__(gui_controller)

        self.title = Text("Mastermind", 1/2, 0.22, 100, align="center")
        self.play_button = TextButton(
            #PARAM1 func
            self.gui_controller.init_choose_online_mode_screen,
            "Start", 
            1/4,
            0.60,
            50, align="center"
        )
        self.quit_button = TextButton(
            self.gui_controller.stop, "Beenden", 3/4,
            0.60, 50, align="center"
        )
        self.buttons = [self.play_button, self.quit_button]

    def handle_events(self, events):
        """
        TEMPLATE PATTERN
        Routine in der das Hauptmenü Events bearbeitet
        HINWEIS: Aufgabe des controllers, aber bestimmte
        Scenes benötigen extra events.
        """
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
        self.wnd.blit(self.wnd.background)
        for i in (self.title, *self.buttons):
            self.wnd.blit_ui(i)
