"""
Modul für die Darstellung des Fensters der Benutzeroberfläche
"""
import pygame as pg
from pubsub import pub

from .sprites import Sprite
from . import GameMode
from . import WOOD_TEXTURE_PATH, DARKBROWN, MENU_BACKGROUND_PATH


class Window:
    """
    Klass für die Darstellung des Fensters auf der GUI.
    Stellt seine länge und breite bereit.
    """
    # __slots__ = ("surface", "board_size_var", "_tilesize")

    def __init__(self, width, height, caption="Mastermind"):
        self.surface = pg.display.set_mode((width, height), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
        pg.display.set_caption(caption)
        self._tile_size = 70
        self.board_size_var = 5

        self._min_height = 800
        self._min_width = 1000
        pub.subscribe(self.set_board_size_var, "clicked_game_mode")
        self.regenerate_background()

    def set_board_size_var(self, game_mode):
        """
        Set the board size var for the different game_modes
        """
        if(game_mode == GameMode.MASTERMIND):
            self.board_size_var = 5
            self.tile_size = 70
            self._min_width = 1000
        else:
            self.board_size_var = 6
            self.tile_size = 60
            self._min_width = 1100
    
    def handle_events(self, events: list[pg.event.Event]) -> list[pg.event.Event]:
        """
        Bearbeite Events, die mit der Skalierung des Fensters zu tun haben.
        Limitiere die größe des Fensters.
        :param events: Liste aller Events
        :return: Liste Events ohne Resize
        """
        for event in events:
            if event.type == pg.VIDEORESIZE:
                width, height = event.size
                if width < self._min_width:
                    width = self._min_width
                if height < self._min_height:
                    height = self._min_height
                pg.display.set_mode((width,height), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)

                self.regenerate_background()
                events.remove(event)
        return events

    def regenerate_background(self):
        """
        Regeneriert das Hintergrundbild, um zur aktuellen Fenstergröße zu passen.
        Zentriert das Bild, erhält das Seitenverhältnis und initialisiert mit einem gezoomten Ausschnitt.
        """
        width, height = self.surface.get_size()
        original_image = pg.image.load(MENU_BACKGROUND_PATH).convert()
        original_width, original_height = original_image.get_size()
        aspect_ratio = original_width / original_height

        # Set the initial zoom factor (adjust as needed)
        zoom_factor = 1.5

        if width / height > aspect_ratio:
            new_width = int(height * aspect_ratio)
            new_height = height
        else:
            new_width = width
            new_height = int(width / aspect_ratio)

        scaled_image = pg.transform.scale(original_image, (new_width, new_height))

        zoomed_in_image = pg.transform.smoothscale(
            scaled_image, (int(new_width * zoom_factor), int(new_height * zoom_factor)))
        x_zoom_offset = (width - int(new_width * zoom_factor)) // 2
        y_zoom_offset = (height - int(new_height * zoom_factor)) // 2

        self.background = Sprite(zoomed_in_image, x_zoom_offset, y_zoom_offset)
        self.background_rect = self.background.surface.get_rect()


    @property
    def size(self) -> tuple[int, int]:
        """
        Die Größe des Fensters.
        :return: Tupel(width, height)
        """
        return pg.display.get_window_size()

    @staticmethod
    def get_sc_unit() -> tuple[int, int]:
        """
        Scale-Unit: Größenmaß. Wird
        verwendet, um die GUI Element-Größe
        zu berechnen.
        :return: Tupel(width, height)
        """
        return 0.1 * pg.display.get_window_size()[1]

    @property
    def tile_size(self) -> int:
        """
        Die Größe eines Tiles
        :return: tilegröße int
        """
        return self._tile_size
    
    @tile_size.setter
    def tile_size(self, value) -> None:
        """
        Setze die Größe eines Tiles
        :param value: neue Tilegröße int
        """
        self._tile_size = value

    @property
    def board_offset(self) -> tuple[int, int]:
        """
        Offset des Boards
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.94 - 5 * 70,
            self.size[1] * 0.02)
    
    def maker_game_rate_slot_offset(self) -> tuple[int, int]:
        """
        Offset des Boards
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.5 - 5 * 70,
            self.size[1] * 0.02)

    def center_offset(self, width: int, height: int) -> tuple[int, int]:
        """
        Erzeuge einen offset für ein Objekt im Center
        :return: (x_offset, y_offset)
        """
        x_offset = self.size[0]//2 - width//2
        y_offset = self.size[1]//2 - height//2

        return x_offset, y_offset

    @property
    def colorbar_offset(self) -> tuple[int, int]:
        """
        Offset der Colorbar
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.012,
            self.size[1] * 0.85)
    
    def maker_make_bar_offset(self, code_length: int) -> tuple[int, int]:
        """
        Offset der MakerMake Kode Bar
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.5  - self.tile_size * code_length // 2,
            self.size[1] * 0.5)
    
    def makermake_colorbar_offset(self, color_amount: int) -> tuple[int, int]:
        """
        Offset der MakerMake Colorbar
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.5 - self.tile_size * color_amount // 2,
            self.size[1] * 0.65)
    
    def maker_game_colorbar_offset(self) -> tuple[int, int]:
        """
        Offset der MakerMake Gamebar
        :return: (x_offset, y_offset)
        """
        return (self.size[0] * 0.33 - self.tile_size,
            self.size[1] * 0.65)

    def blit(self, sprite):
        """
        Füge ein zeichenbares element zur Oberfläche hinzu
        :param sprite: Sprite, zeichenbares Objekt
        """
        self.surface.blit(sprite.surface, sprite.position)
        

    def blit_w_offset(self, sprite):
        """
        Füge ein zeichenbares element zur Oberfläche hinzu
        :param sprite: Sprite, zeichenbares Objekt
        """
        self.surface.blit(sprite.surface, sprite.position)

    def blit_ui(self, text):
        """
        Methode zum Hinzufügen eines Text-Objekts zur Oberfläche
        :param text: der Text
        """
        for r in text.renders:
            pos = text.offset
            pos = tuple([elem * pos[i] for i, elem in enumerate(self.size)])
            setattr(r[1], text.align, pos)
            self.surface.blit(*r)

    def subsurface(self, rect: pg.Rect):
        """
        Methode zum Erzeugen einer Sub-Oberfläche auf dem Fenster.
        :param rect: Form aus Pygame
        """
        subsurface = self.surface.subsurface(rect)

        # Load the background image
        bg_image = pg.image.load(WOOD_TEXTURE_PATH)

        # Blit the background image onto the subsurface
        subsurface.blit(bg_image, (0, 0))

        # Draw a white border on the subsurface
        border_width = 2
        pg.draw.rect(subsurface, DARKBROWN, subsurface.get_rect(), border_width)

        return subsurface
    
    def alert_subsurface(self, rect: pg.Rect, color):
        """
        Methode zum Erzeugen einer Sub-Oberfläche auf dem Fenster.
        :param rect: Form aus Pygame
        """
        subsurface = self.surface.subsurface(rect)

        subsurface.fill(color)

        # Draw a white border on the subsurface
        border_width = 2
        rect = pg.draw.rect(subsurface, (255, 255, 255), subsurface.get_rect(), border_width)
      
        return subsurface
    
    def rescale_bg(self, sprite):
        """
        Skaliere den Background einer Szene neu
        """
        sprite.surface = pg.transform.scale(sprite.surface, self.size)

    def clear(self):
        """
        Lösche die inhalte auf der Oberfläche
        """
        self.surface.fill((0, 0, 0))