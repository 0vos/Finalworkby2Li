import random


def init_maze(height, width):
    """初始化迷宫为全空格"""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_maze(maze):
    """打印当前迷宫状态"""
    for row in maze:
        print(''.join(row))
    print()  # 添加空行分隔不同状态

def dig_maze(maze, top, bottom, left, right):
    """
    递归分割迷宫区域
    :param maze: 迷宫二维列表
    :param top: 当前区域上边界
    :param bottom: 当前区域下边界
    :param left: 当前区域左边界
    :param right: 当前区域右边界
    """
    # 计算当前区域的高度和宽度
    height_region = bottom - top + 1
    width_region = right - left + 1
    
    # 终止条件：区域太小无法继续分割
    if height_region < 3 or width_region < 3:
        return
    
    # 随机选择十字墙的位置（避开边界）
    wall_row = random.randint(top + 1, bottom - 1)
    wall_col = random.randint(left + 1, right - 1)
    
    # 绘制横墙（行墙）
    for col in range(left, right + 1):
        maze[wall_row][col] = '#'
    
    # 绘制竖墙（列墙）
    for row in range(top, bottom + 1):
        maze[row][wall_col] = '#'
    
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
    for door in random.sample(door_positions, 3):
        row, col = door
        maze[row][col] = ' '  # 开门洞
    
    # 打印当前迷宫状态
    print(f"添加十字墙并开门洞后（区域[{top},{bottom}]x[{left},{right}]）:")
    print_maze(maze)
    
    # 递归处理四个子区域
    # 左上区域
    dig_maze(maze, top, wall_row - 1, left, wall_col - 1)
    # 右上区域
    dig_maze(maze, top, wall_row - 1, wall_col + 1, right)
    # 左下区域
    dig_maze(maze, wall_row + 1, bottom, left, wall_col - 1)
    # 右下区域
    dig_maze(maze, wall_row + 1, bottom, wall_col + 1, right)

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

# iimaze = [
#     ["# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# "],
#     ["# ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "# "],
#     ["# ", "# ", "  ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# "],
#     ["# ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "# ", "# ", "  ", "# ", "# ", "# ", "# ", "# ", "  ", "# ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "  ", "  ", "  ", "  ", "  ", "# ", "  ", "  ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "# ", "# ", "# ", "# ", "# ", "  ", "# ", "# ", "  ", "# ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "# ", "# ", "# ", "# ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "# ", "  ", "  ", "# ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "# ", "  ", "  ", "  ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "# ", "  ", "# ", "# ", "# ", "# ", "# ", "# ", "  ", "# ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "  ", "  ", "  ", "  ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "  ", "# ", "  ", "# ", "  ", "  ", "  ", "  ", "# ", "  ", "# ", "  ", "# ", "# "],
#     ["# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# ", "# "],
# ]
# print_maze(iimaze)
# 主程序
print("程序开始")

# 获取用户输入的迷宫尺寸
height = int(input("请输入迷宫的高度(至少5): "))
width = int(input("请输入迷宫的宽度(至少5): "))

# 初始化迷宫
maze = init_maze(height, width)
print("初始迷宫:")
print_maze(maze)

# 递归分割迷宫（内部区域，避开外边框）
dig_maze(maze, 1, height-2, 1, width-2)

# 添加外边框
add_border(maze)
print("最终迷宫（添加边框后）:")
print_maze(maze)

print("程序结束")