# game.py
import pygame
import sys
import random
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
        "no_lives": "Game Over! All shields depleted. Press ENTER to restart Level 1.",
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
        "win": "Pesanan Siap! ANDA MENANG SEMUA!",
        "timeout": "Masa Tamat! Pelanggan mengamuk!",
        "rule_boba": "Space-Cow makan Boba Pearls!",
        "rule_torch": "Space-Cow meletupkan dapur!",
        "err_move": "Perlu Chef Bobby untuk gerak!",
        "err_full": "Dulang penuh / silap tebing!",
        "lose_heart": "Tersentuh! Perisai rosak!",
        "no_lives": "Permainan Tamat! Semua nyawa habis. Tekan ENTER ke Tahap 1.",
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
            self.anomalies = [
                {"x": 340, "y": 150, "speed": 160, "direction": 1},
                {"x": 460, "y": 450, "speed": 190, "direction": -1}
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
            for anomaly in self.anomalies:
                anomaly["y"] += anomaly["speed"] * dt * anomaly["direction"]
                
                # Rigid containment constraints keeping anomalies safely inner-bound
                if anomaly["y"] <= 100:
                    anomaly["y"] = 100
                    anomaly["direction"] = 1
                elif anomaly["y"] >= 500:
                    anomaly["y"] = 500
                    anomaly["direction"] = -1
                
                if self.tray.rect.collidepoint(anomaly["x"], anomaly["y"]):
                    if self.invuln_timer <= 0:
                        anomaly["direction"] *= -1  # Instantly deflect course
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
            self.screen.fill(COLOR_BG)
            hint_txt = "Press [L] to Language | [F] to Fullscreen"
            self.screen.blit(self.ui_font.render(hint_txt, True, (0, 255, 200)), (20, 20))
            title = self.title_font.render(self.get_text("title"), True, (255, 0, 128))
            sub = self.font.render(self.get_text("subtitle"), True, (0, 255, 255))
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 110)))
            self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, 160)))
            self.btn_start.draw(self.screen, self.font, mouse_pos)
            self.btn_levels.draw(self.screen, self.font, mouse_pos)
            self.btn_controls.draw(self.screen, self.font, mouse_pos)
            self.btn_exit.draw(self.screen, self.font, mouse_pos)
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
            for anomaly in self.anomalies:
                pygame.draw.circle(self.screen, (150, 0, 255), (anomaly["x"], int(anomaly["y"])), 18)
                pygame.draw.circle(self.screen, (0, 255, 255), (anomaly["x"], int(anomaly["y"])), 22, 2)
            self.screen.blit(self.font.render(self.get_text("anomaly_warning"), True, (255, 0, 255)), (20, 560))

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
            
            if self.state == "win":
                breakdown_txt = f"Level Score: +{self.level_score}  |  Total Score: {self.total_score}"
                lbl_break = self.font.render(breakdown_txt, True, (255, 255, 0))
                self.screen.blit(lbl_break, lbl_break.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 5)))
                sub_lbl = self.font.render("Press 'ENTER' to Advance / Press 'P' to Resume", True, (0, 255, 255))
            elif self.state == "lose":
                sub_lbl = self.font.render("Press 'ENTER' to Restart", True, (255, 50, 50))

            self.screen.blit(sub_lbl, sub_lbl.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)))