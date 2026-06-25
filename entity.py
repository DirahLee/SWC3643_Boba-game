# entity.py
import pygame
from assets import load_image

class Entity:
    def __init__(self, definition, index):
        self.name = definition["name"]
        self.filename = definition["file"]
        self.color = definition.get("color", (255, 255, 255))
        
        self.image = load_image(self.filename, size=(70, 70))
        self.rect = self.image.get_rect()
        
        self.side = 0 # 0 = Kiri, 1 = Kanan
        self.on_tray = False
        self.index = index

        pygame.font.init()
        self.label_font = pygame.font.SysFont("trebuchetms", 11, bold=True)

    def draw(self, surface):
        frame_rect = self.rect.inflate(6, 6)
        pygame.draw.rect(surface, self.color, frame_rect, 2, border_radius=8)
        
        surface.blit(self.image, self.rect)

        text_surf = self.label_font.render(self.name.upper(), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 12))
        
        pill_bg = text_rect.inflate(10, 4)
        pygame.draw.rect(surface, (15, 15, 25), pill_bg, border_radius=4)
        pygame.draw.rect(surface, self.color, pill_bg, 1, border_radius=4)
        
        surface.blit(text_surf, text_rect)

    def update_position(self, tray, positions):
        if self.on_tray:
            if self in tray.passengers:
                p_idx = tray.passengers.index(self)
                # Centers characters nicely inside the smaller UFO cockpit
                offset_x = -32 if p_idx == 0 else 32
                self.rect.center = (tray.x + offset_x, tray.y - 12)
        else:
            self.rect.center = positions[self.index]