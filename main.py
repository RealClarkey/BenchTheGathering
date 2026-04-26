import pygame

# Initialise pygame
pygame.init()

# Create window (width, height)
screen = pygame.display.set_mode((800, 400))

# Optional: set window title
pygame.display.set_caption("My Game")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with a colour (RGB)
    screen.fill((30, 30, 30))

    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()