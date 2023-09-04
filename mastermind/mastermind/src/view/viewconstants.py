"""
Konstanten für das View
"""
import pygame as pg

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800
SC_UNIT = WINDOW_HEIGHT * 0.1

WINDOW_CAPTION = "Mastermind"

# UI COLORS
BUTTON_COLOR = (111,11,1)
BUTTON_HOVER_COLOR = (143,21,33)
STANDARD_BORDER = (255,255,255)
STANDARD_SELECT = (105,64,144)
GREEN_BUTTON = (44,122,32)
DARK_GREEN_BUTTON = (44,105,26)
LIGHT_BG = (84,36,19, 69)

# Fonts
#GVTIME_FONT_PATH = "assets/fonts/GvtimeRegular.otf"
GVTIME_FONT_PATH = "assets/fonts/Astrella.otf"

# Images
MENU_BACKGROUND_PATH = "assets/backgrounds/menu_bg3.jpg"
WOOD_TEXTURE_PATH = "assets/backgrounds/wood-texture-seamless.jpg"

# UI Design Leitfaden
LIGHTGREY = (200,200,200)
DARKBROWN = (84,36,19)
LIGHTBROWN = (127,103,95)
TRANSPARENT = (0,0,0,0)
STANDARD_TEXT = (255,255,255)
HINT_TEXT = (244,244,244)
STANDARD_ALERT_BOX = (222,222,22,255)
HOTPINK = (255,105,180,255)

# USERNAME
MIN_USERNAME = 4
MAX_USERNAME = 10

__all__ = ["WINDOW_WIDTH", "WINDOW_HEIGHT", "SC_UNIT", "WINDOW_CAPTION", "BUTTON_COLOR",
            "BUTTON_HOVER_COLOR", "GVTIME_FONT_PATH", "MENU_BACKGROUND_PATH",
            "WOOD_TEXTURE_PATH", "LIGHTGREY", "DARKBROWN", "STANDARD_BORDER", "STANDARD_TEXT",
            "TRANSPARENT", "HINT_TEXT", "MIN_USERNAME", "MAX_USERNAME", "STANDARD_ALERT_BOX",
            "STANDARD_SELECT", "LIGHT_BG", "LIGHTBROWN", "HOTPINK", "GREEN_BUTTON", "DARK_GREEN_BUTTON"]
