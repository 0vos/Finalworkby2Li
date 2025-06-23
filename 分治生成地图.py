import random
def init_maze(height, width):
    maze = [[' ' for _ in range(width)] for _ in range(height)]
    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

def add_wall(maze, index, direction):
    if direction == "row":
        maze[index][:] = '#'
    if direction == "col":
        maze[:][index] = '#'

def open_door(maze, row, col):
    if maze[row][col] == '#':
        maze[row][col] = ' '
    else:
        raise ValueError("已经是通路不需要挖墙")

def get_door_position(maze, row=':', col=':'):
    if row == ":" and col != ":":
        width = len(maze[0])
        row = random.randint(1, width - 2)  # 不包括左右的边界
        return row, col
    if col == ":" and row != ":":
        height = len(maze[0])
        col = random.randint(1, height - 2)  # 不包括左右的边界
        return row, col

def dig_maze(maze):
    height = len(maze)
    width = len(maze[0])
    
the_maze = init_maze(15, 15)
print_maze(the_maze)