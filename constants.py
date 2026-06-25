# constants.py
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 60
TIMER_SECONDS = 90
LEVEL_TIMERS = [90, 80, 70]
LEVEL_BACKGROUNDS = ["background.png"]
BOAT_IMAGE = "UFO.png"
METEOR_IMAGE = "meteor.png"
HEART_IMAGE = "heart.png"

# Palet Warna Tema Cosmic / Cyberpunk
COLOR_BG = (15, 15, 25)
COLOR_LEFT = (50, 20, 50)
COLOR_RIGHT = (20, 50, 50)
COLOR_STREAM = (0, 255, 200)
COLOR_TEXT = (236, 240, 241)
BTN_COLOR = (255, 0, 128)
BTN_HOVER = (200, 0, 100)
PANEL_COLOR = (25, 25, 35)

IMAGE_DIR = "assets/images"

# Definisi Entiti (Kini ditambah nama fail gambar .png)
ENTITY_DEFINITIONS = [
    {"name": "Chef Bobby", "label": "CHEF", "color": (255, 255, 255), "file": "chef_bobby.png"},
    {"name": "Space-Cow", "label": "COW", "color": (211, 84, 0), "file": "space_cow.png"},
    {"name": "Boba Pearls", "label": "BOBA", "color": (142, 68, 173), "file": "boba_pearls.png"},
    {"name": "Plasma Torch", "label": "TORCH", "color": (231, 76, 60), "file": "plasma_torch.png"}
]

DANGEROUS_PAIRS = [
    ("Space-Cow", "Boba Pearls"),
    ("Space-Cow", "Plasma Torch")
]