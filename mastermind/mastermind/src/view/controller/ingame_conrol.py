import pygame as pg
from pubsub import pub
from ..scenes import Scene
from . import Pin
from ...model.colors import Colors
from ...model.player import Role
from ..scenes.game_scene.constants import *
from ..ui import remove_event

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class InGameGuiControl(metaclass=SingletonMeta):
    """
    Klasse für GUI-Interaktion und Event-Handling wenn das Spiel im Gang ist
    """

    @classmethod
    def clear_instance(cls):
        cls._instances.clear()

    def __init__(self, scene: Scene):
        if hasattr(self, "initialized"):
            return
        self.initialized = True
        self.scene = scene
        self.gui_controller = scene.gui_controller
        self.board = self.scene.board
        self.wnd = scene.gui_controller.wnd
        self.__selected_color = None
        if self.board.offset == "mmb_offset":
            self.code_length = self.board.spalten
        else:
            self.code_length = self.board.spalten - 1
        self.my_turn = False
        self.selected = None
        pub.subscribe(self.add_rating, "add_rating")
        pub.subscribe(self.add_guess, "add_guess")
        pub.subscribe(self.receive_set_code, "send_code")
        # TO REMOVE

    def handle_events(self, events) -> list[pg.event.Event]:
        """
        Verarbeite die Click-Events auf der GUI und update das VIEW
        """
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                self.selected_color = self.select_color(self.scene.color_bar.color_selection, mx, my, self.selected_color)
                if self.select_color is not None:
                    index = self.scene.board.versuche - self.scene.board.zuege
                    self.place_pin(self.scene.board.board_pins, index, mx, my, self.selected_color)
        return events
    
    def select_color(self, pins: list[Pin], mx: int, my: int, previous_color):
        """
        Überprüft, ob der User auf einen Pin geclicked hat
        und aktualisiert nachdem die gewählte Farbe.
        :param pin: List von Pins in betrachtung
        :param mx: x-Koordinate des Mausclicks
        :param my: y-Koordinate des Mausclicks
        :param previous_color: letzte Farbe, wenn der Mausclick außerhalb
        des Tiles des Pins ist.
        """
        if not self.scene.color_bar.offset:
            colorbar_x_offset, colorbar_y_offset = self.wnd.colorbar_offset
        elif self.scene.color_bar.offset == "mmm_cbar":
            colorbar_x_offset, colorbar_y_offset = self.wnd.makermake_colorbar_offset(self.scene.color_bar.color_amount)
        elif self.scene.color_bar.offset == "mmg_rate":
            colorbar_x_offset, colorbar_y_offset = self.wnd.maker_game_colorbar_offset()
        else:
            colorbar_x_offset, colorbar_y_offset = self.wnd.colorbar_offset

        for pin in pins:
            if pin.x_coord < mx - colorbar_x_offset < pin.x_coord + self.wnd.tile_size and pin.y_coord < my - colorbar_y_offset < pin.y_coord + self.wnd.tile_size:
                return pin.color
        return previous_color

    def place_pin(self, board_pins: list[Pin], versuch: int, mx: int, my: int, color: pg.Color):
        """
        Setzte einen Pin mit der gewählten Farbe des Nutzers auf
        dem Spielboard.
        :param board_pins: Liste von Pins in der aktullen Reihe
        :param versuch: bestimmt die Reihe, bzw. den aktuellen Versuch
        (startend bei 0)
        :param mx: x-Koordinate des Mausclicks
        :param my: y-Koordinate des Mausclicks
        :param color: Farbe, die gesetzt werden soll
        """
        if not self.board.offset:
            board_x_offset, board_y_offset = self.wnd.board_offset
        elif self.scene.board.offset == "mg_rs":
            versuch = -1
            board_x_offset, board_y_offset = self.wnd.maker_game_rate_slot_offset()
        elif self.scene.board.offset == "mmb_offset":
            board_x_offset, board_y_offset = self.wnd.maker_make_bar_offset(self.board.spalten)
        else:
            board_x_offset, board_y_offset = self.wnd.board_offset
    
        for pin in board_pins[versuch]:
            if pin.x_coord < mx - board_x_offset < pin.x_coord + self.wnd.tile_size and pin.y_coord < my - board_y_offset < pin.y_coord + self.wnd.tile_size:
                pin.color = color
                break

    def handle_button_events(self, events, buttons):
        """
        Methode, die die Events einer Menge von Buttons verarbeitet
        :param events: liste von events
        :param buttons: liste von buttons
        """

        if self.scene.board.zuege == self.scene.board.versuche:
            self.win_condition()
        for event in events:
            if event.type == pg.MOUSEMOTION:
                for button in buttons:
                    if button.is_under_mouse(event.pos):
                        button.on_hover()
                        #Jedes mal nachdem ein Event verabreitet wurde, wird es aus der Liste entfernt.
                        #Wenn wieder in den gui_controller gewechselt wird, wird dadurch die Liste an zu prüfenden
                        #Events verringert.
                        remove_event(events, event)
                    elif button.hovering:
                        button.on_unhover()
                        remove_event(events, event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_under_mouse(event.pos):
                        button.on_click()
                        events.remove(event)
        return events

    def create_attempt(self) -> list[tuple[int,int,int,int]]:
        """
        Errechne den aktuellen versuch aus der GUI
        :return: Kodierungsversuch des Users
        """
        index = self.scene.board.versuche - self.scene.board.zuege
        board_pins = self.scene.board.board_pins
        if self.scene.board.offset == "mg_rs":
            index = 0
 
        self.selected = [board_pins[index][c].color for c in range(self.code_length)]
        selected_colors = [c for c in self.selected if c is not None]
        return selected_colors
    
    def send_rating_attempt(self):
        """
        Sende ein Rating/ Feedback als Event
        """
        if self.scene.board.offset == "mg_rs":
            if not self.my_turn:
                self.gui_controller.alert_user("Lass dir zuerst einen     neuen Rateversuch vom   Computer geben", lambda: self.gui_controller.close_alert(self.reload_after_alert))
                return
            else:
                attempt = self.create_attempt()
                kode = [self.parse_color(at) for at in attempt]
                pub.sendMessage("add_rating", rating=kode)

    def reload_after_alert(self):
        pg.display.flip()

    def send_guessing_attempt(self):
        """
        Sende ein Guessing attempt
        """
        attempt = self.create_attempt()
        if len(attempt) == self.code_length:
            kode = [self.parse_color(at) for at in attempt]
            pub.sendMessage("add_guess", guess=kode)
            pub.sendMessage("request_validation", guess=kode)
            self.board.zuege = self.board.zuege + 1
        else:
            print("not enough colors chosen!")
    
    def add_guess(self, guess: list[Colors]):
        # add_guess soll sich nicht doppeln
        #+if self.gui_controller.local_role == Role.MAKER:
        #    return
        if self.gui_controller.local_role == Role.BREAKER:
            return
        elif self.gui_controller.scene.board.offset == "mmb_offset":
            return
        else:    
            code = self.parse_to_gui_colors(guess)
            for i,pin in enumerate(self.scene.fremd_board.board_pins[self.scene.fremd_board.versuche-self.scene.fremd_board.zuege]):
                pin.color = code[i]
        self.scene.fremd_board.zuege = self.scene.fremd_board.zuege + 1
        self.my_turn = True
    
    def parse_color(self, gui_color: tuple[int, int, int, int]) -> Colors:
        """
        Rechne eine Farbe aus der GUI in eine Color aus dem Model um
        :return: Farbe aus Colors
        """
        if gui_color == BLACK:
            return Colors.BLACK
        elif gui_color == WHITE:
            return Colors.WHITE
        elif gui_color == RED:
            return Colors.RED
        elif gui_color == YELLOW:
            return Colors.YELLOW
        elif gui_color == GREEN:
            return Colors.GREEN
        elif gui_color == ORANGE:
            return Colors.ORANGE
        elif gui_color == BROWN:
            return Colors.BROWN
        elif gui_color == BLUE:
            return Colors.BLUE
        elif gui_color is None:
            return None
        else:
            raise ValueError("Color not recognized - Bad Color Code!")

    def parse_to_gui_colors(self, colors: list[Colors]):
        """
        Parse eine Liste von "Colors" aus dem Game-Model in Ihre Farb-
        darstellung
        :param colors: Liste aus Colors
        """
        gui_colors = []
        for color in colors:
            match color:
                case Colors.BLACK:
                    gui_colors.append(BLACK)
                case Colors.WHITE:
                    gui_colors.append(WHITE)
                case Colors.RED:
                    gui_colors.append(RED)
                case Colors.BLUE:
                    gui_colors.append(BLUE)
                case Colors.GREEN:
                    gui_colors.append(GREEN)
                case Colors.YELLOW:
                    gui_colors.append(YELLOW)
                case Colors.ORANGE:
                    gui_colors.append(ORANGE)
                case Colors.BROWN:
                    gui_colors.append(BROWN)
        return gui_colors

            
    def add_rating(self, rating: list[Colors]):
        """
        Zeige ein gegebenes Rating des Makers auf der GUI an
        :param rating: Liste von "Colors" - das Rating 
        """
        colors = self.parse_to_gui_colors(rating)
        
        if self.scene.board.offset == "mg_rs":
            self.scene.fremd_board.set_rating(colors)
            self.my_turn = False
            return
        self.board.set_rating(colors)
        self.my_turn = False

    def surrender(self):
        """
        Der Spieler gibt das Spiel auf
        """
        pub.sendMessage("clear_data")
        self.gui_controller.re_init()

    @property
    def selected_color(self):
        """
        :return: Farbe, die der Spieler setzen möchte
        """
        return self.__selected_color
    
    @selected_color.setter
    def selected_color(self, color: pg.Color):
        """
        :param color: setzt, die aktuelle Farbe, mit der der Nutzer
        setzten möchte
        """
        self.__selected_color = color

    def create_code(self):
        attempt = self.create_attempt()
        if len(attempt) == self.code_length:
            kode = [self.parse_color(at) for at in attempt]     
            self.gui_controller.init_maker_game_scene()
            for i,pin in enumerate(self.gui_controller.scene.fremd_board.board_pins[0]):
                pin.color = self.selected[i]
            pub.sendMessage("code_set", code=kode)
            pub.sendMessage("request_guess")
            self.my_turn = True
        else:
            self.gui_controller.alert_user(f"Der Code muss {self.code_length} Pins lang sein!", self.gui_controller.close_alert(self.reload_after_alert))


    def updateScene(self, scene: Scene):
        self.scene = scene

    def receive_set_code(self, code):
        kode = self.parse_to_gui_colors(code)
        
        if self.scene.board.is_feedback:
            for i,pin in enumerate(self.scene.board.board_pins[0]):
                pin.color = kode[i]
                pin.revealed = True

    def next_guess(self):
        if not self.my_turn:
            self.my_turn = False
            pub.sendMessage("request_guess")
        else:
            self.gui_controller.alert_user("Gebe zuerst deine Bewer- tung ab!", lambda: self.gui_controller.close_alert(self.reload_after_alert))

    def win_condition(self):
        if not self.gui_controller.local_online:
            if (not self.board.offset == "mmb_offset" or not self.board.offset == "mg_rs"):
                pub.sendMessage("request_code")
                self.gui_controller.alert_user("Leider hast du es nicht  geschafft den Kode zu     knacken... :(", lambda: self.gui_controller.re_init())
        else:
            self.gui_controller.alert_user("Leider hast du es nicht  geschafft den Kode zu     knacken... :(", lambda: self.gui_controller.re_init())