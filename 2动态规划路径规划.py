the_maze = [
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
    ["#","G","T"," ","T","G","#","G","T"," "," "," ","#"," ","#"],
    ["#","#","#"," ","#","#","#","#","#"," ","#"," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#","G","#"," ","#"," ","#","B","S"],
    ["#"," ","#"," ","#"," ","#","T","#"," ","#"," ","#"," ","#"],
    ["#"," "," "," "," "," "," "," "," ","T","#"," "," ","L","#"],
    ["#"," ","#"," ","#","#","#","#","#","#","#","#","#"," ","#"],
    ["#"," ","#"," "," "," ","#"," ","#","T","T"," "," "," ","#"],
    ["#"," ","#","#","#","#","#","G","#","#","#"," ","#"," ","#"],
    ["#","T"," "," "," ","G","#"," "," "," "," "," ","#"," ","#"],
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","T","#"],
    ["#","T","#"," "," "," "," "," "," "," ","#"," ","T","T","#"],
    ["#","G","#"," ","#","T","#"," ","#"," ","#"," ","#"," ","#"],
    ["#"," "," "," ","#","G","#"," ","#","G"," "," ","#"," ","#"],
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","E","#"]
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

    sx, sy = start
    q = deque()
    q.append((sx, sy, frozenset(), 0))  # x, y, coins_taken_set, current_score

    visited = dict()  # key: (x, y, frozenset(coins_taken)) → score
    prev = dict()  # 用于路径回溯
    final_key = None

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        x, y, taken, score = q.popleft()

        key = (x, y, taken)
        if key in visited and visited[key] >= score:
            continue
        visited[key] = score

        if (x, y) == end:
            if final_key is None or score > visited[final_key]:
                final_key = key

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and maze[nx][ny] != "#":
                cell = maze[nx][ny]
                gain = 0
                new_taken = set(taken)
                if cell == "G" and (nx, ny) not in taken:
                    gain = 5
                    new_taken.add((nx, ny))
                elif cell == "T" and (nx, ny) not in taken:
                    gain = -3
                    new_taken.add((nx, ny))
                new_key = (nx, ny, frozenset(new_taken))
                if new_key in visited and visited[new_key] >= score + gain:
                    continue
                q.append((nx, ny, frozenset(new_taken), score + gain))
                prev[new_key] = key

    def reconstruct_path(end_key):
        path = []
        key = end_key
        print("开始回溯路径:")
        while key in prev:
            # print(f"回溯: 当前坐标=({key[0]}, {key[1]}), 已收金币数={len(key[2])}, 当前得分={visited.get(key, '?')}")
            path.append((key[0], key[1]))
            key = prev[key]
        path.append((sx, sy))
        print(f"总步数: {len(path)}")
        print("路径坐标列表:")
        for step in reversed(path):
            print(step)
        return path[::-1]

    def visualize_path(maze, path):
        maze_copy = [row[:] for row in maze]
        # count = 0
        for i, j in path:
            if maze_copy[i][j] not in ("S", "E"):
                maze_copy[i][j] = "."
                # count += 1
        print("最优路径图:")
        for row in maze_copy:
            print("".join(row))

    if final_key:
        path = reconstruct_path(final_key)
        visualize_path(maze, path)
        return visited[final_key]
    return None

start_pos, end_pos = get_start_end(the_maze)
max_c = max_coins(the_maze, start_pos, end_pos)
print(max_c)
