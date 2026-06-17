import pygame

from src.assets import CardAssets
from src.cards.card_catalog import create_hero_cards


class PlayerHeroSelectScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 24)
        self.heroes = create_hero_cards()
        self.hero_rects = []
        self.card_assets = CardAssets()
        self.card_image_cache = {}

        self.create_layout()

    def create_layout(self):
        card_width = 180
        card_height = 240
        gap = 24
        columns = 5
        start_x = (self.game.width - ((card_width * columns) + (gap * (columns - 1)))) // 2
        start_y = 170

        self.hero_rects = []

        for index, hero in enumerate(self.heroes):
            row = index // columns
            column = index % columns
            x = start_x + column * (card_width + gap)
            y = start_y + row * (card_height + gap)
            self.hero_rects.append((hero, pygame.Rect(x, y, card_width, card_height)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("menu")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for hero, rect in self.hero_rects:
                if rect.collidepoint(event.pos):
                    self.game.selected_player_hero = hero
                    self.game.change_screen("battle")
                    break

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((35, 35, 70))

        title_text = self.font.render("Choose Your Player Hero", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width // 2, 80))
        screen.blit(title_text, title_rect)

        for hero, rect in self.hero_rects:
            card_image = self.image_for_card(hero, rect.size)

            if card_image is not None:
                screen.blit(card_image, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                continue

            pygame.draw.rect(screen, (220, 220, 220), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            name_text = self.card_font.render(hero.name, True, (0, 0, 0))
            type_text = self.card_font.render(f"Type: {hero.hero_type}", True, (0, 0, 0))
            hp_text = self.card_font.render(f"HP: {hero.hit_points}", True, (0, 0, 0))

            screen.blit(name_text, (rect.x + 12, rect.y + 24))
            screen.blit(type_text, (rect.x + 12, rect.y + 64))
            screen.blit(hp_text, (rect.x + 12, rect.y + 104))

    def image_for_card(self, card, size):
        cache_key = (card.name, card.card_type, size)

        if cache_key not in self.card_image_cache:
            self.card_image_cache[cache_key] = self.card_assets.scaled_image_for_card(card, size)

        return self.card_image_cache[cache_key]
