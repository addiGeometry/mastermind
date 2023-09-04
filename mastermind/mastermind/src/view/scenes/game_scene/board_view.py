"""
Grafische Darsatellung des Boards
"""

import pygame
from . import DARKBROWN, HOTPINK
from . import Pin, CluePin
from . import Colors

class BoardView:
    """
    Die Klasse Board ist ein Teil der Game Scene und ist für die Darstellung des Spielverlaufs
    zuständig.
    """
    __slots__ = ["spalten", "reihen", "color_amount", "width", "height", "pins_surface" ,"feedback_surface", "_board_pins", "board_feedback",
                  "_versuche", "_tilesize", "offset", "is_feedback", "_zuege"]

    def __init__(self, reihen: int, spalten: int, anzahl_farben: int, tilesize: int, offset=None, feedback=True, versuche=None):
        """
        :param reihen: Anzahl der Reihen des Spielfelds  
        :param spalten: Anzahl der Spalten des Spielfelds
        :param spalten: Anzahl der Farben im Spielmodus
        """
        self.offset = offset
        self.is_feedback = feedback
        self._tilesize = tilesize
        if not versuche:
            self._versuche = reihen
        else:
            self._versuche = versuche
        self._zuege = 0
        self.reihen = reihen + 1
        self.spalten = spalten + 1
        self.color_amount = anzahl_farben
        

        # Für die Pins
        self.pins_surface = pygame.Surface(((spalten + 1) * self.tilesize, (self.reihen + 1)* self.tilesize)).convert_alpha()
        self.pins_surface.fill((0,0,0,0))
        
        # Für das Feedback
        self.feedback_surface = pygame.Surface((self.tilesize, (self.reihen + 1) * self.tilesize)).convert_alpha()
        self.feedback_surface.fill((0,0,0,0))

        self._board_pins = []
        self.board_feedback = []

        self.create_pins()
        if feedback:
            self.create_feedback()
        else:
            self.spalten = spalten
        
        if (not self.offset == "mmb_offset" and not self.offset == "mg_rs" and not self.offset == "mg_main"):
            for pin in self.board_pins[0]:
                pin.revealed = False
        
        self.height = self.reihen * self.tilesize
        self.width = self.spalten * self.tilesize

    @property
    def tilesize(self):
        """
        Die Größe eines Tiles auf dem Feld
        """
        return self._tilesize

    def create_feedback(self):
        """
        Erzeuge die Anzeige für das Feeback
        """
        for i in range(1, self.reihen):
            temp_row = []
            line_divisor = 4
            pin_amount = 2
            x_shift = 0
            for row in range(2):
                for col in range(pin_amount):
                    temp_row.append(CluePin(col * (self.tilesize//line_divisor), (row * (self.tilesize//line_divisor))+ i * self.tilesize, tile_size=self.tilesize, x_shift=x_shift))
                if self.spalten == 6:
                    line_divisor = 4
                    pin_amount = 3
                    x_shift = -self.tilesize/8
                    
            self.board_feedback.append(temp_row)
    
    def create_pins(self):
        """
        Erzeuge die Platzhalter für die Pins auf dem GameBoard
        """
        if self.is_feedback:
            kacheln = self.spalten 
        else:
            kacheln = self.spalten + 1
        self.board_pins = [[Pin(col*self.tilesize, row*self.tilesize, tile_size=self.tilesize) for col in range(kacheln)[:-1]] for row in range(self.reihen)]

    def clear_board(self):
        self.__init__(self.reihen-1, self.spalten, self.color_amount, self.tilesize, offset=self.offset, feedback=self.is_feedback)
        self.create_pins()

    def draw(self, surface):
        """
        Zeichne das Objekt auf der Pygame Oberfläche
        """
        surface.blit(self.pins_surface, (0,0))
        surface.blit(self.feedback_surface, ((self.spalten - 1) * self.tilesize,0))

        # Pin-Platzhalter
        for row in self.board_pins:
            for pin in row:
                pin.draw(self.pins_surface)

        # Feedback Pins
        for row in self.board_feedback:
            for pin in row:
                pin.draw(self.feedback_surface)

        for x in range(0, self.width, self.tilesize):
            for y in range(0, self.height, self.tilesize):
                pygame.draw.line(surface, DARKBROWN, (x, 0), (x, self.height))
                pygame.draw.line(surface, DARKBROWN, (0, y), (self.width, y))
        pygame.draw.line(surface, DARKBROWN, (0, self.height - 1), (self.width, self.height - 1))

        # Aktuelle Reihe
        if self.offset is None:
            pygame.draw.rect(surface, HOTPINK,
                            (0, self.tilesize*(self.versuche-self.zuege), (self.spalten-1)*self.tilesize, self.tilesize), 4)
        elif self.offset   == "mg_main":
            pygame.draw.rect(surface, HOTPINK,
                            (0, self.tilesize*(self.versuche-self.zuege+1), (self.spalten)*self.tilesize, self.tilesize), 4)

    @property
    def board_pins(self):
        return self._board_pins

    @board_pins.setter
    def board_pins(self, value):
        if isinstance(value, list):
            self._board_pins = value
        else:
            raise ValueError("board_pins must be a list")
        
    @property
    def versuche(self):
        return self._versuche

    @versuche.setter
    def versuche(self, value):
        if isinstance(value, int):
            self._versuche = value
        else:
            raise ValueError("versuche must be an integer")
        
    @property
    def zuege(self):
        return self._zuege

    @zuege.setter
    def zuege(self, value):
        if isinstance(value, int):
            self._zuege = value
        else:
            raise ValueError("zuege must be an integer")

    def set_rating(self, colors: list[tuple[int, int, int, int]]):
        """
        """
        print("Versuche: ", self.versuche)
        print("Züge: ", self.zuege)
        index = self.versuche-self.zuege
        if self.offset is None:
            index -= 1
        for color, pin in zip(colors, self.board_feedback[index]):
            pin.color = color

    def next_round(self):
        self.versuche -= 1
        return self.versuche > 0