"""
Package mit Klassen für die Auswahl eines Ports und einer IP
für den Online-Modus
"""
import pygame as pg
from pubsub import pub
from ..ui import remove_event

from .. import (TRANSPARENT, STANDARD_TEXT, HINT_TEXT, LIGHTGREY,
                STANDARD_SELECT)
from . import Scene, Text, TextButton
from ..input_fields import InputField

class ChoosePortAndIP(Scene):
    """
    Scene, in der der User, wenn er online spielen will, die IP-Adresse und den Port
    festlegt
    """
    __slots__ = Scene.slots + ("background", "title", "subtitle", "ip_input", "port_input", "buttons", "quit_button",
                               "ip", "port", "draw_buttons", "text", "forms", "selected")

    def __init__(self, gui_controller):
        super().__init__(gui_controller)
        self.ip = ""

        self.title = Text("Wähle IP & Port", 1/2, 0.25, 100, align="center")
        self.subtitle = Text("für den onlinemodus", 1/2, 0.32, 100, align="center")
        self.ip_input = InputField(lambda: 2, "IP-Adresse:",
                                1/2,
                                0.52,
                                50,
                                align="center", button_color=TRANSPARENT,
                                button_hover_color=TRANSPARENT,
                                border_color=LIGHTGREY,
                                border_hover_color=STANDARD_SELECT,
                                input_text_color=STANDARD_TEXT,
                                text_color=HINT_TEXT,
                                scale=4
                                )
        self.port_input = InputField(lambda: 2, "Port:",
                                1/2,
                                0.65,
                                50,
                                align="center", button_color=TRANSPARENT,
                                button_hover_color=TRANSPARENT,
                                border_color=LIGHTGREY,
                                border_hover_color=STANDARD_SELECT,
                                input_text_color=STANDARD_TEXT,
                                text_color=HINT_TEXT,
                                scale=4
                                )
        self.quit_button = TextButton(
            self.gui_controller.stop, "Beenden", 1/2,
            0.80, 50, align="center"
        )
        self.forms = [self.ip_input, self.port_input]
        self.buttons = [self.quit_button, self.ip_input, self.port_input]
        self.text = [self.title, self.subtitle]
        self.selected = None
        self.draw_buttons = self.buttons.copy()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked_input_field = None
                for text_input_field in self.forms:
                    if text_input_field.is_under_mouse(event.pos):
                        clicked_input_field = text_input_field
                        break

                if self.selected and self.selected != clicked_input_field:
                    self.selected.input_field_on_delesect()
                    self.selected.click()
                    self.selected.render()
                    self.selected = None  # Deselect the previously selected field

                if clicked_input_field:
                    if not clicked_input_field.clicked:  # Check if not double-clicked
                        self.selected = clicked_input_field
                        self.selected.input_field_on_click()
                        self.selected.click()
                        self.selected.render()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    filled = all(text_input_field.text.body != text_input_field.type
                                 for text_input_field in self.forms)
                    if filled:
                        self.gui_controller.attempt_ip_and_port(self.ip_input.text.body,
                                                                self.port_input.text.body)
                        remove_event(events, event)
                        break
                elif self.selected:
                    self.selected.handle_key_input(event, max=16)
                    remove_event(events, event)

        return events


    def update(self, delta):
        pass

    def draw(self):
        self.wnd.blit(self.wnd.background)
        for form in (*self.forms, self.title):
            self.wnd.blit_ui(form)
        self.wnd.blit_ui(self.quit_button)
        for i in self.sprites:
            i.draw(self.wnd)