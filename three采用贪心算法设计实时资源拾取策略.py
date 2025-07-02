
# from collections import deque
# import heapq

# # 玩家视野范围
# VIEW_RANGE = 1

# # 资源价值
# RESOURCE_VALUE = {'G': 50, 'T': -30, ' ': 0, 'L': 0, 'B': 0, 'E': 0}
# WALL = '#'
# DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# # 检查位置是否合法
# def is_valid(maze, x, y):
#     return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != WALL

# # 获取当前位置的3x3视野
# def get_vision(maze, pos):
#     x, y = pos
#     vision = {}
#     for dx in range(-VIEW_RANGE, VIEW_RANGE + 1):
#         for dy in range(-VIEW_RANGE, VIEW_RANGE + 1):
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
#                 vision[(nx, ny)] = maze[nx][ny]
#     return vision

# # A*搜索
# def astar(maze, start, goal):
#     heap = []
#     heapq.heappush(heap, (0, start))
#     came_from = {}
#     cost_so_far = {start: 0}

#     while heap:
#         _, current = heapq.heappop(heap)
#         if current == goal:
#             break
#         for dx, dy in DIRS:
#             nx, ny = current[0] + dx, current[1] + dy
#             if is_valid(maze, nx, ny):
#                 new_cost = cost_so_far[current] + 1
#                 next_node = (nx, ny)
#                 if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
#                     cost_so_far[next_node] = new_cost
#                     priority = new_cost + abs(goal[0]-nx) + abs(goal[1]-ny)
#                     heapq.heappush(heap, (priority, next_node))
#                     came_from[next_node] = current

#     path = []
#     node = goal
#     while node != start:
#         if node not in came_from:
#             return []
#         path.append(node)
#         node = came_from[node]
#     path.append(start)
#     path.reverse()
#     return path

# # 资源采集 + 探索
# def explore_and_collect(maze, start):
#     pos = start
#     collected_path = [pos]
#     visited = {}
#     max_steps = 500
#     step_count = 0

#     discovered_exit = None

#     while step_count < max_steps:
#         step_count += 1
#         vision = get_vision(maze, pos)

#         # 优先检测出口
#         for vpos, val in vision.items():
#             if val == 'E':
#                 discovered_exit = vpos
#                 break
#         if discovered_exit:
#             break

#         # 选择视野中价值最高的位置移动（考虑资源价值 - 惩罚）
#         best_score = float('-inf')
#         next_move = None
#         for vpos, val in vision.items():
#             if vpos == pos or maze[vpos[0]][vpos[1]] == WALL:
#                 continue
#             val_score = RESOURCE_VALUE.get(val, 0)
#             penalty = visited.get(vpos, 0) * 32
#             score = val_score - penalty
#             if score > best_score:
#                 best_score = score
#                 next_move = vpos

#         if not next_move:
#             break  # 无资源可采，停止

#         path = astar(maze, pos, next_move)
#         for p in path[1:]:
#             collected_path.append(p)
#             visited[p] = visited.get(p, 0) + 1
#             if maze[p[0]][p[1]] == 'G':
#                 maze[p[0]][p[1]] = ' '
#             pos = p

#     return pos, collected_path, discovered_exit

# # BFS导航至出口
# def bfs_to_exit(maze, start, goal):
#     queue = deque([start])
#     visited = {start}
#     parent = {}
#     while queue:
#         x, y = queue.popleft()
#         if (x, y) == goal:
#             break
#         for dx, dy in DIRS:
#             nx, ny = x + dx, y + dy
#             if is_valid(maze, nx, ny) and (nx, ny) not in visited:
#                 visited.add((nx, ny))
#                 parent[(nx, ny)] = (x, y)
#                 queue.append((nx, ny))

#     path = []
#     node = goal
#     while node != start:
#         if node not in parent:
#             return []
#         path.append(node)
#         node = parent[node]
#     path.append(start)
#     path.reverse()
#     return path

# # 测试入口
# if __name__ == "__main__":
#     maze = [
#     list("###########S###"),
#     list("# GTG#        #"),
#     list("###G### #######"),
#     list("# T   #   # #G#"),
#     list("### # ### # #G#"),
#     list("# G # #G    GT#"),
#     list("### # #####T#T#"),
#     list("# # # #     # #"),
#     list("#T# # ### ### #"),
#     list("#   #       # #"),
#     list("# #############"),
#     list("#   #G# T #GT #"),
#     list("### #T# ##### #"),
#     list("#    L  B   TG#"),
#     list("#########E#####")

# ]


#     start = (0, 1)
#     print("初始迷宫：")
#     for row in maze:
#         print(''.join(row))

#     final_pos, collect_path, exit_pos = explore_and_collect(maze, start)

#     print("\n资源拾取路径：")
#     print(collect_path)

#     if exit_pos:
#         exit_path = bfs_to_exit(maze, final_pos, exit_pos)
#         print("\n出口路径：")
#         print(exit_path)
#     else:
#         print("\n未发现出口！")

#     input("\n程序结束，按 Enter 键退出...")


from collections import deque
import heapq

# 玩家视野范围
VIEW_RANGE = 1

# 资源价值
RESOURCE_VALUE = {'G': 50, 'T': -30, ' ': 0, 'L': 0, 'B': 0, 'E': 0}
WALL = '#'
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 检查位置是否合法
def is_valid(maze, x, y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != WALL

# 获取当前位置的3x3视野
def get_vision(maze, pos):
    x, y = pos
    vision = {}
    for dx in range(-VIEW_RANGE, VIEW_RANGE + 1):
        for dy in range(-VIEW_RANGE, VIEW_RANGE + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                vision[(nx, ny)] = maze[nx][ny]
    return vision

# A*搜索
def astar(maze, start, goal):
    heap = []
    heapq.heappush(heap, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        for dx, dy in DIRS:
            nx, ny = current[0] + dx, current[1] + dy
            if is_valid(maze, nx, ny):
                new_cost = cost_so_far[current] + 1
                next_node = (nx, ny)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + abs(goal[0]-nx) + abs(goal[1]-ny)
                    heapq.heappush(heap, (priority, next_node))
                    came_from[next_node] = current

    path = []
    node = goal
    while node != start:
        if node not in came_from:
            return []
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path

# 资源采集 + 探索
def explore_and_collect(maze, start):
    pos = start
    collected_path = [pos]
    visited = {}
    max_steps = 500
    step_count = 0
    discovered_exit = None
    
    # 初始化资源总值
    total_resource = 0
    
    # 处理起点位置的资源（如果有）
    start_val = maze[start[0]][start[1]]
    if start_val in RESOURCE_VALUE:
        total_resource += RESOURCE_VALUE[start_val]
        # 如果是黄金，收集后移除
        if start_val == 'G':
            maze[start[0]][start[1]] = ' '
    
    # 起点也算一步，扣除0.01
    total_resource -= 0.01

    while step_count < max_steps:
        step_count += 1
        vision = get_vision(maze, pos)

        # 优先检测出口
        for vpos, val in vision.items():
            if val == 'E':
                discovered_exit = vpos
                break
        if discovered_exit:
            break

        # 选择视野中价值最高的位置移动（考虑资源价值 - 惩罚）
        best_score = float('-inf')
        next_move = None
        for vpos, val in vision.items():
            if vpos == pos or maze[vpos[0]][vpos[1]] == WALL:
                continue
            val_score = RESOURCE_VALUE.get(val, 0)
            penalty = visited.get(vpos, 0) * 32  # 增加惩罚因子
            score = val_score - penalty
            if score > best_score:
                best_score = score
                next_move = vpos

        if not next_move:
            break  # 无资源可采，停止

        path = astar(maze, pos, next_move)
        for p in path[1:]:
            collected_path.append(p)
            visited[p] = visited.get(p, 0) + 1
            
            # 处理当前位置的资源
            cell_value = maze[p[0]][p[1]]
            if cell_value in RESOURCE_VALUE:
                total_resource += RESOURCE_VALUE[cell_value]
                # 如果是黄金，收集后移除
                if cell_value == 'G':
                    maze[p[0]][p[1]] = ' '
            
            # 每走一步扣除0.002
            total_resource -= 0.002
            
            pos = p

    return total_resource, pos, collected_path, discovered_exit

# BFS导航至出口
def bfs_to_exit(maze, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {}
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if is_valid(maze, nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    path = []
    node = goal
    while node != start:
        if node not in parent:
            return []
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return path

# 测试入口
if __name__ == "__main__":
    maze = [
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

    start = (0, 12)  # 修正起点位置为S的位置
    
    print("初始迷宫：")
    for row in maze:
        print(''.join(row))

    # 获取资源总值和路径
    total_resource, final_pos, collect_path, exit_pos = explore_and_collect(maze, start)

    print("\n资源拾取路径：")
    print(collect_path)
    
    # 打印资源总值
    print(f"\n资源总值: {total_resource:.2f}")

    if exit_pos:
        exit_path = bfs_to_exit(maze, final_pos, exit_pos)
        print("\n出口路径：")
        print(exit_path)
        
        # 计算出口路径上的资源变化
        for p in exit_path[1:]:
            # 处理出口路径上的资源
            cell_value = maze[p[0]][p[1]]
            if cell_value in RESOURCE_VALUE:
                total_resource += RESOURCE_VALUE[cell_value]
                # 如果是黄金，收集后移除
                if cell_value == 'G':
                    maze[p[0]][p[1]] = ' '
            
            # 每走一步扣除0.01
            total_resource -= 0.002
            
        # 打印最终资源总值
        print(f"\n最终资源总值: {total_resource:.2f}")
    else:
        print("\n未发现出口！")
        print(f"最终资源总值: {total_resource:.2f}")

    input("\n程序结束，按 Enter 键退出...")

