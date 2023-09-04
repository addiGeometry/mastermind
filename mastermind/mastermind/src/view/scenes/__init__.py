"""
Package für alle Scenen im Spiel.
Scenen entsprechen GUI-Zuständen. Eine Scene beinhaltet
die Darstellende Logik und greift auf die GUI-Controller-Klassen zurück,
um Events zu senden oder sich selbst updzudaten. Einige Scenen enthalten
auch kleine View-Verarbeitungs-Mechanismen, weil das die Handhabung
vereinfacht.
"""


from .. import Sprite, Text, TextButton, DARKBROWN, LIGHTGREY
from .. import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BACKGROUND_PATH

from .scenes import Scene
from .choose_gamemode_scene import ChooseGameModeScene
from .choose_online_scene import ChooseOnlineModeScene
from .menu_scene import MenuScene
from .choose_role_scene import ChooseRoleScene
from .game_scene.game_scene import BreakerGameScene
from .game_scene.maker_scene import MakerMakeScene, MakerGameScene
from .choose_name_scene import ChooseNameScene
from .choose_ip_and_port_scene import ChoosePortAndIP

__all__ = ["Scene", "ChooseRoleScene", "MenuScene", "ChooseOnlineModeScene",
           "ChooseGameModeScene", "BreakerGameScene", "ChooseNameScene", "ChoosePortAndIP",
           "MakerMakeScene"]

