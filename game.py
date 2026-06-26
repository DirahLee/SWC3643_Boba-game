# game.py
import pygame
import sys
import random
import math
from constants import *
from assets import load_image
from entity import Entity
from boat import HoverTray
from button import Button

LANG = {
    "EN": {
        "title": "BOBA PANIC: COSMIC CAFÉ",
        "subtitle": "Quantum River Crossing Adventure",
        "loading": "INITIALIZING CORE COFFEE SYSTEMS...",
        "msg_start": "Board Chef Bobby to start!",
        "btn_start": "START GAME (STAGE 1)",
        "btn_levels": "SELECT LEVEL",
        "btn_controls": "CONTROLS GUIDE",
        "btn_exit": "EXIT PROTOCOL",
        "btn_back": "RETURN TO MENU",
        "btn_lang": "Lang (L): EN",
        "btn_pause": "Pause (P)",
        "btn_restart": "Restart (R)",
        "btn_exit_menu": "EXIT MENU",
        "time": "Time",
        "score": "Score",
        "level": "Level",
        "hearts": "Hearts",
        "win": "Order Up! YOU WIN THE GAME!",
        "timeout": "Time's Up! Customers furious!",
        "rule_boba": "Space-Cow ate the Boba Pearls!",
        "rule_torch": "Space-Cow blew up the kitchen!",
        "err_move": "Need Chef Bobby to move tray!",
        "err_full": "Tray full or wrong side!",
        "lose_heart": "Crash! Shield damaged!",
        "no_lives": "Game Over! All shields depleted. Press ENTER to restart",
        "next_level": "Next level ready! Press ENTER to continue.",
        "restart_hint": "Press 'R' to retry.",
        "meteor_warning": "Level 2 hazard: Meteor rain!",
        "anomaly_warning": "Level 3 hazard: Quantum Anomalies!",
        "solution_title": "WINNING BLUEPRINT (Press 'A' to Auto-Solve):",
        "sol_1": "1. Cow to Right bank",
        "sol_2": "2. Chef returns empty",
        "sol_3": "3. Boba to Right, bring Cow back",
        "sol_4": "4. Torch to Right, Cow stays Left",
        "sol_5": "5. Chef returns empty",
        "sol_6": "6. Chef & Cow to Right -> Victory!",
        "instructions": [
            "MISSION: Move all assets safely to the Right Bank Counter.",
            "CRITICAL RULES:",
            "  -> Space-Cow cannot be left alone with Boba Pearls.",
            "  -> Space-Cow cannot be left alone with Plasma Torch.",
            "  -> The UFO tray needs Chef Bobby onboard to move.",
            "KEYBOARD MAP CONTROLS:",
            "  [1] - Board/Unboard CHEF BOBBY",
            "  [2] - Board/Unboard SPACE-COW",
            "  [3] - Board/Unboard BOBA PEARLS",
            "  [4] - Board/Unboard PLASMA TORCH",
            "  [SPACEBAR] - Launch the UFO across the stream",
            "  [A] - Auto-Solve Blueprint",
            "  [P] - Pause | [R] - Restart",
            "  [L] - Swap / Change Language",
            "  [F] - Toggle Fullscreen Mode"
        ]
    },
    "MY": {
        "title": "PANIK BOBA: KAFE KOSMIK",
        "subtitle": "Pengembaraan Menyeberang Sungai Kuantum",
        "loading": "MEMULAKAN SISTEM KAFE UTAMA...",
        "msg_start": "Naikkan Chef Bobby untuk mula!",
        "btn_start": "MULA TAHAP 1",
        "btn_levels": "PILIH TAHAP",
        "btn_controls": "PANDUAN KAWALAN",
        "btn_exit": "KELUAR SISTEM",
        "btn_back": "KEMBALI KE MENU",
        "btn_lang": "Bhs (L): MY",
        "btn_pause": "Jeda (P)",
        "btn_restart": "Mula Semula (R)",
        "btn_exit_menu": "KELUAR MENU",
        "time": "Masa",
        "score": "Markah",
        "level": "Tahap",
        "hearts": "Nyawa",
        "win": "Pesanan Siap! ANDA MENANG!",
        "timeout": "Masa Tamat! Pelanggan mengamuk!",
        "rule_boba": "Space-Cow makan Boba Pearls!",
        "rule_torch": "Space-Cow meletupkan dapur!",
        "err_move": "Perlu Chef Bobby untuk gerak!",
        "err_full": "Dulang penuh / silap tebing!",
        "lose_heart": "Tersentuh! Perisai rosak!",
        "no_lives": "Permainan Tamat! Semua nyawa habis. Tekan ENTER mula semula.",
        "next_level": "Tahap seterusnya sedia! Tekan ENTER.",
        "restart_hint": "Tekan 'R' to cuba lagi.",
        "meteor_warning": "Tahap 2: Hujan meteor aktif!",
        "anomaly_warning": "Tahap 3: Anomali Kuantum Bergerak!",
        "solution_title": "PELAN JAWAPAN (Tekan 'A' untuk Auto-Selesai):",
        "sol_1": "1. Bawa Lembu ke Kanan",
        "sol_2": "2. Chef pulang kosong",
        "sol_3": "3. Boba ke Kanan, bawa balik Lembu",
        "sol_4": "4. Torch ke Kanan, Lembu tinggal Kiri",
        "sol_5": "5. Chef pulang kosong",
        "sol_6": "6. Chef & Lembu ke Kanan -> Menang!",
        "instructions": [
            "MISI: Pindahkan semua aset ke Bank Kanan dengan selamat.",
            "PERATURAN KRITIKAL:",
            "  -> Space-Cow tidak boleh ditinggalkan dengan Boba Pearls.",
            "  -> Space-Cow tidak boleh ditinggalkan dengan Plasma Torch.",
            "  -> UFO tray perlukan Chef Bobby untuk bergerak.",
            "PAUTAN KAWALAN:",
            "  [1] - Naik/Turun CHEF BOBBY",
            "  [2] - Naik/Turun SPACE-COW",
            "  [3] - Naik/Turun BOBA PEARLS",
            "  [4] - Naik/Turun PLASMA TORCH",
            "  [SPACEBAR] - Lancarkan UFO melintasi sungai",
            "  [A] - Rangka kerja Auto-Selesai",
            "  [P] - Jeda | [R] - Mula Semula",
            "  [L] - Tukar / Ubah Bahasa",
            "  [F] - Skrin Penuh (Fullscreen)"
        ]
    }
}

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.lang_code = "EN"
        self.level = 1
        self.hearts = 3
        self.total_score = 0
        self.level_score = 0
        
        self.meteors = []
        self.meteor_spawn_timer = 0.0
        self.anomalies = []
        self.invuln_timer = 0.0  # Cooldown tracker to prevent machine-gun hit damage

        self.menu_time = 0.0
        self.menu_stars = [
            {"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT),
             "speed": random.uniform(0.2, 0.8), "size": random.randint(1, 3),
             "twinkle": random.uniform(0, 6.28)}
            for _ in range(60)
        ]

        self.state = "loading"
        self.loading_progress = 0
        
        pygame.font.init()
        self.title_font = pygame.font.SysFont("trebuchetms", 36, bold=True)
        self.font = pygame.font.SysFont("trebuchetms", 20, bold=True)
        self.btn_font = pygame.font.SysFont("trebuchetms", 12, bold=True)
        self.ui_font = pygame.font.SysFont("monospace", 13)

        self.bg_images = [load_image(path, size=(SCREEN_WIDTH, SCREEN_HEIGHT)) for path in LEVEL_BACKGROUNDS]
        self.heart_img = load_image(HEART_IMAGE, size=(24, 24))
        self.meteor_img = load_image(METEOR_IMAGE, size=(16, 16))

        self.reset(full_reset=True, loading=True)
        self.setup_buttons()

    def setup_buttons(self):
        self.btn_start = Button(pygame.Rect(362, 210, 300, 45), self.get_text("btn_start"), lambda: self.reset_to_play(1))
        self.btn_levels = Button(pygame.Rect(362, 270, 300, 45), self.get_text("btn_levels"), lambda: self.set_state("level_select"))
        self.btn_controls = Button(pygame.Rect(362, 330, 300, 45), self.get_text("btn_controls"), lambda: self.set_state("instructions"))
        self.btn_exit = Button(pygame.Rect(362, 390, 300, 45), self.get_text("btn_exit"), sys.exit)
        
        self.btn_back = Button(pygame.Rect(362, 510, 300, 45), self.get_text("btn_back"), lambda: self.set_state("menu"))

        self.btn_lvl1 = Button(pygame.Rect(362, 220, 300, 50), "STAGE 1: STARTER STREAM", lambda: self.reset_to_play(1))
        self.btn_lvl2 = Button(pygame.Rect(362, 290, 300, 50), "STAGE 2: METEOR SHOWER", lambda: self.reset_to_play(2))
        self.btn_lvl3 = Button(pygame.Rect(362, 360, 300, 50), "STAGE 3: QUANTUM ANOMALY", lambda: self.reset_to_play(3))

        self.btn_lang = Button(pygame.Rect(810, 430, 95, 35), self.get_text("btn_lang"), self.toggle_lang)
        self.btn_pause = Button(pygame.Rect(910, 430, 95, 35), self.get_text("btn_pause"), self.toggle_pause)
        self.btn_restart = Button(pygame.Rect(810, 470, 95, 35), self.get_text("btn_restart"), self.reset_level)
        self.btn_exit_menu = Button(pygame.Rect(910, 470, 95, 35), self.get_text("btn_exit_menu"), self.exit_to_menu)

    def set_state(self, new_state):
        self.state = new_state
        self.setup_buttons()

    def get_text(self, key):
        return LANG[self.lang_code].get(key, "")

    def reset(self, full_reset=True, loading=False, targeted_level=1):
        if full_reset:
            self.level = targeted_level
            self.total_score = 0
        
        self.hearts = 3
        self.timer = LEVEL_TIMERS[min(self.level - 1, len(LEVEL_TIMERS)-1)]
        self.moves = 0
        self.level_score = 0
        self.message = self.get_text("msg_start")
        self.meteors.clear()
        self.anomalies.clear()
        self.meteor_spawn_timer = 0.0
        self.invuln_timer = 0.0

        if self.level == 3:
            # Orbital anomalies: two portals circling a centre point with a safe/danger phase cycle
            self.anomalies = [
                {"cx": 400, "cy": 310, "radius": 110, "angle": 0.0,
                 "speed": 0.7, "x": 510.0, "y": 310.0, "phase_timer": 0.0},
                {"cx": 400, "cy": 310, "radius": 70, "angle": math.pi,
                 "speed": -1.0, "x": 330.0, "y": 310.0, "phase_timer": 2.5},
            ]

        self.left_bank_positions = [(60, 180), (150, 180), (60, 300), (150, 300)]
        self.right_bank_positions = [(650, 180), (740, 180), (650, 300), (740, 300)]
        
        self.entities = [Entity(defn, i) for i, defn in enumerate(ENTITY_DEFINITIONS)]
        self.tray = HoverTray(x=260, y=450, left_x=260, right_x=540)
        
        if loading:
            self.state = "loading"
            self.loading_progress = 0

    def reset_to_play(self, target_level=1):
        self.level = target_level
        self.reset(full_reset=True, targeted_level=target_level)
        self.state = "playing"

    def reset_level(self):
        if self.hearts <= 0:
            self.reset(full_reset=True, targeted_level=1)
        else:
            self.reset(full_reset=False, targeted_level=self.level)
        self.state = "playing"

    def start_next_level(self):
        if self.level < 3:
            self.level += 1
        self.reset(full_reset=False, targeted_level=self.level)
        self.state = "playing"
        self.message = self.get_text("msg_start")

    def exit_to_menu(self):
        self.state = "menu"
        self.reset(full_reset=True, targeted_level=1)

    def toggle_lang(self):
        self.lang_code = "MY" if self.lang_code == "EN" else "EN"
        self.setup_buttons()
        if self.state in ["playing", "menu", "instructions", "level_select"]:
            self.message = self.get_text("msg_start")

    def toggle_pause(self):
        if self.state == "playing":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "playing"

    def toggle_entity(self, index):
        if self.state != "playing" or self.tray.moving:
            return
        ent = self.entities[index]
        if ent.on_tray:
            self.tray.unboard(ent)
        else:
            if not self.tray.board(ent):
                self.message = self.get_text("err_full")

    def auto_solve(self):
        if self.state != "playing" or self.tray.moving:
            return
        chef, cow, boba, torch = self.entities[0], self.entities[1], self.entities[2], self.entities[3]

        if chef.side == 0 and cow.side == 0 and boba.side == 0 and torch.side == 0:
            if not cow.on_tray: self.tray.board(cow)
            if not chef.on_tray: self.tray.board(chef)
            self.tray.start_crossing()
        elif self.tray.side == 1 and cow.on_tray and chef.on_tray:
            self.tray.unboard(cow)
            self.tray.start_crossing()
        elif self.tray.side == 0 and chef.on_tray and boba.side == 0:
            self.tray.board(boba)
            self.tray.start_crossing()
        elif self.tray.side == 1 and boba.on_tray and cow.side == 1:
            self.tray.unboard(boba)
            self.tray.board(cow)
            self.tray.start_crossing()
        elif self.tray.side == 0 and cow.on_tray and torch.side == 0:
            self.tray.unboard(cow)
            self.tray.board(torch)
            self.tray.start_crossing()
        elif self.tray.side == 1 and torch.on_tray and boba.side == 1:
            self.tray.unboard(torch)
            self.tray.start_crossing()
        elif self.tray.side == 0 and chef.side == 0 and cow.side == 0:
            if not chef.on_tray: self.tray.board(chef)
            elif not cow.on_tray:
                self.tray.board(cow)
                self.tray.start_crossing()
        elif self.tray.side == 1 and cow.on_tray and chef.on_tray:
            self.tray.unboard(cow)
            self.tray.unboard(chef)

    def lose_life(self, message_key):
        if self.invuln_timer > 0:
            return  # Immune during temporary cooldown
        
        self.hearts -= 1
        if self.hearts <= 0:
            self.hearts = 0
            self.state = "lose"
            self.message = self.get_text("no_lives")
        else:
            self.message = self.get_text(message_key)
            self.invuln_timer = 1.2  # 1.2 seconds of protection frames

    def spawn_meteor(self):
        x = random.randint(240, 560)
        y = -40
        self.meteors.append({"x": x, "y": y, "speed": random.uniform(220, 360)})

    def calculate_score(self):
        time_bonus = int(self.timer) * 100
        move_penalty = self.moves * 50
        heart_bonus = self.hearts * 500
        return max(0, time_bonus - move_penalty + heart_bonus)

    def check_rules(self):
        if self.tray.moving:
            return

        left_bank = [e.name for e in self.entities if e.side == 0 and not e.on_tray]
        right_bank = [e.name for e in self.entities if e.side == 1 and not e.on_tray]

        for bank in (left_bank, right_bank):
            if "Space-Cow" in bank and "Boba Pearls" in bank and "Chef Bobby" not in bank:
                self.hearts = 0
                self.lose_life("rule_boba")
                return
            if "Space-Cow" in bank and "Plasma Torch" in bank and "Chef Bobby" not in bank:
                self.hearts = 0
                self.lose_life("rule_torch")
                return

        if all(e.side == 1 and not e.on_tray for e in self.entities):
            self.level_score = self.calculate_score()
            self.total_score += self.level_score
            self.state = "win"
            if self.level < 3:
                self.message = self.get_text("next_level")
            else:
                self.message = self.get_text("win")

    def update(self):
        dt = 1 / FPS
        if self.state == "loading":
            self.loading_progress += 1.5
            if self.loading_progress >= 100:
                self.state = "menu"
            return

        if self.state == "menu":
            self.menu_time += dt
            for star in self.menu_stars:
                star["y"] = (star["y"] + star["speed"]) % SCREEN_HEIGHT
            return

        if self.state != "playing":
            return

        if self.invuln_timer > 0:
            self.invuln_timer -= dt

        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0
            self.hearts = 0
            self.lose_life("timeout")
            return

        was_moving = self.tray.moving
        self.tray.update(dt)
        if was_moving and not self.tray.moving:
            self.moves += 1

        for e in self.entities:
            positions = self.right_bank_positions if e.side == 1 else self.left_bank_positions
            e.update_position(self.tray, positions)

        if self.level == 2:
            self.meteor_spawn_timer -= dt
            if self.meteor_spawn_timer <= 0:
                self.spawn_meteor()
                self.meteor_spawn_timer = 1.5

            for meteor in list(self.meteors):
                meteor["y"] += meteor["speed"] * dt
                if meteor["y"] > SCREEN_HEIGHT + 20:
                    self.meteors.remove(meteor)
                elif self.tray.rect.collidepoint(meteor["x"], meteor["y"]):
                    self.meteors.remove(meteor)
                    self.lose_life("lose_heart")

        elif self.level == 3:
            PHASE_CYCLE = 5.0   # 2s safe + 3s danger per cycle
            SAFE_WINDOW = 2.0
            for anomaly in self.anomalies:
                anomaly["angle"] += anomaly["speed"] * dt
                anomaly["phase_timer"] = (anomaly["phase_timer"] + dt) % PHASE_CYCLE
                anomaly["x"] = anomaly["cx"] + math.cos(anomaly["angle"]) * anomaly["radius"]
                anomaly["y"] = anomaly["cy"] + math.sin(anomaly["angle"]) * anomaly["radius"]

                is_safe = anomaly["phase_timer"] < SAFE_WINDOW
                if not is_safe and self.tray.rect.collidepoint(anomaly["x"], anomaly["y"]):
                    if self.invuln_timer <= 0:
                        self.lose_life("lose_heart")

        self.check_rules()

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == "loading":
            self.screen.fill((10, 10, 20))
            lbl_title = self.title_font.render(self.get_text("title"), True, (0, 255, 255))
            self.screen.blit(lbl_title, lbl_title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)))
            lbl_load = self.font.render(self.get_text("loading"), True, (255, 0, 128))
            self.screen.blit(lbl_load, lbl_load.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            pygame.draw.rect(self.screen, (50, 50, 70), (262, SCREEN_HEIGHT//2 + 40, 500, 20), border_radius=5)
            pygame.draw.rect(self.screen, (0, 255, 200), (262, SCREEN_HEIGHT//2 + 40, int(5 * self.loading_progress), 20), border_radius=5)
            return

        if self.state == "menu":
            # Starfield background
            if self.bg_images:
                self.screen.blit(self.bg_images[0], (0, 0))
            else:
                self.screen.fill(COLOR_BG)

            # Dark overlay for depth
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 5, 20, 140))
            self.screen.blit(overlay, (0, 0))

            t = self.menu_time

            # Animated twinkling star particles
            for star in self.menu_stars:
                twinkle = (math.sin(t * 3.0 + star["twinkle"]) + 1) / 2
                brightness = int(100 + 155 * twinkle)
                pygame.draw.circle(self.screen, (brightness, brightness, brightness),
                                   (int(star["x"]), int(star["y"])), star["size"])

            # Left energy column — floating cyan boba orbs
            for i in range(5):
                bob_y = 215 + i * 62 + int(math.sin(t * 1.2 + i * 0.8) * 18)
                glow_a = max(0, int(80 + 80 * math.sin(t * 2.0 + i)))
                gs = pygame.Surface((36, 36), pygame.SRCALPHA)
                pygame.draw.circle(gs, (0, 180, 255, glow_a), (18, 18), 14)
                self.screen.blit(gs, (73, bob_y - 18))
                pygame.draw.circle(self.screen, (0, 200, 255), (91, bob_y), 6)
                if i < 4:
                    next_y = 215 + (i + 1) * 62 + int(math.sin(t * 1.2 + (i + 1) * 0.8) * 18)
                    pygame.draw.line(self.screen, (0, 80, 130), (91, bob_y + 7), (91, next_y - 7), 1)

            # Right energy column — floating pink boba orbs
            for i in range(5):
                bob_y = 215 + i * 62 + int(math.sin(t * 1.4 + i * 0.9 + 1.6) * 18)
                glow_a = max(0, int(80 + 80 * math.sin(t * 2.2 + i + 1)))
                gs = pygame.Surface((36, 36), pygame.SRCALPHA)
                pygame.draw.circle(gs, (255, 0, 128, glow_a), (18, 18), 14)
                self.screen.blit(gs, (SCREEN_WIDTH - 109, bob_y - 18))
                pygame.draw.circle(self.screen, (255, 0, 150), (SCREEN_WIDTH - 91, bob_y), 6)
                if i < 4:
                    next_y = 215 + (i + 1) * 62 + int(math.sin(t * 1.4 + (i + 1) * 0.9 + 1.6) * 18)
                    pygame.draw.line(self.screen, (120, 0, 60), (SCREEN_WIDTH - 91, bob_y + 7), (SCREEN_WIDTH - 91, next_y - 7), 1)

            # Orbiting boba pearls around the title band
            orbit_cx, orbit_cy = SCREEN_WIDTH // 2, 118
            for i in range(6):
                angle = t * 0.55 + i * (math.pi * 2 / 6)
                ox = orbit_cx + math.cos(angle) * 308
                oy = orbit_cy + math.sin(angle) * 28
                size = 5 if i % 2 == 0 else 3
                color = (255, 0, 128) if i % 2 == 0 else (0, 255, 200)
                pygame.draw.circle(self.screen, color, (int(ox), int(oy)), size)

            # Neon title panel
            panel_w, panel_h = 684, 76
            panel_x = SCREEN_WIDTH // 2 - panel_w // 2
            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((255, 0, 128, 18))
            pygame.draw.rect(panel_surf, (255, 0, 128, 210), (0, 0, panel_w, panel_h), 2, border_radius=12)
            pygame.draw.rect(panel_surf, (255, 0, 128, 60), (4, 4, panel_w - 8, panel_h - 8), 1, border_radius=9)
            self.screen.blit(panel_surf, (panel_x, 82))

            # Title glow shadow (4 directions)
            for dx, dy in [(-3, 0), (3, 0), (0, -2), (0, 3)]:
                shadow = self.title_font.render(self.get_text("title"), True, (110, 0, 55))
                self.screen.blit(shadow, shadow.get_rect(center=(SCREEN_WIDTH // 2 + dx, 118 + dy)))

            # Title main text
            title = self.title_font.render(self.get_text("title"), True, (255, 0, 128))
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 118)))

            # Subtitle with pulsing colour
            pulse = (math.sin(t * 2.5) + 1) / 2
            sub_color = (int(pulse * 60), int(190 + pulse * 65), 255)
            sub = self.font.render(self.get_text("subtitle"), True, sub_color)
            self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 163)))

            # Animated separator line
            sep_a = int(70 + 60 * math.sin(t * 1.8))
            sep_surf = pygame.Surface((520, 2), pygame.SRCALPHA)
            sep_surf.fill((0, 255, 200, sep_a))
            self.screen.blit(sep_surf, (SCREEN_WIDTH // 2 - 260, 183))

            # Buttons
            self.btn_start.draw(self.screen, self.font, mouse_pos)
            self.btn_levels.draw(self.screen, self.font, mouse_pos)
            self.btn_controls.draw(self.screen, self.font, mouse_pos)
            self.btn_exit.draw(self.screen, self.font, mouse_pos)

            # Hint text at bottom-centre
            hint_txt = "Press [L] to Language | [F] to Fullscreen"
            hint_surf = self.ui_font.render(hint_txt, True, (0, 255, 200))
            self.screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))
            return

        if self.state == "level_select":
            self.screen.fill(COLOR_BG)
            title = self.title_font.render("CHOOSE SECTOR TIMELINE", True, (255, 0, 128))
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 110)))
            self.btn_lvl1.draw(self.screen, self.font, mouse_pos)
            self.btn_lvl2.draw(self.screen, self.font, mouse_pos)
            self.btn_lvl3.draw(self.screen, self.font, mouse_pos)
            self.btn_back.draw(self.screen, self.font, mouse_pos)
            return

        if self.state == "instructions":
            self.screen.fill(COLOR_BG)
            title = self.title_font.render(self.get_text("btn_controls"), True, (0, 255, 255))
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))
            guidelines = LANG[self.lang_code].get("instructions", [])
            y_offset = 140
            for line in guidelines:
                color = (0, 255, 200) if "->" in line or "[" in line or line.endswith(":") else COLOR_TEXT
                self.screen.blit(self.ui_font.render(line, True, color), (150, y_offset))
                y_offset += 24
            self.btn_back.draw(self.screen, self.font, mouse_pos)
            return

        background = self.bg_images[0] if self.bg_images else None
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(COLOR_BG)

        # Draw tray with blinking transparency effect when invulnerable
        if self.invuln_timer > 0 and int(self.invuln_timer * 10) % 2 == 0:
            pass 
        else:
            self.tray.draw(self.screen)

        if self.level == 2:
            for meteor in self.meteors:
                self.screen.blit(self.meteor_img, self.meteor_img.get_rect(center=(meteor["x"], meteor["y"])))
            self.screen.blit(self.font.render(self.get_text("meteor_warning"), True, (255, 255, 0)), (20, 560))
        elif self.level == 3:
            PHASE_CYCLE = 5.0
            SAFE_WINDOW = 2.0
            gt = pygame.time.get_ticks() / 1000.0

            # Subtle orbit path guide rings
            for anomaly in self.anomalies:
                r = int(anomaly["radius"])
                orbit_surf = pygame.Surface((r * 2 + 6, r * 2 + 6), pygame.SRCALPHA)
                pygame.draw.circle(orbit_surf, (60, 0, 120, 55), (r + 3, r + 3), r, 1)
                self.screen.blit(orbit_surf, (int(anomaly["cx"]) - r - 3, int(anomaly["cy"]) - r - 3))

            # Draw each anomaly with phase-aware visuals
            for anomaly in self.anomalies:
                pt = anomaly["phase_timer"]
                is_safe = pt < SAFE_WINDOW
                ax, ay = int(anomaly["x"]), int(anomaly["y"])

                if is_safe:
                    # Ghost state — faded, harmless
                    fade_a = int(35 + 40 * abs(math.sin(pt * math.pi / SAFE_WINDOW)))
                    ghost = pygame.Surface((60, 60), pygame.SRCALPHA)
                    pygame.draw.circle(ghost, (150, 0, 255, fade_a), (30, 30), 18)
                    pygame.draw.circle(ghost, (0, 255, 255, fade_a + 25), (30, 30), 23, 3)
                    self.screen.blit(ghost, (ax - 30, ay - 30))
                else:
                    # Active danger — pulsing solid portal
                    dp = int(130 + 80 * math.sin(gt * 6))
                    pygame.draw.circle(self.screen, (dp, 0, 255), (ax, ay), 18)
                    pygame.draw.circle(self.screen, (0, 255, 255), (ax, ay), 23, 3)
                    # Rotating spark ring
                    for s in range(4):
                        sa = gt * 4.0 + s * math.pi / 2
                        sx = ax + int(math.cos(sa) * 29)
                        sy = ay + int(math.sin(sa) * 29)
                        pygame.draw.circle(self.screen, (255, 80, 255), (sx, sy), 3)

            # Phase status HUD bar
            if self.anomalies:
                pt = self.anomalies[0]["phase_timer"]
                is_safe = pt < SAFE_WINDOW
                bar_color = (0, 230, 80) if is_safe else (255, 60, 60)
                status_txt = "QUANTUM PHASE: SAFE — CROSS NOW!" if is_safe else "QUANTUM PHASE: UNSTABLE — WAIT!"
                status_bg = pygame.Rect(12, 557, 560, 34)
                pygame.draw.rect(self.screen, (0, 0, 0), status_bg, border_radius=6)
                pygame.draw.rect(self.screen, bar_color, status_bg, 2, border_radius=6)
                status_surf = self.font.render(status_txt, True, bar_color)
                self.screen.blit(status_surf, status_surf.get_rect(center=status_bg.center))

        for e in self.entities:
            e.draw(self.screen)

        pygame.draw.rect(self.screen, PANEL_COLOR, (800, 0, 224, 600))
        self.screen.blit(self.title_font.render("COSMIC", True, (0, 255, 255)), (810, 50))
        
        time_color = (255, 50, 50) if self.timer < 10 else COLOR_TEXT
        self.screen.blit(self.font.render(f"{self.get_text('time')}: {int(self.timer)}s", True, time_color), (810, 110))
        self.screen.blit(self.font.render(f"{self.get_text('level')}: {self.level}", True, COLOR_TEXT), (810, 140))
        self.screen.blit(self.font.render(f"{self.get_text('hearts')}:", True, COLOR_TEXT), (810, 170))
        for i in range(self.hearts):
            self.screen.blit(self.heart_img, (900 + i * 28, 168))

        display_score = self.total_score + (self.calculate_score() if self.state == "win" else 0)
        self.screen.blit(self.font.render(f"{self.get_text('score')}: {display_score}", True, (255, 255, 0)), (810, 210))
        self.screen.blit(self.font.render(f"Status: {self.state.upper()}", True, COLOR_TEXT), (810, 240))
        
        msg_bg = pygame.Rect(20, 20, 760, 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), msg_bg, border_radius=10)
        msg_surf = self.font.render(self.message, True, (255, 255, 0))
        self.screen.blit(msg_surf, msg_surf.get_rect(center=msg_bg.center))

        sol_y = 270
        self.screen.blit(self.ui_font.render(self.get_text("solution_title"), True, (0, 255, 200)), (810, sol_y))
        for i in range(1, 7):
            sol_y += 18
            self.screen.blit(self.ui_font.render(self.get_text(f"sol_{i}"), True, (170, 180, 200)), (810, sol_y))

        self.btn_lang.draw(self.screen, self.btn_font, mouse_pos)
        self.btn_pause.draw(self.screen, self.btn_font, mouse_pos)
        self.btn_restart.draw(self.screen, self.btn_font, mouse_pos)
        self.btn_exit_menu.draw(self.screen, self.btn_font, mouse_pos)

        if self.state in ["paused", "win", "lose"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            end_lbl = self.title_font.render(self.message, True, (255, 255, 255))
            self.screen.blit(end_lbl, end_lbl.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
            
            if self.state == "paused":
                sub_lbl = self.font.render("Press 'P' to Resume", True, (0, 255, 200))
            elif self.state == "win":
                breakdown_txt = f"Level Score: +{self.level_score}  |  Total Score: {self.total_score}"
                lbl_break = self.font.render(breakdown_txt, True, (255, 255, 0))
                self.screen.blit(lbl_break, lbl_break.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 5)))
                sub_lbl = self.font.render("Press 'ENTER' to Advance", True, (0, 255, 255))
            elif self.state == "lose":
                sub_lbl = self.font.render("Press 'ENTER' to Restart", True, (255, 50, 50))

            self.screen.blit(sub_lbl, sub_lbl.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)))