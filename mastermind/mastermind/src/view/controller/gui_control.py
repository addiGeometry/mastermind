"""
Controller für die GUI.
"""
import sys
import pygame as pg
from pubsub import pub
import re
import copy

from .. import Colors
from ..ui import remove_event
from mastermind import Role
from mastermind import GameMode

from ..popup import SimpleAlertDialog
from .. import (Window,
               WINDOW_CAPTION, MIN_USERNAME,
               MAX_USERNAME, DARKBROWN)

from ..scenes import (MenuScene, ChooseOnlineModeScene,
                ChooseRoleScene, ChooseGameModeScene, ChoosePortAndIP)
from ..scenes import (ChooseNameScene, BreakerGameScene, MakerMakeScene,
                      MakerGameScene)
from .ingame_conrol import InGameGuiControl

WHITE = (255, 255, 255)
FPS = 200
INIT_WIDTH = 1280
INIT_HEIGHT = 800
IPV4_REGEX = r"^(?:\d{1,3}\.){3}\d{1,3}$"


class GuiController:
    """
    Klasse des GUI-Controllers
    """
    # doenst work in combination with pub sub
    # __slots__ = ("_run", "_paused", "clock", "wnd", "scene", "newgamedata")

    def __init__(self):
        """
        Initialisiert den GUI-Controller. Kümmert sich um die Messung der Frame rate und
        instanziiert das Hauptmenü.
        """
        # limit the execution speed of the game to 60FPS
        self._run = True
        self.clock = pg.time.Clock()
        self.wnd = Window(INIT_WIDTH, INIT_HEIGHT, WINDOW_CAPTION)
        self.scene = MenuScene(self)
        self.local_role = None
        self.local_game_mode = None
        self.local_online = None
        # self.scene = BreakerGameScene(self, 10, 4, 6)
        self.scene_backup = None
        self.button_backup = []
        self.sprite_backup = []
        self.dialogs = []

        pub.subscribe(self.start_game, "start_game")
        pub.subscribe(self.connection_established, "http_established")
        pub.subscribe(self.bad_request, "bad_http_request")
        pub.subscribe(self.init_maker_game_scene, "maker_game_start")
        pub.subscribe(self.bad_request,"send_modal")
        pub.subscribe(self.kick_to_main_menu, "kick_to_main_menu")

        pub.subscribe(self.game_won, "game_won")

        self.next_scene = None


    def run(self):
        """
        Run Routine des GUI-Controllers
        """
        while self._run:
            frame_delta = self.clock.tick() * 0.001
            # pygame events
            events = pg.event.get()
            events = self.wnd.handle_events(events)
            events = self.scene.handle_events(events)
            events = self.handle_button_events(events, self.scene.buttons)
            for event in events:
                if event.type == pg.QUIT:
                    self.stop()

            self.scene.update(frame_delta)

            if frame_delta < 0.1:
                self.wnd.clear()
                self.scene.draw()
                pg.display.flip()

    def stop(self):
        """
        Beendet das Programm
        """
        # TODO Maybe in the Future: Close Leaking ressources! ==> Callback needed
        pg.quit()
        sys.exit()

    def init_choose_online_mode_screen(self):
        """
        Spiel Gestartet => Hauptmenü ==spielen==> init_choose_online_mode_screen
        Wechsle in den Screen, indem der User auswählen kann, ob er online oder 
        offline spielt.
        """
        self.scene = ChooseOnlineModeScene(self)
        self.wnd.clear()
        pg.display.flip()


    def init_choose_gamemode(self):
        """
        ChooseIfOnlineMode ==isMultiplayer?==> init_choose_gamemode
        Wechsle in den Screen, indem der User den Spielmodus auswählen kann
        (Super Mastermind, Original Mastermind)
        """
        self.scene = ChooseGameModeScene(self)
        self.wnd.clear()
        pg.display.flip()

    def init_choose_role_screen(self):
        """
        Initialisiere den Screen, in dem die Rolle(Coder, Breaker) ausgewählt werden kann.
        """
        if not self.local_online:
            self.scene = ChooseRoleScene(self)
            self.wnd.clear()
            pg.display.flip()
        else:
            self.set_role(Role.BREAKER)
            # TODO fire event?
        
    def init_choose_playername(self):
        """
        Initialisiere den Screen(im Onlinemodus), in dem der Spieler seinen Namen auswählt
        """
        self.scene = ChooseNameScene(self)
        self.wnd.clear()
        pg.display.flip()
    

    def init_choose_ip_and_port_screen(self):
        """
        ChhoseNameScene ==name?==> init_choose_ip_and_port_scree
        Wechsle in den Screen, indem der User den Spielmodus auswählen kann
        (Super Mastermind, Original Mastermind)
        """
        self.scene = ChoosePortAndIP(self)
        self.wnd.clear()
        pg.display.flip()

    def set_is_online(self, is_online: bool):
        """
        Setzte, ob der Spieler online oder offline spielen möchte
        """
        self.local_online = is_online
        if not is_online:    
            self.init_choose_gamemode()
        else:
            self.init_choose_playername()
        pub.sendMessage("clicked_online", online_mode=is_online)

    def set_username(self, name: str):
        """
        Setzte, den Username des Spielers
        """
        if MIN_USERNAME <= len(name):
            pub.sendMessage("username_set", username=name)
            self.init_choose_ip_and_port_screen()
        else:
            self.alert_user(f"Der Name muss zwischen {MIN_USERNAME} und {MAX_USERNAME} "
                            + "Zeichen lang sein", self.init_choose_playername)
    
    def set_gamemode(self, game_mode: GameMode):
        """
        Setzte, ob der Spieler Mastermind (original) oder Super spielen will.
        """
        self.local_game_mode = game_mode
        self.init_choose_role_screen()
        pub.sendMessage("clicked_game_mode", game_mode=game_mode)
        pub.sendMessage("handshake")

    def set_role(self, role: Role):
        """
        Setzte, ob der Spieler als Kodierer oder Rater spielen möchte
        """
        self.local_role = role
        self.create_game()
        pub.sendMessage("clicked_role", role=role)

    def create_game(self):
        """
        Feuere das Event um ein neues Game zu erstellen
        """
        if not (self.local_game_mode or self.local_role):
            raise RuntimeError("No game infos specified. Bad method call for 'create_game'")

        pub.sendMessage("create_game",
                        game_mode=self.local_game_mode,
                        role=self.local_role)
        pub.sendMessage("clicked_online_play", online_mode=self.local_online)

    def start_game(self, anzahl_zuege: int, code_length: int, anzahl_farben: int):
        """
        Starte das Spiel
        """
        if self.local_role == Role.BREAKER:
            self.scene = BreakerGameScene(self, anzahl_zuege, code_length, anzahl_farben)
            self.wnd.clear()
            pg.display.flip()
        else:
            self.init_maker_make_scene(code_length, anzahl_farben, anzahl_zuege)

    def init_maker_make_scene(self, code_length, anzahl_farben, anzahl_zuege):
        self.wnd.clear()
        self.scene = MakerMakeScene(self, code_length, anzahl_farben)
        self.next_scene = MakerGameScene(self, anzahl_zuege, code_length, anzahl_farben)
        self.next_scene.fremd_board.versuche = anzahl_zuege
        self.next_scene.ingame_gui_controller = self.scene.ingame_gui_controller
        pg.display.flip()
    
    def init_maker_game_scene(self):
        self.wnd.clear()
        #HARD CODED!!!
        #TODO REMOVE ME
        self.scene.ingame_gui_controller.scene = self.next_scene
        self.scene.ingame_gui_controller.selected_color = None
        self.scene = self.next_scene
        self.wnd.clear()
        pg.display.flip()

    def alert_user(self, alert: str, callback) -> None:
        """
        Öffne ein Popup, um den Nutzer auf etwas hinzuweisen
        """
        rows = [alert[i:i+25] for i in range(0, len(alert), 25)]
        dialog = SimpleAlertDialog(*rows, wnd=self.wnd, scale=0.7, ok_action=lambda: self.close_alert(callback),
                                color=DARKBROWN)

        self.button_backup = list(self.scene.buttons)  # Create a new list instead of copying the reference
        self.sprite_backup = list(self.scene.sprites)  # Create a new list instead of copying the reference
        self.scene.sprites.append(dialog)
        self.scene.buttons.append(dialog.ok_button)
        self.dialogs.append(dialog)
        dialog.draw(dialog.wnd)
        dialog.ok_button.render()
        pg.display.flip()

    def close_alert(self, callback) -> None:
        """
        Schließe ein Alert Popup
        """
        self.scene.sprites = list(self.sprite_backup)  # Create a new list instead of copying the reference
        self.scene.buttons = list(self.button_backup)  # Create a new list instead of copying the reference
        self.scene.draw_buttons = list(self.button_backup)  # Create a new list instead of copying the reference
        
        callback()

    def handle_button_events(self, events, buttons):
        """
        Methode, die die Events einer Menge von Buttons verarbeitet
        :param events: liste von events
        :param buttons: liste von buttons
        """ 
        for event in events:
            if event.type == pg.MOUSEMOTION:
                for button in buttons:
                    if button.is_under_mouse(event.pos):
                        button.on_hover()
                    elif button.hovering:
                        button.on_unhover()
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_under_mouse(event.pos):
                        button.on_click()
                        remove_event(events, event)
        return events
        
    def attempt_ip_and_port(self, ip: str, port: str):
        """
        Überprüfe zurnächst, ob die Eingaben für IP und Port
        sinnvoll sind.
        :param ip: IP, die zu checken ist
        :param port: Port, der zu checken ist
        """
        pub.sendMessage("transmit_network_data", ip=ip, port=port)
        self.init_choose_gamemode()

    def bad_request(self, message="Fehler: Überprüfe deine  IP-Adresse und den Port"):
        """
        wird aufgerufen, wenn beim Aufbau der HTTP Request ein Fehler auftritt
        """
        self.alert_user(message,
                        self.init_choose_ip_and_port_screen)

    def connection_established(self):
        """
        Wird aufgerufen, wenn erfolgreich ein multiplayer erzeugt wurde.
        Startet die nächste Szene
        ==> init_choose_gamemode
        """
    
    def kick_to_main_menu(self, reason):
        self.alert_user(reason,
                        self.__init__)
        
    def re_init(self):
        pub.sendMessage("clear_data")
        self._run = True
        self.clock = pg.time.Clock()
        self.wnd = Window(INIT_WIDTH, INIT_HEIGHT, WINDOW_CAPTION)
        self.scene = MenuScene(self)
        self.local_role = None
        self.local_game_mode = None
        self.local_online = None
        # self.scene = BreakerGameScene(self, 10, 4, 6)
        self.scene_backup = None
        self.button_backup = []
        self.sprite_backup = []
        self.dialogs = []
        self.next_scene = None
        InGameGuiControl.clear_instance()
        self.wnd.clear()
        pg.display.flip()

    def game_won(self):
        if isinstance(self.scene, BreakerGameScene):
            self.alert_user("Glückwunsch! Du hast den Code erraten!", lambda: self.re_init())
        elif isinstance(self.scene, MakerGameScene):
            self.alert_user("Der Computer konnte dei- nen Code erraten. Das    Spiel ist vorbei", lambda: self.re_init())
