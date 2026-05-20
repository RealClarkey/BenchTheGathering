import pygame

'''
## Hero Card:
- Name
- Hero Type (Wizard, Nature, Tech, Neutral)
- Hit Points
- Pic (Image)
- Buffs (Icons)
- Abilities (description, attack damage, mana value)
- Evolution Abilities
'''

pygame.init()

width, height = 1536, 864

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Card Game Prototype")

clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)

# CARD SIZE 
card_h = 342  # 684
card_w = 246  # 492

ishani_img = pygame.image.load("new.png").convert_alpha()
ishani_img = pygame.transform.scale(ishani_img, (card_w, card_h))


def draw_card(x, y, image=None):
    if image:
        screen.blit(image, (x, y))
    else:
        pygame.draw.rect(screen, WHITE, (x, y, card_w, card_h), border_radius=12)
        pygame.draw.rect(screen, BLACK, (x, y, card_w, card_h), 3, border_radius=12)


running = True

while running:
    screen.fill((35, 35, 45))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- CENTERED 4 CARD LAYOUT ---
    gap = 40
    total_width = (card_w * 4) + (gap * 3)

    start_x = (width - total_width) // 2
    y = (height - card_h) // 2

    for i in range(4):
        x = start_x + i * (card_w + gap)

        if i == 0:
            draw_card(x, y, ishani_img)  # first card = image
        else:
            draw_card(x, y)  # others = blank

    pygame.display.flip()
    clock.tick(60)

pygame.quit()