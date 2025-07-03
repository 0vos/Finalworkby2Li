from three采用贪心算法设计实时资源拾取策略 import explore_and_collect, bfs_to_exit
from four采用回溯法解谜关卡 import solve_with_backtracking
from five import min_turns_to_defeat
from 输入输出 import load_data_from_json
import pygame
import time
import copy

resource_value = 0

# 初始化
pygame.init()
width, height = 480, 480
screen = pygame.display.set_mode((width, height + 24))  # 加高顶部
tile_size = 32  # 每个图片的宽高像素

# 加载图块图片
the_images = {
    '#': pygame.image.load("img/wall.png"),
    ' ': pygame.image.load("img/floor.png"),
    'S': pygame.image.load("img/floor.png"),
    'E': pygame.image.load("img/floor.png"),
    'T': pygame.image.load("img/trap.png"),
    'G': pygame.image.load("img/gold.png"),
    'B': pygame.image.load("img/boss.png"),
    'L': pygame.image.load("img/lock.png"),
    'P': pygame.image.load("img/player.png")
}

class MazeScene:
    def __init__(self, maze, images):
        self.maze = maze
        self.images = images

    def render_maze(self):
        # 渲染迷宫
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                image = self.images.get(cell, self.images[' '])  # 默认用 floor
                screen.blit(image, (col_idx * tile_size, row_idx * tile_size + 24))
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, width, 24))
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Gold: {resource_value}", True, (255, 255, 0))
        screen.blit(text, (width - 120, 2))

    def update_cell(self, pos, value):
        self.maze[pos[0]][pos[1]] = value

class Character:
    def __init__(self, images):
        self.images = images

    def paint_character(self, pos):
        # 玩家绘制
        screen.blit(self.images['P'], (pos[1] * tile_size, pos[0] * tile_size + 24))

    def walk_path(self, maze_scene, path, file_name, five_result):
        global resource_value
        for idx, pos in enumerate(path):
            pygame.event.pump()
            maze_scene.render_maze()
            self.paint_character(pos)
            pygame.display.update()
            time.sleep(0.3)

            cell = maze_scene.maze[pos[0]][pos[1]]
            if cell == 'G':
                maze_scene.update_cell(pos, ' ')
                resource_value += 50
            elif cell == 'T':
                maze_scene.update_cell(pos, ' ')
                resource_value -= 30
            elif cell == 'L':
                LockScene().enter(file_name)
                maze_scene.update_cell(pos, ' ')  # 解锁完成
            elif cell == 'B':
                BossScene(five_result).enter()
                maze_scene.update_cell(pos, ' ')  # 打Boss完成
            elif cell == 'E':
                EndScene().enter()
                return

class LockScene:
    def __init__(self):
        from 样例.Lock import PasswordLock
        self.PasswordLock = PasswordLock

    def enter(self, file_name):
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
            screen = pygame.display.set_mode((480, 480))
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
                        pygame.display.quit()  # 仅关闭解锁界面窗口
                        return
                if pos == 3:
                    if is_valid(path, clues):
                        tries[0] += 1
                        pwd_str = ''.join(map(str, path))
                        if lock.hash_password(pwd_str) == target_hash:
                            draw_status(path, f"  Password Found: {pwd_str}")
                            result.append(pwd_str)
                            found[0] = True
                            coins[0] += 0
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

            hint_text = small_font.render("Press [z] to exit...", True, (220, 220, 220))
            hint_rect = hint_text.get_rect(center=(240, 250))
            screen.blit(hint_text, hint_rect)
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            waiting = False
            # pygame.display.quit()
            return result, coins[0], tries[0]

        # 示例测试数据（可修改为读取）
        clues = load_data_from_json(file_name, "C")
        target_hash = load_data_from_json(file_name, "L")
        result, coins, tries = solve_visual(clues, target_hash)
        global resource_value
        resource_value -= tries  # 每次尝试扣 1

class BossScene:
    def __init__(self, five_result):
        # 示例数据
        self.boss_hp = five_result['B']
        self.player_skills = five_result['PlayerSkills']
        self.min_turns = five_result['min_turns']
        self.actions = five_result['actions']
        self.cooldowns = [0] * len(self.player_skills)
        self.font = pygame.font.SysFont(None, 24)

    def draw_bar(self, x, y, width, height, percent, color):
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
        pygame.draw.rect(screen, color, (x, y, int(width * percent), height))

    def enter(self):
        print("进入Boss战界面...")
        clock = pygame.time.Clock()
        boss_imgs = [pygame.image.load("img/big_boss.png") for _ in self.boss_hp]
        player_img = pygame.image.load("img/player_back.png")
        current_boss = 0

        for turn, skill_id in enumerate(self.actions):
            screen.fill((0, 0, 0))

            # 显示当前回合数
            turn_text = self.font.render(f"Turn {turn}", True, (255, 255, 0))
            screen.blit(turn_text, (width - 160, 10))

            # 绘制Boss
            for i, hp in enumerate(self.boss_hp):
                x = 50 + i * 100
                screen.blit(boss_imgs[i], (x, 50))
                self.draw_bar(x, 128, 64, 10, self.boss_hp[i] / [11,13,9,15][i], (255, 0, 0))

            # 绘制玩家
            screen.blit(player_img, (width//2 - 32, 300))

            # 绘制技能冷却
            for i, cd in enumerate(self.cooldowns):
                x = 50 + i * 100
                bar_y = 400
                # 绘制技能标签
                skill_label = self.font.render(f"Skill{i+1}", True, (255, 255, 255))
                screen.blit(skill_label, (x, bar_y - 20))
                cd_percent = cd / self.player_skills[i][1] if self.player_skills[i][1] > 0 else 0
                self.draw_bar(x, bar_y, 64, 10, 1 - cd_percent, (0, 0, 255))
                txt = self.font.render(f"{cd}", True, (255,255,255))
                screen.blit(txt, (x+20, bar_y+15))

            # 攻击当前Boss
            if current_boss >= len(self.boss_hp):
                break
            damage, cooldown = self.player_skills[skill_id]
            if self.cooldowns[skill_id] == 0:
                self.boss_hp[current_boss] -= damage
                self.cooldowns[skill_id] = cooldown
                if self.boss_hp[current_boss] <= 0:
                    current_boss += 1
            # 冷却减1
            for i in range(len(self.cooldowns)):
                if self.cooldowns[i] > 0:
                    self.cooldowns[i] -= 1

            pygame.display.update()
            time.sleep(0.8)
            clock.tick(60)

        print("击败Boss，返回主迷宫。")
        global resource_value
        resource_value -= self.min_turns
        font = pygame.font.SysFont(None, 32)
        screen.fill((0, 0, 0))
        msg = font.render(f"Stage Clear! Spend {self.min_turns} turns = -{self.min_turns} Gold", True, (255, 255, 255))
        screen.blit(msg, (20, 220))

        hint_text = font.render("Press [z] to exit...", True, (220, 220, 220))
        hint_rect = hint_text.get_rect(center=(screen.get_width() // 2, screen.get_height() * 7 // 8))
        screen.blit(hint_text, hint_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        waiting = False

class EndScene:
    def __init__(self):
        pass

    def enter(self):
        global resource_value
        print("进入结算界面...")
        font = pygame.font.SysFont(None, 64)
        screen.fill((0, 0, 0))
        msg = font.render(f"You won {resource_value} Gold", True, (255, 255, 255))
        screen.blit(msg, (20, 220))

        hint_text = font.render("Press [z] to exit...", True, (220, 220, 220))
        hint_rect = hint_text.get_rect(center=(screen.get_width() // 2, screen.get_height() * 7 // 8))
        screen.blit(hint_text, hint_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        waiting = False

        print("通关成功！用时：X秒，资源：Y")
        pygame.quit()
        exit()

if __name__ == '__main__':
    filepath = "maze_15_15.json"
    the_maze = load_data_from_json(filepath, "maze")
    scene = MazeScene(the_maze, the_images)
    character = Character(the_images)
    start = (0, 11)

    logic_maze = copy.deepcopy(the_maze)
    resource, final_pos, path_part, exit_pos = explore_and_collect(logic_maze, start)
    path = []
    if exit_pos:
        exit_path = bfs_to_exit(logic_maze, final_pos, exit_pos)
        exit_path = exit_path[1:]  # 第一个和之前path的最后一个位置相同
        path = path_part + exit_path
        print(path)

    B = load_data_from_json(filepath, "B")
    PlayerSkills = load_data_from_json(filepath, "PlayerSkills")
    five_result = min_turns_to_defeat(B, PlayerSkills)
    # print(five_result)
    while True:
        scene.render_maze()
        pygame.display.update()
        character.walk_path(scene, path, file_name=filepath, five_result=five_result)
        break