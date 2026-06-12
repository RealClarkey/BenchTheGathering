from pathlib import Path

import pygame


BASE_DIR = Path(__file__).resolve().parent.parent
UI_ASSET_DIR = BASE_DIR / "assets" / "images" / "ui"


class UIAssets:
    def __init__(self):
        self.background = self.load("background.jpg")
        self.player_hero = self.load("player_hero.png")
        self.enemy_hero = self.load("enemy_hero.png")
        self.next_turn = self.load("next_turn.png")

    def load(self, filename):
        return pygame.image.load(str(UI_ASSET_DIR / filename)).convert_alpha()

    def scaled(self, surface, size):
        return pygame.transform.smoothscale(surface, size)
