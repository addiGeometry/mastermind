"""
Package mit Klassen für die Auswahl des Usernames
"""
import pygame as pg
from pubsub import pub


from .. import (TRANSPARENT, STANDARD_BORDER, STANDARD_TEXT, HINT_TEXT, STANDARD_SELECT)
from . import Scene, TextButton, Text
from ..input_fields import InputField

class ChooseNameScene(Scene):
    """
    Scene, in der der User, wenn er online spielen will, seinen Username auswählt.
    """
    __slots__ = Scene.slots + ("background", "title", "text_input", "buttons", "quit_button",
                               "username", "draw_buttons")

    def __init__(self, gui_controller):
        super().__init__(gui_controller)
        self.username = ""
        self.title = Text("Wähle deinen Nutzernamen: ", 1/2, 0.25, 100, align="center")
        self.text_input = InputField(lambda: None, "username",
                                1/2,
                                0.52,
                                60,
                                align="center", button_color=TRANSPARENT,
                                button_hover_color=TRANSPARENT,
                                border_color=STANDARD_BORDER,
                                border_hover_color=STANDARD_SELECT,
                                input_text_color=STANDARD_TEXT,
                                text_color=HINT_TEXT
                                )
        self.quit_button = TextButton(
            self.gui_controller.stop, "Beenden", 1/2,
            0.68, 50, align="center"
        )
        self.buttons = [self.text_input, self.quit_button]
        self.draw_buttons = self.buttons.copy()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.text_input.is_under_mouse(event.pos) and not self.text_input.clicked:
                    self.text_input.input_field_on_click()
                    self.text_input.click()
                    events.remove(event)
                else:
                    # Klickt der nutzer wo anders hin, dann wird der Button wieder
                    # de-selected
                    self.text_input.click()
                    self.text_input.input_field_on_delesect()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.text_input.filled:
                        self.username_entered()
                        events.remove(event)
                else:
                    self.text_input.handle_key_input(event)
                    events.remove(event)
        return events

    def username_entered(self):
        """
        Übermittle den fertigen username an den request handler für
        den Multiplayer
        :param name: Name, den der User möchte
        """
        self.text_input.text.body.strip()
        self.gui_controller.set_username(self.text_input.text.body)

    def update(self, delta):
        pass

    def draw(self):
        self.wnd.blit(self.wnd.background)
        for i in (self.title, *self.draw_buttons):
            self.wnd.blit_ui(i)
        for i in self.sprites:
            i.draw(self.wnd)
