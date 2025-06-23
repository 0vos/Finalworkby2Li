
def init_maze(height, width):
    maze = [[' ' for _ in range(width)] for _ in range(height)]
    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

def add_wall(maze, index, direction):
    if direction == ""

the_maze = init_maze(15, 15)
print_maze(maze)