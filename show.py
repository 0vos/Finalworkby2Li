from three采用贪心算法设计实时资源拾取策略 import explore_and_collect, bfs_to_exit
from four采用回溯法解谜关卡 import solve_with_backtracking
from five import min_turns_to_defeat
import pygame
import time
import copy

# 初始化
pygame.init()
width, height = 480, 480
screen = pygame.display.set_mode((width, height))
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
                screen.blit(image, (col_idx * tile_size, row_idx * tile_size))

    def update_cell(self, pos, value):
        self.maze[pos[0]][pos[1]] = value

class Character:
    def __init__(self, images):
        self.images = images

    def paint_character(self, pos):
        # 玩家绘制
        screen.blit(self.images['P'], (pos[1] * tile_size, pos[0] * tile_size))

    def walk_path(self, maze_scene, path):
        for idx, pos in enumerate(path):
            pygame.event.pump()
            maze_scene.render_maze()
            self.paint_character(pos)
            pygame.display.update()
            time.sleep(0.3)

            cell = maze_scene.maze[pos[0]][pos[1]]
            if cell in ('G', 'T'):
                maze_scene.update_cell(pos, ' ')  # 采集金币或触发陷阱后设为路
            elif cell == 'L':
                LockScene().enter()
                maze_scene.update_cell(pos, ' ')  # 解锁完成
            elif cell == 'B':
                BossScene().enter()
                maze_scene.update_cell(pos, ' ')  # 打Boss完成
            elif cell == 'E':
                EndScene().enter()
                return

class LockScene:
    def __init__(self):
        pass

    def enter(self):
        print("进入解锁界面...")
        time.sleep(1)
        print("解锁成功，返回主迷宫。")

class BossScene:
    def __init__(self):
        pass

    def enter(self):
        print("进入Boss战界面...")
        time.sleep(1)
        print("击败Boss，返回主迷宫。")

class EndScene:
    def __init__(self):
        pass

    def enter(self):
        print("进入结算界面...")
        print("通关成功！用时：X秒，资源：Y")
        pygame.quit()
        exit()

if __name__ == '__main__':
    the_maze = [
        list("###########S###"),
        list("# GTG#        #"),
        list("###G### #######"),
        list("# T   #   # #G#"),
        list("### # ### # #G#"),
        list("# G # #G    GT#"),
        list("### # #####T#T#"),
        list("# # # #     # #"),
        list("#T# # ### ### #"),
        list("#   #       # #"),
        list("# #############"),
        list("#   #G# T #GT #"),
        list("### #T# ##### #"),
        list("#    L  B   TG#"),
        list("#########E#####")
    ]

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
    # path = [(0, 12), (0, 11), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 7), (2, 7), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (5, 8), (5, 7), (5, 8), (5, 9), (4, 9), (5, 9), (5, 10), (5, 11), (4, 11), (5, 11), (5, 12), (5, 13), (4, 13), (3, 13), (4, 13), (3, 13), (4, 13), (5, 13), (5, 12), (5, 11), (6, 11), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 8), (7, 9), (8, 9), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (3, 4), (3, 3), (2, 3), (1, 3), (1, 2), (1, 1), (1, 2), (1, 1), (1, 2), (1, 3), (2, 3), (1, 3), (1, 4), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (5, 2), (5, 1), (5, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (9, 2), (9, 1), (10, 1), (11, 1), (11, 2), (11, 3), (12, 3), (13, 3), (13, 2), (13, 1), (13, 2), (13, 3), (12, 3), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (12, 7), (11, 7), (11, 8), (11, 9), (11, 8), (11, 7), (12, 7), (13, 7), (13, 8),(13, 9), (14, 9)]
    while True:
        scene.render_maze()
        pygame.display.update()
        character.walk_path(scene, path)
        break