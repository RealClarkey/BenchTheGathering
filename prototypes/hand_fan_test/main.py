import math
import pygame
import pygame.gfxdraw


MAX_CARDS = 7
MIN_CARDS = 1


class Card:
    def __init__(self, home_center, width, height, angle):
        self.width = width
        self.height = height
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

    def draw(self, screen, hovered=False):
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
            pygame.Vector2(-half_w, half_h)
        ]

        rotated_corners = []

        for corner in corners:
            rotated_x = corner.x * math.cos(angle_rad) - corner.y * math.sin(angle_rad)
            rotated_y = corner.x * math.sin(angle_rad) + corner.y * math.cos(angle_rad)

            rotated_corners.append((
                draw_pos.x + rotated_x,
                draw_pos.y + rotated_y
            ))

        border_colour = (255, 215, 0) if hovered else (0, 0, 0)

        pygame.gfxdraw.filled_polygon(screen, rotated_corners, border_colour)
        pygame.gfxdraw.aapolygon(screen, rotated_corners, border_colour)

        inset = 4 if not hovered else 7

        inner_corners = [
            pygame.Vector2(-half_w + inset, -half_h + inset),
            pygame.Vector2(half_w - inset, -half_h + inset),
            pygame.Vector2(half_w - inset, half_h - inset),
            pygame.Vector2(-half_w + inset, half_h - inset)
        ]

        inner_rotated_corners = []

        for corner in inner_corners:
            rotated_x = corner.x * math.cos(angle_rad) - corner.y * math.sin(angle_rad)
            rotated_y = corner.x * math.sin(angle_rad) + corner.y * math.cos(angle_rad)

            inner_rotated_corners.append((
                draw_pos.x + rotated_x,
                draw_pos.y + rotated_y
            ))

        pygame.gfxdraw.filled_polygon(screen, inner_rotated_corners, (200, 200, 200))
        pygame.gfxdraw.aapolygon(screen, inner_rotated_corners, (200, 200, 200))


def build_fan_cards(num_cards, card_width, card_height, screen_width, screen_height):
    cards = []

    fan_center_x = screen_width // 2
    fan_center_y = screen_height + 600 #260 default
    radius = 800 #600
    angle_step = 7 #7

    centre_index = (num_cards - 1) / 2

    for i in range(num_cards):
        angle = (i - centre_index) * angle_step
        rad = math.radians(angle)

        x = fan_center_x + math.sin(rad) * radius
        y = fan_center_y - math.cos(rad) * radius

        cards.append(Card((x, y), card_width, card_height, angle))

    return cards


def main():
    pygame.init()

    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("BenchTheGathering")

    clock = pygame.time.Clock()
    button_font = pygame.font.SysFont(None, 36)

    add_button = pygame.Rect(width-300, 620, 70, 60)
    sub_button = pygame.Rect(width-200, 620, 70, 60)

    num_cards = 3
    # 0.72 ratio
    card_ratio = 0.72
    card_height = 290
    card_width = card_height * card_ratio

    cards = build_fan_cards(num_cards, card_width, card_height, width, height)

    dragging_card = None
    running = True

    while running:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        hovered_card = None

        for card in reversed(cards):
            if card.rect().collidepoint(mouse_pos):
                hovered_card = card
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if add_button.collidepoint(mouse_pos):
                        if num_cards < MAX_CARDS:
                            num_cards += 1
                            cards = build_fan_cards(num_cards, card_width, card_height, width, height)

                    elif sub_button.collidepoint(mouse_pos):
                        if num_cards > MIN_CARDS:
                            num_cards -= 1
                            cards = build_fan_cards(num_cards, card_width, card_height, width, height)

                    elif hovered_card is not None:
                        dragging_card = hovered_card
                        dragging_card.is_dragging = True
                        dragging_card.is_returning = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging_card is not None:
                    dragging_card.is_dragging = False
                    dragging_card.is_returning = True
                    dragging_card = None

            if event.type == pygame.MOUSEMOTION:
                if dragging_card is not None:
                    dragging_card.pos = mouse_pos

        for card in cards:
            card.update()

        screen.fill((30, 30, 30))

        draw_cards = cards.copy()

        if hovered_card in draw_cards:
            draw_cards.remove(hovered_card)
            draw_cards.append(hovered_card)

        if dragging_card in draw_cards:
            draw_cards.remove(dragging_card)
            draw_cards.append(dragging_card)

        for card in draw_cards:
            card.draw(screen, hovered=(card == hovered_card))

        pygame.draw.rect(screen, (80, 80, 80), add_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), add_button, 3, border_radius=10)

        add_text = button_font.render("Add", True, (255, 255, 255))
        screen.blit(add_text, add_text.get_rect(center=add_button.center))

        pygame.draw.rect(screen, (80, 80, 80), sub_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), sub_button, 3, border_radius=10)

        sub_text = button_font.render("Sub", True, (255, 255, 255))
        screen.blit(sub_text, sub_text.get_rect(center=sub_button.center))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()