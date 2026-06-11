import pygame

from src.cards.card_catalog import create_hero_cards


class CommanderSelectScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 24)
        self.heroes = create_hero_cards()
        self.hero_rects = []

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
                    self.game.selected_commander = hero
                    self.game.change_screen("battle")
                    break

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((35, 35, 70))

        title_text = self.font.render("Choose Your Commander", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width // 2, 80))
        screen.blit(title_text, title_rect)

        for hero, rect in self.hero_rects:
            pygame.draw.rect(screen, (220, 220, 220), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            name_text = self.card_font.render(hero.name, True, (0, 0, 0))
            type_text = self.card_font.render(f"Type: {hero.hero_type}", True, (0, 0, 0))
            hp_text = self.card_font.render(f"HP: {hero.hit_points}", True, (0, 0, 0))

            screen.blit(name_text, (rect.x + 12, rect.y + 24))
            screen.blit(type_text, (rect.x + 12, rect.y + 64))
            screen.blit(hp_text, (rect.x + 12, rect.y + 104))
