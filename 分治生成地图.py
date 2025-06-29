import random
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colors

def recursive_division(r1, r2, c1, c2, M, history):
    """
    递归分割迷宫生成算法，同时记录每一步的历史状态
    """
    # 记录当前状态
    history.append(M.copy())
    
    if r1 < r2 and c1 < c2:
        rm = random.randint(r1, r2 - 1)
        cm = random.randint(c1, c2 - 1)
        
        # 随机选择三个开洞位置
        cd1 = random.randint(c1, cm)
        cd2 = random.randint(cm + 1, c2)
        rd1 = random.randint(r1, rm)
        rd2 = random.randint(rm + 1, r2)
        
        # 随机选择一种开洞模式
        d = random.randint(1, 4)
        if d == 1:
            M[rd2, cm, 2] = 1
            M[rd2, cm + 1, 0] = 1
            M[rm, cd1, 3] = 1
            M[rm + 1, cd1, 1] = 1
            M[rm, cd2, 3] = 1
            M[rm + 1, cd2, 1] = 1
        elif d == 2:
            M[rd1, cm, 2] = 1
            M[rd1, cm + 1, 0] = 1
            M[rm, cd1, 3] = 1
            M[rm + 1, cd1, 1] = 1
            M[rm, cd2, 3] = 1
            M[rm + 1, cd2, 1] = 1
        elif d == 3:
            M[rd1, cm, 2] = 1
            M[rd1, cm + 1, 0] = 1
            M[rd2, cm, 2] = 1
            M[rd2, cm + 1, 0] = 1
            M[rm, cd2, 3] = 1
            M[rm + 1, cd2, 1] = 1
        elif d == 4:
            M[rd1, cm, 2] = 1
            M[rd1, cm + 1, 0] = 1
            M[rd2, cm, 2] = 1
            M[rd2, cm + 1, 0] = 1
            M[rm, cd1, 3] = 1
            M[rm + 1, cd1, 1] = 1
        
        # 记录开洞后的状态
        history.append(M.copy())
        
        # 递归处理四个子区域
        recursive_division(r1, rm, c1, cm, M, history)
        recursive_division(r1, rm, cm + 1, c2, M, history)
        recursive_division(rm + 1, r2, c1, cm, M, history)
        recursive_division(rm + 1, r2, cm + 1, c2, M, history)
    
    elif r1 < r2:  # 区域高度大于1，宽度为1
        rm = random.randint(r1, r2 - 1)
        # 打通上下两个区域
        M[rm, c1, 3] = 1
        M[rm + 1, c1, 1] = 1
        # 记录状态
        history.append(M.copy())
        recursive_division(r1, rm, c1, c1, M, history)
        recursive_division(rm + 1, r2, c1, c1, M, history)
    
    elif c1 < c2:  # 区域宽度大于1，高度为1
        cm = random.randint(c1, c2 - 1)
        # 打通左右两个区域
        M[r1, cm, 2] = 1
        M[r1, cm + 1, 0] = 1
        # 记录状态
        history.append(M.copy())
        recursive_division(r1, r1, c1, cm, M, history)
        recursive_division(r1, r1, cm + 1, c2, M, history)

def generate_maze_with_history(n):
    """
    生成迷宫并返回迷宫状态历史记录
    """
    # 初始化迷宫矩阵（每个单元格有4面墙）
    M = np.zeros((n, n, 4), dtype=int)
    history = []
    
    # 记录初始状态
    history.append(M.copy())
    
    # 递归分割生成迷宫
    recursive_division(0, n - 1, 0, n - 1, M, history)
    
    # 设置入口和出口
    M[0, 0, 0] = 1  # 入口（左上角左侧）
    M[n - 1, n - 1, 2] = 1  # 出口（右下角右侧）
    
    # 记录最终状态
    history.append(M.copy())
    
    return M, history

def maze_to_grid(M, n):
    """
    将迷宫矩阵转换为可视化网格
    """
    size = 2 * n + 1
    grid = np.zeros((size, size), dtype=int)
    
    # 0: 墙
    # 1: 通路
    # 2: 当前处理区域
    
    # 标记通路位置
    for i in range(n):
        for j in range(n):
            # 单元格中心位置
            grid[2 * i + 1][2 * j + 1] = 1
            
            # 检查并打通左墙
            if M[i, j, 0] == 1:
                grid[2 * i + 1][2 * j] = 1
            
            # 检查并打通上墙
            if M[i, j, 1] == 1:
                grid[2 * i][2 * j + 1] = 1
            
            # 检查并打通右墙
            if M[i, j, 2] == 1:
                grid[2 * i + 1][2 * j + 2] = 1
            
            # 检查并打通下墙
            if M[i, j, 3] == 1:
                grid[2 * i + 2][2 * j + 1] = 1
    
    return grid

def create_animation(history, n):
    """
    创建迷宫生成过程的动画
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 创建自定义颜色映射
    # 0: 墙 (黑色)
    # 1: 通路 (白色)
    cmap = colors.ListedColormap(['black', 'white'])
    bounds = [0, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    # 初始网格
    initial_grid = maze_to_grid(history[0], n)
    img = ax.imshow(initial_grid, cmap=cmap, norm=norm, interpolation='nearest')
    
    # 设置标题
    ax.set_title(f'Maze Generation Process (n={n})')
    
    # 移除坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    
    # 更新函数
    def update(frame):
        grid = maze_to_grid(history[frame], n)
        img.set_data(grid)
        ax.set_title(f'Maze Generation Process (n={n}) - Step {frame+1}/{len(history)}')
        return img,
    
    # 创建动画
    ani = FuncAnimation(
        fig, update, frames=len(history),
        interval=200, blit=True, repeat=False
    )
    
    plt.tight_layout()
    plt.show()
    
    return ani

def set_start_end(maze, n):
    """
    在边界上随机设置起点S和终点E（不在四个角）
    """
    size = 2 * n + 1
    # 定义边界位置（不包括四个角）
    boundary_positions = []
    
    # 上边界（第0行，第1列到倒数第2列）
    for j in range(1, size - 1):
        boundary_positions.append((0, j))
    
    # 下边界（最后一行，第1列到倒数第2列）
    for j in range(1, size - 1):
        boundary_positions.append((size - 1, j))
    
    # 左边界（第0列，第1行到倒数第2行）
    for i in range(1, size - 1):
        boundary_positions.append((i, 0))
    
    # 右边界（最后一列，第1行到倒数第2行）
    for i in range(1, size - 1):
        boundary_positions.append((i, size - 1))
    
    # 筛选边界上可用的通路位置（空格）
    available_positions = [pos for pos in boundary_positions if maze[pos[0]][pos[1]] == ' ']
    
    if len(available_positions) < 2:
        # 如果可用位置不足，使用默认位置
        start = (1, 0)  # 左上角附近
        end = (size - 2, size - 1)  # 右下角附近
    else:
        # 随机选择起点和终点
        start = random.choice(available_positions)
        available_positions.remove(start)
        end = random.choice(available_positions)
    
    # 设置起点和终点
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'
    
    return start, end

def add_elements(maze, n):
    """
    在迷宫的通路位置随机添加元素
    G: 金币
    T: 陷阱
    L: 机关
    B: BOSS
    """
    size = 2 * n + 1
    path_positions = []
    for i in range(size):
        for j in range(size):
            if maze[i][j] == ' ':
                path_positions.append((i, j))
    
    if not path_positions:
        return
    
    # 随机选择一些位置放置元素
    # 确保入口(S)和出口(E)不被覆盖
    entrance = None
    exit_pos = None
    for i in range(size):
        for j in range(size):
            if maze[i][j] == 'S':
                entrance = (i, j)
            elif maze[i][j] == 'E':
                exit_pos = (i, j)
    
    # 放置BOSS（只有一个）
    if path_positions:
        boss_candidates = [pos for pos in path_positions if pos != entrance and pos != exit_pos]
        if boss_candidates:
            boss_pos = random.choice(boss_candidates)
            maze[boss_pos[0]][boss_pos[1]] = 'B'
            path_positions.remove(boss_pos)
    
    # 计算要放置的元素总数（随机，但不超过通路位置数量的1/3）
    total_elements = min(len(path_positions), random.randint(1, max(1, len(path_positions) // 3)))
    
    # 随机选择位置放置其他元素
    for _ in range(total_elements):
        if not path_positions:
            break
            
        pos = random.choice(path_positions)
        path_positions.remove(pos)
        
        # 跳过入口和出口位置
        if pos == entrance or pos == exit_pos:
            continue
            
        # 随机选择元素类型
        element_type = random.choices(
            ['G', 'T', 'L'], 
            weights=[5, 3, 2],  # 金币出现概率最高
            k=1
        )[0]
        
        maze[pos[0]][pos[1]] = element_type

def final_maze_to_grid(maze_array, n):
    """
    将最终迷宫转换为可视化网格
    """
    size = 2 * n + 1
    grid = np.zeros((size, size), dtype=int)
    
    # 创建颜色映射
    # 0: 墙 (黑色)
    # 1: 通路 (白色)
    # 2: 起点 (绿色)
    # 3: 终点 (红色)
    # 4: BOSS (紫色)
    # 5: 金币 (黄色)
    # 6: 陷阱 (橙色)
    # 7: 机关 (蓝色)
    
    for i in range(size):
        for j in range(size):
            cell = maze_array[i][j]
            if cell == '#':
                grid[i][j] = 0  # 墙
            elif cell == ' ':
                grid[i][j] = 1  # 通路
            elif cell == 'S':
                grid[i][j] = 2  # 起点
            elif cell == 'E':
                grid[i][j] = 3  # 终点
            elif cell == 'B':
                grid[i][j] = 4  # BOSS
            elif cell == 'G':
                grid[i][j] = 5  # 金币
            elif cell == 'T':
                grid[i][j] = 6  # 陷阱
            elif cell == 'L':
                grid[i][j] = 7  # 机关
    
    return grid

def plot_final_maze(maze_array, n):
    """
    绘制最终迷宫
    """
    grid = final_maze_to_grid(maze_array, n)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 创建自定义颜色映射
    cmap = colors.ListedColormap([
        'black',    # 0: 墙
        'white',    # 1: 通路
        'green',    # 2: 起点
        'red',      # 3: 终点
        'purple',   # 4: BOSS
        'yellow',   # 5: 金币
        'orange',   # 6: 陷阱
        'blue'      # 7: 机关
    ])
    
    bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    img = ax.imshow(grid, cmap=cmap, norm=norm, interpolation='nearest')
    
    # 添加图例
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc='black'),
        plt.Rectangle((0, 0), 1, 1, fc='white'),
        plt.Rectangle((0, 0), 1, 1, fc='green'),
        plt.Rectangle((0, 0), 1, 1, fc='red'),
        plt.Rectangle((0, 0), 1, 1, fc='purple'),
        plt.Rectangle((0, 0), 1, 1, fc='yellow'),
        plt.Rectangle((0, 0), 1, 1, fc='orange'),
        plt.Rectangle((0, 0), 1, 1, fc='blue')
    ]
    
    ax.legend(legend_elements, 
              ['Wall', 'Path', 'Start', 'End', 'BOSS', 'Gold', 'Trap', 'Locker'],
              loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # 设置标题
    ax.set_title(f'Final Maze (n={n})')
    
    # 移除坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.show()

# 获取用户输入
n = int(input("请输入迷宫大小 n: "))

# 生成迷宫并获取历史状态
M, history = generate_maze_with_history(n)

# 创建动画展示迷宫生成过程
print("\n生成迷宫动画...")
create_animation(history, n)

# 创建最终迷宫
size = 2 * n + 1
maze_array = [['#' for _ in range(size)] for _ in range(size)]

# 标记通路位置
for i in range(n):
    for j in range(n):
        # 单元格中心位置
        maze_array[2 * i + 1][2 * j + 1] = ' '
        
        # 检查并打通左墙
        if M[i, j, 0] == 1:
            maze_array[2 * i + 1][2 * j] = ' '
        
        # 检查并打通上墙
        if M[i, j, 1] == 1:
            maze_array[2 * i][2 * j + 1] = ' '
        
        # 检查并打通右墙
        if M[i, j, 2] == 1:
            maze_array[2 * i + 1][2 * j + 2] = ' '
        
        # 检查并打通下墙
        if M[i, j, 3] == 1:
            maze_array[2 * i + 2][2 * j + 1] = ' '

# 设置起点和终点
set_start_end(maze_array, n)

# 在通路位置添加随机元素
add_elements(maze_array, n)

# 打印迷宫
print("\n生成的迷宫:")
for row in maze_array:
    print(''.join(row))

# 绘制最终迷宫
print("\n绘制最终迷宫...")
plot_final_maze(maze_array, n)

# 存储结果的二维数组
print("\n迷宫数组已生成并存储。")

# 保存 JSON 文件
with open('maze.json', 'w', encoding='utf-8') as f:
    json.dump({'maze': maze_array}, f, ensure_ascii=False, indent=2)