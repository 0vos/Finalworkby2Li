import pygame
import time
import sys
from 样例.Lock import PasswordLock  # Ensure this exists

class LockScene:
    def __init__(self):
        from 样例.Lock import PasswordLock
        self.PasswordLock = PasswordLock

    def enter(self):
        print("进入解锁界面...")

        def is_prime(d):
            return d in [2, 3, 5, 7]

        def is_valid(pwd_digits, clues):
            d1, d2, d3 = pwd_digits
            for clue in clues:
                if len(clue) == 3:
                    for i in range(3):
                        if clue[i] != -1 and pwd_digits[i] != clue[i]:
                            return False
                elif len(clue) == 2:
                    if clue == [-1, -1]:
                        if not (is_prime(d1) and is_prime(d2) and is_prime(d3)):
                            return False
                        if len(set(pwd_digits)) != 3:
                            return False
                    else:
                        pos, kind = clue
                        digit = pwd_digits[pos - 1]
                        if kind == 0 and digit % 2 != 0:
                            return False
                        if kind == 1 and digit % 2 != 1:
                            return False
            return True

        def draw_gradient_background(surface, top_color, bottom_color):
            height = surface.get_height()
            for y in range(height):
                ratio = y / height
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

        def solve_visual(clues, target_hash):
            pygame.init()
            screen = pygame.display.set_mode((480, 320))
            pygame.display.set_caption("LockScene - Cracking Password...")
            font = pygame.font.SysFont(None, 32, bold=True)
            small_font = pygame.font.SysFont(None, 24)
            clock = pygame.time.Clock()

            lock = self.PasswordLock()
            result = []
            tries = [0]
            found = [False]
            coins = [0]

            def draw_status(path, status):
                draw_gradient_background(screen, (10, 10, 40), (25, 25, 70))
                info_rect = pygame.Surface((400, 100), pygame.SRCALPHA)
                info_rect.fill((0, 0, 0, 140))
                screen.blit(info_rect, (40, 80))
                try_text = font.render(f"Trying: {''.join(map(str, path))}", True, (230, 230, 230))
                status_text = font.render(status, True, (100, 255, 140))
                screen.blit(try_text, (60, 100))
                screen.blit(status_text, (60, 140))
                pygame.display.update()
                clock.tick(30)

            def dfs(pos, path):
                if found[0]:
                    return
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                if pos == 3:
                    if is_valid(path, clues):
                        tries[0] += 1
                        pwd_str = ''.join(map(str, path))
                        if lock.hash_password(pwd_str) == target_hash:
                            draw_status(path, f"  Password Found: {pwd_str}")
                            result.append(pwd_str)
                            found[0] = True
                            coins[0] += 100
                            time.sleep(2)
                        else:
                            coins[0] -= 1
                            draw_status(path, f"Attempt #{tries[0]} -> {pwd_str} ×")
                            time.sleep(0.2)
                    return
                for digit in range(10):
                    path.append(digit)
                    draw_status(path, "Searching...")
                    time.sleep(0.05)
                    dfs(pos + 1, path)
                    path.pop()

            dfs(0, [])

            draw_gradient_background(screen, (0, 30, 0), (0, 80, 0) if result else (80, 0, 0))
            info_rect = pygame.Surface((420, 120), pygame.SRCALPHA)
            info_rect.fill((0, 0, 0, 180))
            screen.blit(info_rect, (30, 90))

            if result:
                end_text = font.render(f" Success! Attempts: {tries[0]}, Coins: {coins[0]}", True, (180, 255, 180))
            else:
                end_text = font.render(f" Failed. Attempts: {tries[0]}, Coins: {coins[0]}", True, (255, 180, 180))
            screen.blit(end_text, (50, 120))

            hint_text = small_font.render("Press any key to exit...", True, (220, 220, 220))
            hint_rect = hint_text.get_rect(center=(240, 250))
            screen.blit(hint_text, hint_rect)
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False
            pygame.quit()
            return result, coins[0], tries[0]

        # 示例测试数据（可修改为读取）
        clues = [[5, -1, -1], [1, 1]]
        target_hash = self.PasswordLock().hash_password("528")
        solve_visual(clues, target_hash)
