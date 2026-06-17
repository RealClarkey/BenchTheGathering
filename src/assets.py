from pathlib import Path

import pygame


BASE_DIR = Path(__file__).resolve().parent.parent
UI_ASSET_DIR = BASE_DIR / "assets" / "images" / "ui"
LOGO_ASSET_DIR = BASE_DIR / "assets" / "images" / "logo"
CARD_ASSET_DIR = BASE_DIR / "assets" / "images" / "cards"


class UIAssets:
    def __init__(self):
        self.background = self.load("background.jpg")
        self.player_hero = self.load("player_hero.png")
        self.enemy_hero = self.load("enemy_hero.png")
        self.next_turn = self.load("next_turn.png")
        self.logo = self.load_logo("logo.png")

    def load(self, filename):
        return pygame.image.load(str(UI_ASSET_DIR / filename)).convert_alpha()

    def load_logo(self, filename):
        return pygame.image.load(str(LOGO_ASSET_DIR / filename)).convert_alpha()

    def scaled(self, surface, size):
        return pygame.transform.smoothscale(surface, size)

    def scaled_to_fit(self, surface, max_size):
        max_width, max_height = max_size
        scale = min(max_width / surface.get_width(), max_height / surface.get_height())
        size = (
            int(surface.get_width() * scale),
            int(surface.get_height() * scale),
        )
        return self.scaled(surface, size)


class CardAssets:
    def __init__(self):
        self.battle = self.load("battle.png")
        self.mana = self.load("mana.png")

    def load(self, filename):
        return pygame.image.load(str(CARD_ASSET_DIR / filename)).convert_alpha()
