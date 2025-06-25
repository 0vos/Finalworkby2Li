# import random
# import numpy as np


# def init_maze(height, width):
#     """初始化迷宫为全空格"""
#     return [['O' for _ in range(width)] for _ in range(height)]

# def print_maze(maze):
#     """打印当前迷宫状态"""
#     for row in maze:
#         print(''.join(row))
#     print()  # 添加空行分隔不同状态

# def dig_maze(maze, top, bottom, left, right, door_history=None):
#     """
#     递归分割迷宫区域，避免在门洞附近生成新墙
#     :param maze: 迷宫二维列表
#     :param top: 当前区域上边界
#     :param bottom: 当前区域下边界
#     :param left: 当前区域左边界
#     :param right: 当前区域右边界
#     :param door_history: 记录门洞位置的历史
#     """
#     # 初始化门洞历史记录
#     if door_history is None:
#         door_history = {'rows': set(), 'cols': set()}
    
#     # 计算当前区域的高度和宽度
#     height_region = bottom - top + 1
#     width_region = right - left + 1
    
#     # 终止条件：区域太小无法继续分割
#     if height_region < 3 or width_region < 3:
#         return
    
#     # 创建候选墙位置列表
#     row_candidates = [r for r in range(top + 1, bottom) if r not in door_history['rows']]
#     col_candidates = [c for c in range(left + 1, right) if c not in door_history['cols']]
    
#     # 如果没有合适的候选位置，则返回
#     if not row_candidates or not col_candidates:
#         return
    
#     # 随机选择十字墙的位置（避开门洞附近区域）
#     wall_row = random.choice(row_candidates)
#     wall_col = random.choice(col_candidates)
    
#     # 绘制横墙（行墙）
#     for col in range(left, right + 1):
#         maze[wall_row][col] = '#'
    
#     # 绘制竖墙（列墙）
#     for row in range(top, bottom + 1):
#         maze[row][wall_col] = '#'
    
#     # 准备四个可能的门洞位置（十字墙的四个臂）
#     door_positions = [
#         # 上臂（竖墙上半部分）
#         (random.randint(top, wall_row - 1), wall_col),
#         # 下臂（竖墙下半部分）
#         (random.randint(wall_row + 1, bottom), wall_col),
#         # 左臂（横墙左半部分）
#         (wall_row, random.randint(left, wall_col - 1)),
#         # 右臂（横墙右半部分）
#         (wall_row, random.randint(wall_col + 1, right))
#     ]
    
#     # 随机选择三个门洞打开
#     selected_doors = random.sample(door_positions, 3)
#     for door in selected_doors:
#         row, col = door
#         maze[row][col] = 'O'  # 开门洞
    
#     # 更新门洞历史记录
#     for row, col in selected_doors:
#         door_history['rows'].add(row)
#         door_history['cols'].add(col)
    
#     # 打印当前迷宫状态
#     print(f"添加十字墙并开门洞后（区域[{top},{bottom}]x[{left},{right}]）:")
#     print_maze(maze)
    
#     # 创建新的门洞历史记录副本用于递归（确保子区域不会修改父区域的历史）
#     new_door_history = {'rows': set(door_history['rows']), 'cols': set(door_history['cols'])}
    
#     # 递归处理四个子区域
#     # 左上区域
#     dig_maze(maze, top, wall_row - 1, left, wall_col - 1, new_door_history)
#     # 右上区域
#     dig_maze(maze, top, wall_row - 1, wall_col + 1, right, new_door_history)
#     # 左下区域
#     dig_maze(maze, wall_row + 1, bottom, left, wall_col - 1, new_door_history)
#     # 右下区域
#     dig_maze(maze, wall_row + 1, bottom, wall_col + 1, right, new_door_history)

# def add_border(maze):
#     """为迷宫添加封闭边框"""
#     height = len(maze)
#     width = len(maze[0])
    
#     # 添加上下边框
#     for col in range(width):
#         maze[0][col] = '#'
#         maze[height-1][col] = '#'
    
#     # 添加左右边框
#     for row in range(height):
#         maze[row][0] = '#'
#         maze[row][width-1] = '#'

# def set_SE(maze):
#     """在迷宫边框上设置起点和终点，确保它们可通行"""
#     height = len(maze)
#     width = len(maze[0])
    
#     # 1. 收集所有可能的起点位置（边框上的位置）
#     candidate_positions = []
    
#     # 上边框（排除角落）
#     for col in range(1, width-1):
#         if maze[1][col] == 'O':  # 确保下方是通路
#             candidate_positions.append((0, col))
    
#     # 下边框（排除角落）
#     for col in range(1, width-1):
#         if maze[height-2][col] == 'O':  # 确保上方是通路
#             candidate_positions.append((height-1, col))
    
#     # 左边框（排除角落）
#     for row in range(1, height-1):
#         if maze[row][1] == 'O':  # 确保右方是通路
#             candidate_positions.append((row, 0))
    
#     # 右边框（排除角落）
#     for row in range(1, height-1):
#         if maze[row][width-2] == 'O':  # 确保左方是通路
#             candidate_positions.append((row, width-1))
    
#     # # 2. 如果没有找到候选位置，尝试在角落附近寻找
#     # if not candidate_positions:
#     #     # 左上角
#     #     if maze[1][0] == ' ' or maze[0][1] == ' ':
#     #         candidate_positions.append((0, 0))
#     #     # 右上角
#     #     if maze[1][width-1] == ' ' or maze[0][width-2] == ' ':
#     #         candidate_positions.append((0, width-1))
#     #     # 左下角
#     #     if maze[height-2][0] == ' ' or maze[height-1][1] == ' ':
#     #         candidate_positions.append((height-1, 0))
#     #     # 右下角
#     #     if maze[height-2][width-1] == ' ' or maze[height-1][width-2] == ' ':
#     #         candidate_positions.append((height-1, width-1))
    
#     # # 3. 如果仍然没有候选位置，强制在边框上创建通路
#     # if not candidate_positions:
#     #     # 尝试在顶部中间位置创建通路
#     #     mid_col = width // 2
#     #     maze[0][mid_col] = ' '
#     #     maze[1][mid_col] = ' '  # 确保内部连通
#     #     candidate_positions.append((0, mid_col))
    
#     # 4. 随机选择起点和终点
#     if len(candidate_positions) < 2:
#         # 只有一个候选位置，使用它作为起点和终点（虽然不合理，但作为保底）
#         start = end = random.choice(candidate_positions)
#     else:
#         # 确保起点和终点不同
#         start, end = random.sample(candidate_positions, 2)
    
#     # 5. 设置起点和终点
#     maze[start[0]][start[1]] = 'S'
#     maze[end[0]][end[1]] = 'E'
    
#     return start, end


# def place_items(maze):
#      open_posotions = []
#      for i in range(len(maze)):
#          for j in range(len(maze[i])):
#              if maze[i][j] == 'O':
#                  open_posotions.append((i,j))

#      items = ['B','T','L','G']
#      items_counts={}
#      for item in items:
#          count = random.randint(3,7)  # 每个都随机生成3-7个
#          items_counts[item] = count
     
#      for item,count in items_counts.items():
#          if count > len(open_posotions):
#              count = len(open_posotions)

#          sel_pos = random.sample(open_posotions,count)

#          for pos in sel_pos:
#              i,j=pos
#              maze[i][j] = item
#              open_posotions.remove(pos)
#      return items_counts
            

# # 主程序
# print("程序开始")

# # 获取用户输入的迷宫尺寸
# height = int(input("请输入迷宫的高度(至少5): "))
# width = int(input("请输入迷宫的宽度(至少5): "))

# # 初始化迷宫
# maze = init_maze(height, width)
# print("初始迷宫:")
# print_maze(maze)

# # 递归分割迷宫（内部区域，避开外边框）
# dig_maze(maze, 1, height-2, 1, width-2)

# # 添加外边框
# add_border(maze)
# print("添加边框后的迷宫:")
# print_maze(maze)

# # 设置起点和终点
# start, end = set_SE(maze)
# print(f"起点位置: ({start[0]}, {start[1]}), 终点位置: ({end[0]}, {end[1]})")

# #随机放置道具
# items_counts = place_items(maze)
# print(f"物品放置情况: B={items_counts['B']}, T={items_counts['T']}, L={items_counts['L']}, G={items_counts['G']}")



# print("最终迷宫:")
# print_maze(maze)

# # 将迷宫转换为NumPy数组
# maze_array = np.array(maze)

# # 打印NumPy数组信息
# print("迷宫数组形状:", maze_array.shape)
# print("迷宫数组:")
# print(maze_array)


# print("程序结束")



import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colors
import matplotlib.patches as mpatches
import time

# 全局变量用于存储动画帧
animation_frames = []

def init_maze(height, width):
    """初始化迷宫为全空格"""
    return [['O' for _ in range(width)] for _ in range(height)]

def print_maze(maze):
    """打印当前迷宫状态"""
    for row in maze:
        print(''.join(row))
    print()  # 添加空行分隔不同状态

def capture_frame(maze, title):
    """捕获当前迷宫状态作为动画帧"""
    # 将迷宫转换为NumPy数组以便处理
    maze_array = np.array(maze)
    
    # 创建副本并添加标题信息
    frame = {
        "maze": maze_array.copy(),
        "title": title,
        "timestamp": time.time()
    }
    animation_frames.append(frame)
    
    # 打印当前状态（可选）
    print(title)

def dig_maze(maze, top, bottom, left, right, door_history=None):
    """
    递归分割迷宫区域，避免在门洞附近生成新墙
    :param maze: 迷宫二维列表
    :param top: 当前区域上边界
    :param bottom: 当前区域下边界
    :param left: 当前区域左边界
    :param right: 当前区域右边界
    :param door_history: 记录门洞位置的历史
    """
    # 初始化门洞历史记录
    if door_history is None:
        door_history = {'rows': set(), 'cols': set()}
    
    # 计算当前区域的高度和宽度
    height_region = bottom - top + 1
    width_region = right - left + 1
    
    # 终止条件：区域太小无法继续分割
    if height_region < 3 or width_region < 3:
        return
    
    # 创建候选墙位置列表
    row_candidates = [r for r in range(top + 1, bottom) if r not in door_history['rows']]
    col_candidates = [c for c in range(left + 1, right) if c not in door_history['cols']]
    
    # 如果没有合适的候选位置，则返回
    if not row_candidates or not col_candidates:
        return
    
    # 随机选择十字墙的位置（避开门洞附近区域）
    wall_row = random.choice(row_candidates)
    wall_col = random.choice(col_candidates)
    
    # 绘制横墙（行墙）
    for col in range(left, right + 1):
        maze[wall_row][col] = '#'
    
    # 绘制竖墙（列墙）
    for row in range(top, bottom + 1):
        maze[row][wall_col] = '#'
    
    # 捕获添加墙壁后的状态
    capture_frame(maze, f"添加十字墙 ({wall_row}, {wall_col})")
    
    # 准备四个可能的门洞位置（十字墙的四个臂）
    door_positions = [
        # 上臂（竖墙上半部分）
        (random.randint(top, wall_row - 1), wall_col),
        # 下臂（竖墙下半部分）
        (random.randint(wall_row + 1, bottom), wall_col),
        # 左臂（横墙左半部分）
        (wall_row, random.randint(left, wall_col - 1)),
        # 右臂（横墙右半部分）
        (wall_row, random.randint(wall_col + 1, right))
    ]
    
    # 随机选择三个门洞打开
    selected_doors = random.sample(door_positions, 3)
    for door in selected_doors:
        row, col = door
        maze[row][col] = 'O'  # 开门洞
    
    # 更新门洞历史记录
    for row, col in selected_doors:
        door_history['rows'].add(row)
        door_history['cols'].add(col)
    
    # 捕获开门洞后的状态
    capture_frame(maze, f"开门洞后（区域[{top},{bottom}]x[{left},{right}]）")
    
    # 创建新的门洞历史记录副本用于递归（确保子区域不会修改父区域的历史）
    new_door_history = {'rows': set(door_history['rows']), 'cols': set(door_history['cols'])}
    
    # 递归处理四个子区域
    # 左上区域
    dig_maze(maze, top, wall_row - 1, left, wall_col - 1, new_door_history)
    # 右上区域
    dig_maze(maze, top, wall_row - 1, wall_col + 1, right, new_door_history)
    # 左下区域
    dig_maze(maze, wall_row + 1, bottom, left, wall_col - 1, new_door_history)
    # 右下区域
    dig_maze(maze, wall_row + 1, bottom, wall_col + 1, right, new_door_history)

def add_border(maze):
    """为迷宫添加封闭边框"""
    height = len(maze)
    width = len(maze[0])
    
    # 添加上下边框
    for col in range(width):
        maze[0][col] = '#'
        maze[height-1][col] = '#'
    
    # 添加左右边框
    for row in range(height):
        maze[row][0] = '#'
        maze[row][width-1] = '#'
    
    # 捕获添加边框后的状态
    capture_frame(maze, "添加边框后")

def set_SE(maze):
    """在迷宫边框上设置起点和终点，确保它们可通行"""
    height = len(maze)
    width = len(maze[0])
    
    # 1. 收集所有可能的起点位置（边框上的位置）
    candidate_positions = []
    
    # 上边框（排除角落）
    for col in range(1, width-1):
        if maze[1][col] == 'O':  # 确保下方是通路
            candidate_positions.append((0, col))
    
    # 下边框（排除角落）
    for col in range(1, width-1):
        if maze[height-2][col] == 'O':  # 确保上方是通路
            candidate_positions.append((height-1, col))
    
    # 左边框（排除角落）
    for row in range(1, height-1):
        if maze[row][1] == 'O':  # 确保右方是通路
            candidate_positions.append((row, 0))
    
    # 右边框（排除角落）
    for row in range(1, height-1):
        if maze[row][width-2] == 'O':  # 确保左方是通路
            candidate_positions.append((row, width-1))
    
    # 4. 随机选择起点和终点
    if len(candidate_positions) < 2:
        # 只有一个候选位置，使用它作为起点和终点（虽然不合理，但作为保底）
        start = end = random.choice(candidate_positions)
    else:
        # 确保起点和终点不同
        start, end = random.sample(candidate_positions, 2)
    
    # 5. 设置起点和终点
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'
    
    # 捕获设置起点和终点后的状态
    capture_frame(maze, f"设置起点({start})和终点({end})")
    
    return start, end


def place_items(maze):
     open_positions = []
     for i in range(len(maze)):
         for j in range(len(maze[i])):
             if maze[i][j] == 'O':
                 open_positions.append((i,j))

     items = ['B','T','L','G']
     items_counts={}
     for item in items:
         count = random.randint(3,7)  # 每个都随机生成3-7个
         items_counts[item] = count
     
     # 捕获放置物品前的状态
     capture_frame(maze, "开始放置物品")
     
     for item,count in items_counts.items():
         if count > len(open_positions):
             count = len(open_positions)

         sel_pos = random.sample(open_positions,count)

         for pos in sel_pos:
             i,j=pos
             maze[i][j] = item
             open_positions.remove(pos)
             
             # 捕获每个物品放置后的状态
             capture_frame(maze, f"放置{item}在({i},{j})")
     
     return items_counts

def create_animation():
    """创建并显示迷宫生成动画"""
    if not animation_frames:
        print("没有动画帧可显示")
        return
    
    # 设置颜色映射
    cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'blue', 'yellow', 'purple', 'orange'])
    bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    # 创建字符到数字的映射
    char_to_num = {
        'O': 0,  # 通路 - 白色
        '#': 1,  # 墙 - 黑色
        'S': 2,  # 起点 - 绿色
        'E': 3,  # 终点 - 红色
        'B': 4,  # B - 蓝色
        'T': 5,  # T - 黄色
        'L': 6,  # L - 紫色
        'G': 7   # G - 橙色
    }
    
    # 创建图例
    legend_labels = {
        'O': 'Access',
        '#': 'Wall',
        'S': 'Start',
        'E': 'Exit',
        'B': 'BOSS',
        'T': 'Trap',
        'L': 'Locker',
        'G': 'Gold'
    }
    
    # 创建图例
    patches = [mpatches.Patch(color=cmap(char_to_num[char]), label=label) 
               for char, label in legend_labels.items()]
    
    # 设置图形
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.subplots_adjust(right=0.85)  # 为图例留出空间
    
    # 初始化图像
    frame_data = animation_frames[0]["maze"]
    num_rows, num_cols = frame_data.shape
    img_data = np.zeros((num_rows, num_cols))
    
    for i in range(num_rows):
        for j in range(num_cols):
            img_data[i, j] = char_to_num.get(frame_data[i, j], 0)
    
    img = ax.imshow(img_data, cmap=cmap, norm=norm, interpolation='nearest')
    title = ax.set_title(f"初始迷宫")
    
    # 添加图例
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    # 更新函数
    def update(frame_idx):
        frame = animation_frames[frame_idx]
        frame_data = frame["maze"]
        
        for i in range(num_rows):
            for j in range(num_cols):
                img_data[i, j] = char_to_num.get(frame_data[i, j], 0)
        
        img.set_data(img_data)
        title.set_text(frame["title"])
        return img, title
    
    # 创建动画 - 设置repeat=False使动画只播放一次
    ani = FuncAnimation(
        fig, 
        update, 
        frames=len(animation_frames), 
        interval=300, 
        blit=True,
        repeat=False  # 关键修改：只播放一次
    )
    
    # 保存动画（可选）
    # ani.save('maze_generation.gif', writer='pillow', fps=5, dpi=100)
    
    plt.show()
    return ani

# 主程序
print("程序开始")

# 获取用户输入的迷宫尺寸
height = int(input("请输入迷宫的高度(至少5): "))
width = int(input("请输入迷宫的宽度(至少5): "))

# 初始化迷宫
maze = init_maze(height, width)
print("初始迷宫:")
print_maze(maze)

# 捕获初始状态
capture_frame(maze, "初始迷宫")

# 递归分割迷宫（内部区域，避开外边框）
dig_maze(maze, 1, height-2, 1, width-2)

# 添加外边框
add_border(maze)
print("添加边框后的迷宫:")
print_maze(maze)

# 设置起点和终点
start, end = set_SE(maze)
print(f"起点位置: ({start[0]}, {start[1]}), 终点位置: ({end[0]}, {end[1]})")

# 随机放置道具
items_counts = place_items(maze)
print(f"物品放置情况: B={items_counts['B']}, T={items_counts['T']}, L={items_counts['L']}, G={items_counts['G']}")

# 捕获最终状态
capture_frame(maze, "最终迷宫")

print("最终迷宫:")
print_maze(maze)

# 将迷宫转换为NumPy数组
maze_array = np.array(maze)

# 打印NumPy数组信息
print("迷宫数组形状:", maze_array.shape)
print("迷宫数组:")
print(maze_array)

# 创建并显示动画
print("创建动画...")
create_animation()

print("程序结束")