import heapq
from 输入输出 import load_data_from_json
import math
from collections import deque


def min_turns_to_defeat(B, PlayerSkills):
    num_boss = len(B)
    num_skills = len(PlayerSkills)

    avg_damage = sum(skill[0] for skill in PlayerSkills) / len(PlayerSkills)

    # 初始状态：(总代价, 已用回合数, boss_idx, boss_hp, 冷却计数[], 技能序列)
    init_state = (0, 0, 0, B[0], [0] * num_skills, [])
    heap = [init_state]

    min_turns = float('inf')
    best_actions = []

    visited = {}

    while heap:
        f_cost, turns, boss_idx, boss_hp, cooldowns, actions = heapq.heappop(heap)

        key = (boss_idx, boss_hp, tuple(cooldowns))
        if key in visited and visited[key] <= turns:
            continue
        visited[key] = turns

        if boss_idx == num_boss:
            if turns < min_turns:
                min_turns = turns
                best_actions = actions
            continue

        for i, (damage, cd) in enumerate(PlayerSkills):
            if cooldowns[i] == 0:
                new_boss_hp = boss_hp - damage
                new_boss_idx = boss_idx
                new_cooldowns = [max(c - 1, 0) for c in cooldowns]
                new_cooldowns[i] = cd  # reset cooldown for this skill
                new_actions = actions + [i]
                new_turns = turns + 1

                # Boss被击败
                if new_boss_hp <= 0:
                    new_boss_idx += 1
                    if new_boss_idx < num_boss:
                        new_boss_hp = B[new_boss_idx]
                    else:
                        new_boss_hp = 0

                # f(n) = 已用回合数 + 估算剩余回合数
                remaining_hp = sum(B[new_boss_idx:]) + (new_boss_hp if new_boss_idx < num_boss else 0)
                est_remain = remaining_hp / avg_damage
                f_score = new_turns + est_remain

                if f_score >= min_turns:
                    continue  # 剪枝

                heapq.heappush(heap, (f_score, new_turns, new_boss_idx, new_boss_hp, new_cooldowns, new_actions))

    return {
        "B": B,
        "PlayerSkills": PlayerSkills,
        "min_turns": min_turns,
        "actions": best_actions
    }

if __name__ == "__main__":
    file_path = "样例/BOSS战样例/boss_case_1.json"
    B = load_data_from_json(file_path, "B")
    PlayerSkills = load_data_from_json(file_path, "PlayerSkills")
    result = min_turns_to_defeat(B, PlayerSkills)
    import json
    print(json.dumps(result, indent=2))