"""
Sprites im Kontext von Pygame sind Grafikelemente oder Objekte, die in Videospielen 
oder interaktiven Anwendungen dargestellt und manipuliert werden. Sie repräsentieren
in Mastermind Formen, Objekte oder Hintergründe und werden in einer Sprite-Gruppe organisiert.
Sprites haben Eigenschaften und Funktionen, um Bewegungen, Kollisionen und Animationen
zu steuern.
"""

class Sprite:
    """
    Selbst definierte Klasse für Sprites
    """
    __slots__ = ("surface", "rect")

    def __init__(self, surface, x, y):
        self.surface = surface
        self.rect = surface.get_rect().move(x, y)


    @property
    def width(self):
        """
        property
        :return width
        """
        return self.rect.w

    @property
    def height(self):
        """
        property
        :return height
        """
        return self.rect.h

    @property
    def x_coord(self):
        """
        property
        :return x_coord
        """
        return self.rect.x

    @property
    def y_coord(self):
        """
        property
        :return y_coord
        """
        return self.rect.y

    @property
    def position(self):
        """
        property
        :return position
        """
        return (self.rect.x, self.rect.y)

    @position.setter
    def position(self, pos: tuple[int, int]):
        """
        Setze die Position
        """
        self.rect.x, self.rect.y = pos

    @property
    def size(self):
        """
        property
        :return size
        """
        return (self.width, self.height)

