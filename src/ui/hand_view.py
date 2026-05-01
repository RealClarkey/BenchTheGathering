import math

import pygame
import pygame.gfxdraw


class FanCardView:
    def __init__(self, card, home_center, width, height, angle):
        self.card = card

        self.width = int(width)
        self.height = int(height)
        self.angle = angle

        self.home_center = pygame.Vector2(home_center)
        self.pos = pygame.Vector2(home_center)

        self.is_dragging = False
        self.is_returning = False

    def rect(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.pos
        return rect

    def update(self):
        if self.is_returning:
            speed = 0.2
            self.pos += (self.home_center - self.pos) * speed

            if self.pos.distance_to(self.home_center) < 1:
                self.pos = self.home_center.copy()
                self.is_returning = False

    def draw(self, screen, font, hovered=False):
        draw_pos = self.pos.copy()

        if hovered and not self.is_dragging and not self.is_returning:
            draw_pos.y -= 20

        angle_rad = math.radians(self.angle)
        half_w = self.width / 2
        half_h = self.height / 2

        corners = [
            pygame.Vector2(-half_w, -half_h),
            pygame.Vector2(half_w, -half_h),
            pygame.Vector2(half_w, half_h),
            pygame.Vector2(-half_w, half_h),
        ]

        rotated_corners = []
        for corner in corners:
            rotated_x = corner.x * math.cos(angle_rad) - corner.y * math.sin(angle_rad)
            rotated_y = corner.x * math.sin(angle_rad) + corner.y * math.cos(angle_rad)
            rotated_corners.append((draw_pos.x + rotated_x, draw_pos.y + rotated_y))

        border_colour = (255, 215, 0) if hovered else (0, 0, 0)

        pygame.gfxdraw.filled_polygon(screen, rotated_corners, border_colour)
        pygame.gfxdraw.aapolygon(screen, rotated_corners, border_colour)

        inset = 7 if hovered else 4

        inner_corners = [
            pygame.Vector2(-half_w + inset, -half_h + inset),
            pygame.Vector2(half_w - inset, -half_h + inset),
            pygame.Vector2(half_w - inset, half_h - inset),
            pygame.Vector2(-half_w + inset, half_h - inset),
        ]

        inner_rotated_corners = []
        for corner in inner_corners:
            rotated_x = corner.x * math.cos(angle_rad) - corner.y * math.sin(angle_rad)
            rotated_y = corner.x * math.sin(angle_rad) + corner.y * math.cos(angle_rad)
            inner_rotated_corners.append((draw_pos.x + rotated_x, draw_pos.y + rotated_y))

        pygame.gfxdraw.filled_polygon(screen, inner_rotated_corners, (220, 220, 220))
        pygame.gfxdraw.aapolygon(screen, inner_rotated_corners, (220, 220, 220))

        # Temporary card text. Later this can move into card_view.py.
        name_text = font.render(self.card.name, True, (0, 0, 0))
        name_rect = name_text.get_rect(center=draw_pos)
        screen.blit(name_text, name_rect)


class HandView:
    def __init__(self, cards, hand_rect):
        self.cards = cards
        self.hand_rect = hand_rect

        self.card_ratio = 0.72
        self.card_height = int(hand_rect.height * 1.2) #1.7 was default
        self.card_width = int(self.card_height * self.card_ratio)

        self.radius = int(hand_rect.width * 0.95) #0.95 default
        self.angle_step = 7

        self.card_views = []
        self.hovered_card = None
        self.dragging_card = None

        # Dropped card mechanics
        self.dropped_card = None
        self.drop_position = None

        self.font = pygame.font.SysFont(None, 20)

        self.build_fan()

    def build_fan(self):
        self.card_views.clear()

        num_cards = len(self.cards)

        if num_cards == 0:
            return

        fan_center_x = self.hand_rect.centerx
        fan_center_y = self.hand_rect.bottom + int(self.hand_rect.height * 2.75) #3.5 as default

        centre_index = (num_cards - 1) / 2

        for i, card in enumerate(self.cards):
            angle = (i - centre_index) * self.angle_step
            rad = math.radians(angle)

            x = fan_center_x + math.sin(rad) * self.radius
            y = fan_center_y - math.cos(rad) * self.radius

            card_view = FanCardView(
                card=card,
                home_center=(x, y),
                width=self.card_width,
                height=self.card_height,
                angle=angle,
            )

            self.card_views.append(card_view)

    def handle_event(self, event):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        self.hovered_card = self.get_hovered_card(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered_card is not None:
                self.dragging_card = self.hovered_card
                self.dragging_card.is_dragging = True
                self.dragging_card.is_returning = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging_card is not None:
                self.dropped_card = self.dragging_card.card
                self.drop_position = event.pos

                self.dragging_card.is_dragging = False
                self.dragging_card.is_returning = True
                self.dragging_card = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_card is not None:
                self.dragging_card.pos = mouse_pos

    def update(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.hovered_card = self.get_hovered_card(mouse_pos)

        for card_view in self.card_views:
            card_view.update()

    def draw(self, screen):
        draw_cards = self.card_views.copy()

        # Draw hovered/dragged card last so it appears on top.
        if self.hovered_card in draw_cards:
            draw_cards.remove(self.hovered_card)
            draw_cards.append(self.hovered_card)

        if self.dragging_card in draw_cards:
            draw_cards.remove(self.dragging_card)
            draw_cards.append(self.dragging_card)

        for card_view in draw_cards:
            card_view.draw(
                screen,
                self.font,
                hovered=(card_view == self.hovered_card),
            )

    def get_hovered_card(self, mouse_pos):
        for card_view in reversed(self.card_views):
            if card_view.rect().collidepoint(mouse_pos):
                return card_view

        return None