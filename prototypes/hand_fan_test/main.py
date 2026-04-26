import math
import pygame


num_cards = 3
cards_need_update = False
selected_card_index = None

def build_fan_cards(num_cards, card_width, card_height, screen_width, screen_height):
    cards = []

    fan_center_x = screen_width // 2
    fan_center_y = screen_height + 260
    radius = 600

    angle_step = 7
    centre_index = (num_cards - 1) / 2

    angles = [(i - centre_index) * angle_step for i in range(num_cards)]

    for angle in angles:
        rad = math.radians(angle)

        x = fan_center_x + math.sin(rad) * radius
        y = fan_center_y - math.cos(rad) * radius

        rect = pygame.Rect(0, 0, card_width, card_height)
        rect.center = (x, y)

        cards.append((rect, angle))

    return cards




def main():
    global cards_need_update, selected_card_index, num_cards

    pygame.init()

    # ADD BUTTON
    add_button = pygame.Rect(1080, 620, 70, 60)
    button_font = pygame.font.SysFont(None, 36)

    # SUB BUTTON

    sub_button = pygame.Rect(1160, 620, 70, 60)
    button_font = pygame.font.SysFont(None, 36)

    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("BenchTheGathering")

    card_width = 128
    card_height = 180

    cards = build_fan_cards(num_cards, card_width, card_height, width, height)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if add_button.collidepoint(mouse_pos):
                    if num_cards < 7:
                        num_cards += 1
                        selected_card_index = None
                        cards_need_update = True

                elif sub_button.collidepoint(mouse_pos):
                    if num_cards > 1:
                        num_cards -= 1
                        selected_card_index = None
                        cards_need_update = True

                else:
                    for i in range(len(cards) - 1, -1, -1):
                        card, angle = cards[i]

                        if card.collidepoint(mouse_pos):
                            if selected_card_index == i:
                                selected_card_index = None
                            else:
                                selected_card_index = i
                            break


        if cards_need_update:
            cards = build_fan_cards(num_cards, card_width, card_height, width, height)
            cards_need_update = False

        screen.fill((30, 30, 30))

        draw_order = list(range(len(cards)))

        if selected_card_index is not None:
            draw_order.remove(selected_card_index)
            draw_order.append(selected_card_index)

        for i in draw_order:
            card, angle = cards[i]

            card_surface = pygame.Surface((card.width, card.height), pygame.SRCALPHA)

            pygame.draw.rect(
                card_surface,
                (200, 200, 200),
                card_surface.get_rect(),
                border_radius=10
            )

            # Default border
            border_colour = (0, 0, 0)
            border_width = 3

            # Highlight selected card
            if i == selected_card_index:
                border_colour = (255, 215, 0)
                border_width = 6

            pygame.draw.rect(
                card_surface,
                border_colour,
                card_surface.get_rect(),
                border_width,
                border_radius=10
)

            rotated_card = pygame.transform.rotate(card_surface, -angle)
            draw_center = card.center

            if i == selected_card_index:
                draw_center = (card.centerx, card.centery - 10) # Tweak this for card height movement.

            rotated_rect = rotated_card.get_rect(center=draw_center)

            screen.blit(rotated_card, rotated_rect)
        
        # ADD BUTTON
        pygame.draw.rect(screen, (80, 80, 80), add_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), add_button, 3, border_radius=10)

        add_text = button_font.render("Add", True, (255, 255, 255))
        add_text_rect = add_text.get_rect(center=add_button.center)
        screen.blit(add_text, add_text_rect)

        # SUB BUTTON
        pygame.draw.rect(screen, (80, 80, 80), sub_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), sub_button, 3, border_radius=10)

        sub_text = button_font.render("Sub", True, (255, 255, 255))
        sub_text_rect = sub_text.get_rect(center=sub_button.center)
        screen.blit(sub_text, sub_text_rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()