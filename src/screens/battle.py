import pygame
from src.cards.card import Card


class BattleScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 20)

        self.battlefield_rect = pygame.Rect(0, 0, 988, 550) # Battlefield Area
        self.card_rect = pygame.Rect(988, 0, 1280-988, 330) # Card Area
        self.graveyard_rect = pygame.Rect(988, 330, 1280-988, 330) # Graveyard Area
        self.next_rect = pygame.Rect(988, 660, 1280-988, 60) # Graveyard Area
        self.hand_rect = pygame.Rect(170, 550, 988-170, 170) # Hand Area
        self.avitar_rect = pygame.Rect(0, 550, 170, 170) # Avitar Area

        self.cards = [
            Card("Voldemort", 10),
            Card("AM-Wizard", 8),
            Card("SS-Animal", 11),
            Card("LC-Elf", 11),
            Card("JP-Giant", 11),
            Card("NP-Treant", 11),
            Card("KitKat", 9)
            
        ]

        for i, card in enumerate(self.cards):
            card.rect = pygame.Rect(200 + i * 110, 580, 100, 150)

    # 1280 x 720
    
    

    #def handle_mouse_click(self, event):
    #    if event.type == pygame.MOUSEBUTTONDOWN:
    #        if event.button == 1:
    #            print("Left Mouse Clicked")

    #def handle_event_print(self, event):
    #    if event.type == pygame.KEYDOWN:
    #        a = pygame.key.name(event.key)
    #        print (f"this {a} was clicked")


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Returning to menu screen")
                self.game.change_screen("menu")
        #self.handle_mouse_click(event)
        #self.handle_event_print(event)

    

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 110, 30))

        # Battlefield Area
        pygame.draw.rect(screen, (200, 50, 50), self.battlefield_rect) 
        text = self.font.render("Battle Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.battlefield_rect.center)
        screen.blit(text, text_rect)

        # Card Area
        pygame.draw.rect(screen, (0, 0, 255), self.card_rect) 
        text = self.font.render("Card Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.card_rect.center)
        screen.blit(text, text_rect)

        # Graveyard Area
        pygame.draw.rect(screen, (0, 255, 255), self.graveyard_rect)
        text = self.font.render("Graveyard Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.graveyard_rect.center)
        screen.blit(text, text_rect)


        # Next Area
        pygame.draw.rect(screen, (255, 255, 0), self.next_rect) 
        text = self.font.render("Next Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.next_rect.center)
        screen.blit(text, text_rect)

        # Hand Area
        pygame.draw.rect(screen, (55, 0, 150), self.hand_rect) 
        text = self.font.render("Hand Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.hand_rect.center)
        screen.blit(text, text_rect)

        # Avitar Area
        pygame.draw.rect(screen, (0, 100, 100), self.avitar_rect) 
        text = self.font.render("Avitar Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.avitar_rect.center)
        screen.blit(text, text_rect)

        #title_text = self.font.render("BATTLE SCREEN", True, (255, 255, 255))
        info_text = self.font.render("Press ESC to return to menu", True, (255, 255, 255))

        #screen.blit(title_text, (430, 250))
        screen.blit(info_text, (330, 350))

        for card in self.cards:
            pygame.draw.rect(screen, (220, 220, 220), card.rect)
            pygame.draw.rect(screen, (0, 0, 0), card.rect, 2)

            name_text = self.card_font.render(card.name, True, (0, 0, 0))
            name_rect = name_text.get_rect(center=card.rect.center)
            screen.blit(name_text, name_rect)