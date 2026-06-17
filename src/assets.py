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
        self.elf = self.load("elf.png")
        self.ishani = self.load("ishani.png")
        self.knight = self.load("knight.png")
        self.mana = self.load("mana.png")
        self.moldrax = self.load("moldrax.png")
        self.troll = self.load("troll.png")
        self.wizard = self.load("wizard.png")
        self.type_images = {
            "Mana": self.mana,
            "Skill": self.battle,
        }
        self.named_images = {
            "Elf": self.elf,
            "Ishani": self.ishani,
            "Knight": self.knight,
            "Moldrax": self.moldrax,
            "Troll": self.troll,
            "Wizard": self.wizard,
        }

    def load(self, filename):
        return pygame.image.load(str(CARD_ASSET_DIR / filename)).convert_alpha()

    def image_for_card(self, card):
        return self.named_images.get(card.name) or self.type_images.get(card.card_type)

    def scaled_image_for_card(self, card, size):
        image = self.image_for_card(card)

        if image is None:
            return None

        return pygame.transform.smoothscale(image, size)
