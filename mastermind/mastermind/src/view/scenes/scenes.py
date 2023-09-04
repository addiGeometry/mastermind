"""
Python File für die Abstrakte Klasse einer Szene (Scene).
In Pygame entspricht die Szene einer "Leinwand" oder auch anders
gesagt dem Fenster, auf dem Surfaces, Objekte und Sprites gerendert werden.
"""

import abc

#TODO all?
#__all__ = ("MenuScene", "")


class Scene(metaclass=abc.ABCMeta):
    """
    Abstrakte Klasse für Scenes
    """
    #SLOTS lassen sich nicht si gut vererben.... ._.
    slots = ("gui_controller", "wnd", "frames", "timer", "sprites", "buttons")

    def __init__(self, gui_controller):
        """
        Eine Szene bekommt den gui_controller, um auf seine Funktionen zuzugreifen
        """
        self.gui_controller = gui_controller
        self.wnd = gui_controller.wnd
        self.frames = 0
        self.timer = 0
        self.sprites = []

    @property
    def fps(self):
        if not self.timer:
            return 0
        
        return self.frames / self.timer
    
    def handle_events(self, events):
        return events
    
    def update(self, delta):
        raise NotImplementedError
    
    def draw(self):
        raise NotImplementedError