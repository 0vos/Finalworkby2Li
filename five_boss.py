import heapq
from input_output import load_data_from_json
import math
from collections import deque

# 定义函数 min_turns_to_defeat，用于计算击败所有 BOSS 所需的最少回合数
def min_turns_to_defeat(B, PlayerSkills):
    """
    计算击败所有 BOSS 所需的最少回合数。

    参数:
    B (list): 包含每个 BOSS 生命值的列表。
    PlayerSkills (list): 包含玩家技能的列表，每个技能是一个元组 (伤害值, 冷却回合数)。

    返回:
    dict: 包含原始输入数据、最少回合数和对应技能序列的字典。
    """
    # 获取 BOSS 的数量
    num_boss = len(B)
    # 获取玩家技能的数量
    num_skills = len(PlayerSkills)

    # 计算玩家技能的平均伤害值，用于估算打剩余血量要多少回合：
    avg_damage = sum(skill[0] for skill in PlayerSkills) / len(PlayerSkills)

    # 初始状态，格式为 (总代价, 已用回合数, 当前 BOSS 索引, 当前 BOSS 生命值, 技能冷却计数列表, 已使用技能序列)
    init_state = (0, 0, 0, B[0], [0] * num_skills, [])
    # 初始化优先队列，用于存储待探索的状态
    heap = [init_state]

    # 初始化最少回合数为正无穷大
    min_turns = float('inf')
    # 初始化最优技能序列为空列表
    best_actions = []

    # 用于记录已经访问过的状态，避免重复计算
    visited = {}

    # 当优先队列不为空时，继续探索
    while heap:
        # 每次从最小 f(n) 的状态开始展开 从优先队列中
        f_cost, turns, boss_idx, boss_hp, cooldowns, actions = heapq.heappop(heap)

        # 生成当前状态的唯一键，用于判断是否已经访问过
        key = (boss_idx, boss_hp, tuple(cooldowns))
        # 如果该状态已经访问过，且之前的回合数更少，则跳过
        if key in visited and visited[key] <= turns:
            continue
        # 记录当前状态的最少回合数
        visited[key] = turns

        # 如果所有 BOSS 都已被击败
        if boss_idx == num_boss:
            # 如果当前回合数比之前记录的最少回合数更少
            if turns < min_turns:
                # 更新最少回合数
                min_turns = turns
                # 更新最优技能序列
                best_actions = actions
            continue

        # 遍历玩家的所有技能
        for i, (damage, cd) in enumerate(PlayerSkills):
            # 如果该技能的冷却时间已过
            if cooldowns[i] == 0:
                # 计算使用该技能后当前 BOSS 的剩余生命值
                new_boss_hp = boss_hp - damage
                # 初始化新的 BOSS 索引
                new_boss_idx = boss_idx
                # 更新所有技能的冷却时间，冷却中的技能冷却时间减 1，最小为 0
                new_cooldowns = [max(c - 1, 0) for c in cooldowns]
                # 重置当前使用技能的冷却时间
                new_cooldowns[i] = cd
                # 更新已使用技能序列
                new_actions = actions + [i]
                # 回合数加 1
                new_turns = turns + 1

                # 如果当前 BOSS 被击败
                if new_boss_hp <= 0:
                    # 切换到下一个 BOSS
                    new_boss_idx += 1
                    # 如果还有未击败的 BOSS
                    if new_boss_idx < num_boss:
                        # 获取下一个 BOSS 的生命值
                        new_boss_hp = B[new_boss_idx]
                    else:
                        # 所有 BOSS 已击败，剩余生命值为 0
                        new_boss_hp = 0

                # 计算估计总代价，f(n) = 已用回合数 + 估算剩余回合数
                remaining_hp = sum(B[new_boss_idx:]) + (new_boss_hp if new_boss_idx < num_boss else 0)
                est_remain = remaining_hp / avg_damage
                f_score = new_turns + est_remain

                # 如果估计总代价大于等于当前记录的最少回合数，进行剪枝操作
                if f_score >= min_turns:
                    continue

                # 将新状态加入优先队列
                heapq.heappush(heap, (f_score, new_turns, new_boss_idx, new_boss_hp, new_cooldowns, new_actions))

    # 返回包含原始输入数据、最少回合数和对应技能序列的字典
    return {
        "B": B,
        "PlayerSkills": PlayerSkills,
        "min_turns": min_turns,
        "actions": best_actions
    }

if __name__ == "__main__":
    # 定义 JSON 文件路径
    file_path = "test_and_manual/样例/BOSS战样例/boss_case_1.json"
    # 从 JSON 文件中加载 BOSS 生命值数据
    B = load_data_from_json(file_path, "B")
    # 从 JSON 文件中加载玩家技能数据
    PlayerSkills = load_data_from_json(file_path, "PlayerSkills")
    # 调用 min_turns_to_defeat 函数计算最少回合数
    result = min_turns_to_defeat(B, PlayerSkills)
    import json
    # 以格式化的 JSON 字符串形式打印结果
    print(json.dumps(result, indent=2))