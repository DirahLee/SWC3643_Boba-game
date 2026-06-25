# assets.py
import os
import pygame
import random
from constants import IMAGE_DIR, ENTITY_DEFINITIONS, LEVEL_BACKGROUNDS, BOAT_IMAGE, METEOR_IMAGE, HEART_IMAGE


def ensure_directories():
    os.makedirs(IMAGE_DIR, exist_ok=True)


def generate_ufo(filename):
    surface = pygame.Surface((180, 90), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (40, 40, 80), (0, 15, 180, 65))
    pygame.draw.ellipse(surface, (0, 255, 255), (5, 20, 170, 55), 3)
    pygame.draw.ellipse(surface, (90, 120, 180), (20, 35, 140, 30))
    for idx in range(6):
        pygame.draw.circle(surface, (0, 180, 255), (28 + idx * 24, 52), 6)
    pygame.image.save(surface, filename)


def generate_meteor(filename):
    # Decreased surface size to 16x16 and adjusted vector shapes to fit proportionally
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 120, 0), (8, 8), 7)
    pygame.draw.circle(surface, (255, 200, 50), (6, 6), 4)
    pygame.draw.polygon(surface, (255, 140, 0), [(0, 6), (5, 8), (0, 11)])
    pygame.image.save(surface, filename)


def generate_heart(filename):
    surface = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.polygon(surface, (240, 60, 120), [(12, 22), (2, 10), (6, 4), (12, 8), (18, 4), (22, 10)])
    pygame.draw.circle(surface, (240, 60, 120), (8, 8), 6)
    pygame.draw.circle(surface, (240, 60, 120), (16, 8), 6)
    pygame.image.save(surface, filename)


def generate_background(filename, theme_index):
    surface = pygame.Surface((1024, 1200))
    gradients = [
        ((10, 10, 35), (30, 5, 70)),
        ((8, 20, 50), (10, 70, 110)),
        ((15, 12, 30), (85, 25, 65))
    ]
    top_color, bottom_color = gradients[theme_index % len(gradients)]
    for y in range(1200):
        ratio = y / 1199
        color = (
            int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
            int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
            int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        )
        pygame.draw.line(surface, color, (0, y), (1023, y))
    for _ in range(120):
        x = random.randint(0, 1023)
        y = random.randint(0, 1199)
        radius = random.randint(1, 2)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), radius)
    pygame.image.save(surface, filename)


def generate_entity_image(definition, filename):
    surface = pygame.Surface((70, 70), pygame.SRCALPHA)
    pygame.draw.circle(surface, definition["color"], (35, 30), 28)
    pygame.draw.rect(surface, (255, 255, 255), (8, 42, 54, 20), border_radius=8)
    pygame.font.init()
    font = pygame.font.SysFont("arial", 11, bold=True)
    text = font.render(definition["label"], True, (0, 0, 0))
    surface.blit(text, text.get_rect(center=(35, 52)))
    pygame.image.save(surface, filename)


def ensure_assets():
    pygame.init()
    ensure_directories()
    generators = []
    generators.append((BOAT_IMAGE, generate_ufo))
    generators.append((METEOR_IMAGE, generate_meteor))
    generators.append((HEART_IMAGE, generate_heart))
    for idx, bg_name in enumerate(LEVEL_BACKGROUNDS):
        generators.append((bg_name, lambda fn, idx=idx: generate_background(fn, idx)))
    for definition in ENTITY_DEFINITIONS:
        generators.append((definition["file"], lambda fn, definition=definition: generate_entity_image(definition, fn)))

    for name, generate in generators:
        path = os.path.join(IMAGE_DIR, name)
        if not os.path.exists(path):
            try:
                generate(path)
            except Exception as e:
                print(f"Failed to generate asset {path}: {e}")


def load_image(name, size=None):
    paths_to_try = [os.path.join(IMAGE_DIR, name), name]

    image = None
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                image = pygame.image.load(path).convert_alpha()
                break
            except Exception as e:
                print(f"Ralat membaca fail {path}: {e}")

    if image is None:
        print(f"Amaran: Tidak dapat memuatkan gambar '{name}'!")
        surf = pygame.Surface(size if size else (70, 70), pygame.SRCALPHA)
        surf.fill((255, 0, 0))
        return surf

    if size:
        image = pygame.transform.smoothscale(image, size)
    return image