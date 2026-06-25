# button.py
import pygame
from constants import BTN_COLOR, BTN_HOVER, COLOR_TEXT

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface, font, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = BTN_HOVER if is_hover else BTN_COLOR
        
        # Kesan Glow/Border untuk tema Cyberpunk
        pygame.draw.rect(surface, (0,0,0), self.rect.inflate(4, 4), border_radius=10)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        text_surface = font.render(self.text, True, COLOR_TEXT)
        surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False