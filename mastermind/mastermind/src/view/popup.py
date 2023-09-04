import pygame as pg
from . import Window
from . import Text, TextButton, STANDARD_ALERT_BOX

class SimpleAlertDialog:
    """
    Multifunktioneller Alert-Dialog, mit dem man den Nutzer auf Dinge hinweisen kann.
    :param text: Text auf dem dialog
    :param wnd: Reference auf das Window für blitting
    :param scale: bestimme die Größe des Windows
    """

    __slots__ = ["_text", "_surface", "wnd", "ok_button", "buttons", "scale", "color"]

    def __init__(self, *rows: str, wnd: Window, scale, ok_action, color=STANDARD_ALERT_BOX) -> None:
        row_spacing = 0.25  # Adjust the spacing factor as desired
        self._text = [
            Text(row, 1/2, (i+1)/(len(rows)+1)*row_spacing + 0.3, 50, align="center")
            for i, row in enumerate(rows)
        ]
        self.wnd = wnd
        self.color = color
        self.scale = scale
        self._surface = None
        self.ok_button = TextButton(ok_action,"ok", 0, 0, 50, parent_offset=(1,1))
        self.buttons = []

    @property
    def surface(self) -> pg.surface.Surface:
        """
        Die Oberfläche des Alert-Dialogsa
        """
        return self._surface

    def draw(self, wnd: Window):
        """
        Zeichne das Objekt auf der Pygame Oberfläche
        """
        width, height = [x * self.scale for x in self.wnd.size]
        x_coord, y_coord = self.wnd.center_offset(width, height)
       
        dialog = wnd.alert_subsurface((x_coord, y_coord, width, height), self.color)
        dia_rect = dialog.get_rect()
        
        dialog_center_x = dia_rect.centerx
        dialog_center_y = dia_rect.centery

        self.ok_button.parent_offset = (dialog_center_x + x_coord, dialog_center_y + y_coord
                                        + self.ok_button.height
                                        )
        # Calculate the center coordinates of the button surface
        button_center_x = dialog_center_x - (self.ok_button._width // 2)
        button_center_y = dialog_center_y * 1.4 - (self.ok_button._height // 2)

        # Set the new coordinates for the button
        self.ok_button.offset = button_center_x, button_center_y

        for text in self._text:
            wnd.blit_ui(text)  
        dialog.blit(self.ok_button.surface, self.ok_button.offset)
