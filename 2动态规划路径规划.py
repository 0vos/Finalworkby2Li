from collections import deque
the_maze = [
    list("#S#############"),
    list("#OOBOOOOOOO#OO#"),
    list("###O#OOOTOO#OO#"),
    list("#OGO#OOOOOGOOO#"),
    list("######O#####OO#"),
    list("#OOOOOLOOOO#OO#"),
    list("########O######"),
    list("#OOOBOOOTOO#OO#"),
    list("#O##########OO#"),
    list("#OO#OOOOOBOOOO#"),
    list("#TO#O#OOOOG#OO#"),
    list("#OO#O#######OO#"),
    list("#OO#OOOOLOO#OO#"),
    list("#OLOO#OOOOO#OOE"),
    list("###############"),
]
def get_start_end(maze):
    print("初始化开始")
    start = (0, 0)
    end = (0, 0)
    for r_index, row in enumerate(maze):
        for c_index, char in enumerate(row):
            if char == "S":
                start = (r_index, c_index)
            elif char == "E":
                end = (r_index, c_index)
    print("初始化结束")
    return start, end

def max_coins(maze, start, end):
    print("开始寻找")
    h, w = len(maze), len(maze[0])
    from collections import deque

    def print_dp_state(state_dict):
        print("当前最大金币值状态（部分路径片段）:")
        for (x, y, collected), val in list(state_dict.items())[:10]:  # 只打印前10条状态以免太长
            print(f"({x},{y}) coins={val} collected={len(collected)}")

    sx, sy = start
    q = deque()
    q.append((sx, sy, frozenset(), 0))  # x, y, coins_taken_set, current_score

    visited = dict()  # key: (x, y, frozenset(coins_taken)) → score
    max_result = -float('inf')

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        x, y, taken, score = q.popleft()

        key = (x, y, taken)
        if key in visited and visited[key] >= score:
            continue
        visited[key] = score

        if (x, y) == end:
            max_result = max(max_result, score)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and maze[nx][ny] != "#":
                cell = maze[nx][ny]
                gain = 0
                new_taken = set(taken)
                if cell == "G" and (nx, ny) not in taken:
                    gain = 5
                    new_taken.add((nx, ny))
                elif cell == "T":
                    gain = -3
                q.append((nx, ny, frozenset(new_taken), score + gain))

    return max_result if max_result != -float('inf') else None

start_pos, end_pos = get_start_end(the_maze)
max_c = max_coins(the_maze, start_pos, end_pos)
print(max_c)

# def init_dp_table(maze):
#     dp_table = []
#     start_position = (0, 0)
#     exit_position = (0, 0)
#     for row_index, row in enumerate(maze):
#         dp_row = []
#         for col_index, char in enumerate(row):
#             if char == "#":
#                 dp_row.append('#')
#             elif char == "S":
#                 start_position = (row_index, col_index)
#                 dp_row.append(0)
#             elif char == "E":
#                 exit_position = (row_index, col_index)
#                 dp_row.append(0)
#             else:
#                 dp_row.append(0)
#         dp_table.append(dp_row)
#     return dp_table, start_position, exit_position
#
# def print2d(maze):
#     a_maze = []
#     for row in maze:
#         tmp_row = []
#         for elem in row:
#             if isinstance(elem, int):
#                 elem = str(elem)
#             tmp_row.append(elem)
#         a_maze.append(tmp_row)
#     for row in a_maze:
#         print(''.join(row))
#
# def count_coins(maze, old_coins, row_index, col_index):
#     if maze[row_index][col_index] == 'G':
#         return old_coins + 5
#     elif maze[row_index][col_index] == 'T':
#         return old_coins - 3
#     else:
#         return old_coins
#
# def dp_way(maze, dp_table, start_position, exit_position):
#     height, width = len(maze), len(maze[0])
#     coins = 0
#     i = start_position[0]
#     j = start_position[1]
#     while (i, j) != exit_position:
#         if i - 1 >=0 and dp_table[i - 1][j] == 0:
#             coins = count_coins(maze, coins, i)
#
#
# the_dp_table, start_pos, exit_pos = init_dp_table(the_maze)
# print2d(the_dp_table)