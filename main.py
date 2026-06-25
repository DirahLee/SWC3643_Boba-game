# main.py
import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from assets import ensure_assets
from game import GameManager

class GameRunner:
    def __init__(self):
        ensure_assets()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Boba Panic: Cosmic Café")
        self.game = GameManager(self.screen)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game.toggle_pause()
                    elif event.key == pygame.K_r:
                        self.game.reset_level()
                    elif event.key == pygame.K_RETURN:
                        if self.game.state == "win":
                            if self.game.level < 3:
                                self.game.start_next_level()
                            else:
                                self.game.exit_to_menu()
                        elif self.game.state == "lose":
                            self.game.reset_level()
                    elif event.key == pygame.K_l:
                        self.game.toggle_lang()
                    elif event.key == pygame.K_a:
                        self.game.auto_solve()
                    elif event.key == pygame.K_SPACE:
                        if self.game.state == "playing":
                            if not self.game.tray.start_crossing():
                                self.game.message = self.game.get_text("err_move")
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        if self.game.state == "playing":
                            self.game.toggle_entity(event.key - pygame.K_1)
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game.state == "menu":
                        self.game.btn_start.check_click(event.pos)
                        self.game.btn_levels.check_click(event.pos)
                        self.game.btn_controls.check_click(event.pos)
                        self.game.btn_exit.check_click(event.pos)
                    elif self.game.state == "level_select":
                        self.game.btn_lvl1.check_click(event.pos)
                        self.game.btn_lvl2.check_click(event.pos)
                        self.game.btn_lvl3.check_click(event.pos)
                        self.game.btn_back.check_click(event.pos)
                    elif self.game.state == "instructions":
                        self.game.btn_back.check_click(event.pos)
                    elif self.game.state in ["playing", "paused", "win", "lose"]:
                        self.game.btn_lang.check_click(event.pos)
                        self.game.btn_pause.check_click(event.pos)
                        self.game.btn_restart.check_click(event.pos)
                        self.game.btn_exit_menu.check_click(event.pos)
                    
            self.game.update()
            self.game.draw()
            pygame.display.flip()

if __name__ == "__main__":
    runner = GameRunner()
    runner.run()