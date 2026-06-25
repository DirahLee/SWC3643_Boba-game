# boat.py
from assets import load_image
from constants import BOAT_IMAGE

class HoverTray:
    def __init__(self, x, y, left_x, right_x):
        self.image = load_image(BOAT_IMAGE, size=(180, 90))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.left_x = left_x
        self.right_x = right_x
        
        self.side = 0 # 0 = Kiri, 1 = Kanan
        self.moving = False
        self.speed = 400
        self.target_x = x
        self.passengers = []

    def draw(self, surface):
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)

    def board(self, entity):
        if len(self.passengers) >= 2 or self.side != entity.side:
            return False
        entity.on_tray = True
        self.passengers.append(entity)
        return True

    def unboard(self, entity):
        if entity in self.passengers:
            entity.on_tray = False
            self.passengers.remove(entity)
            entity.side = self.side
            return True
        return False

    def can_move(self):
        return True

    def start_crossing(self):
        if not self.can_move() or self.moving:
            return False
        self.moving = True
        self.target_x = self.right_x if self.side == 0 else self.left_x
        return True

    def update(self, dt):
        if not self.moving:
            return False
            
        direction = 1 if self.target_x > self.x else -1
        self.x += self.speed * dt * direction
        
        if (direction > 0 and self.x >= self.target_x) or (direction < 0 and self.x <= self.target_x):
            self.x = self.target_x
            self.side = 1 - self.side
            self.moving = False
            for p in self.passengers:
                p.side = self.side
            return True
        return False