import heapq
import math
from collections import namedtuple

# 定义技能结构
Skill = namedtuple('Skill', ['damage', 'cooldown'])


# 定义状态节点
class StateNode:
    def __init__(self, boss_index, current_hp, cooldowns, turns, sequence):
        """
        初始化战斗状态节点
        
        参数:
        boss_index: 当前正在攻击的Boss索引
        current_hp: 当前Boss剩余血量
        cooldowns: 各技能剩余冷却时间
        turns: 已使用回合数
        sequence: 已使用的技能序列
        """
        self.boss_index = boss_index
        self.current_hp = current_hp
        self.cooldowns = cooldowns[:]  # 复制列表避免引用问题
        self.turns = turns
        self.sequence = sequence[:]    # 复制列表避免引用问题
        self.cost = 0  # 代价函数值 (f(n) = g(n) + h(n))
    
    def __lt__(self, other):
        """用于优先队列比较，代价小的优先"""
        return self.cost < other.cost
    
    def __repr__(self):
        """状态的可读表示"""
        return (f"StateNode(boss_index={self.boss_index}, current_hp={self.current_hp}, "
                f"cooldowns={self.cooldowns}, turns={self.turns}, sequence={self.sequence})")

def branch_and_bound_boss_battle(boss_hp_list, player_skills):
    """
    使用分支限界法求解多个BOSS战最优策略
    
    参数:
    boss_hp_list: BOSS血量列表
    player_skills: 玩家技能列表，每个技能为(damage, cooldown)
    
    返回:
    (min_turns, best_sequence): 最小回合数和对应的技能序列
    """
    # 将玩家技能转换为Skill对象
    skills = [Skill(damage, cooldown) for damage, cooldown in player_skills]
    
    # 计算玩家平均伤害（用于启发式函数）
    avg_damage = sum(skill.damage for skill in skills) / len(skills)
    
    # 计算所有Boss总血量（用于启发式函数）
    total_hp = sum(boss_hp_list)
    
    # 初始化优先队列 (最小堆)
    priority_queue = []
    
    # 初始状态: 第一个Boss满血，无冷却，0回合，空序列
    initial_cooldowns = [0] * len(skills)
    initial_node = StateNode(0, boss_hp_list[0], initial_cooldowns, 0, [])
    
    # 计算剩余总血量：当前Boss剩余 + 后续所有Boss
    remaining_hp = initial_node.current_hp + sum(boss_hp_list[1:])
    initial_node.cost = 0 + (remaining_hp / avg_damage)  # f(n) = g(n) + h(n)
    
    heapq.heappush(priority_queue, initial_node)
    
    # 记录最佳解
    best_turns = float('inf')
    best_sequence = None
    
    # 状态缓存: (boss_index, current_hp, cooldowns_tuple) -> 最小回合数
    state_cache = {}
    
    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        
        # 检查是否击败所有BOSS
        if current_node.boss_index >= len(boss_hp_list):
            if current_node.turns < best_turns:
                best_turns = current_node.turns
                best_sequence = current_node.sequence
            continue
        
        # 剪枝1: 当前代价已超过已知最优解
        if current_node.cost >= best_turns:
            continue
        
        # 状态缓存检查
        state_key = (current_node.boss_index, current_node.current_hp, tuple(current_node.cooldowns))
        if state_key in state_cache and state_cache[state_key] <= current_node.turns:
            continue
        state_cache[state_key] = current_node.turns
        
        # 尝试所有可用技能
        for idx, skill in enumerate(skills):
            # 技能不可用条件: 冷却中
            if current_node.cooldowns[idx] > 0:
                continue
            
            # 计算新状态
            new_boss_index = current_node.boss_index
            new_current_hp = current_node.current_hp - skill.damage
            
            # 更新冷却时间: 所有技能冷却-1，当前技能设置冷却
            new_cooldowns = [max(cd - 1, 0) for cd in current_node.cooldowns]
            new_cooldowns[idx] = skill.cooldown  # 设置当前技能的冷却时间
            
            # 新回合数和新序列
            new_turns = current_node.turns + 1
            new_sequence = current_node.sequence + [idx]
            
            # 如果当前Boss被击败，转移到下一个Boss
            if new_current_hp <= 0 and new_boss_index < len(boss_hp_list) - 1:
                new_boss_index += 1
                new_current_hp = boss_hp_list[new_boss_index]
                # 重置冷却时间（在击败Boss后所有冷却时间减少1）
                new_cooldowns = [max(cd - 1, 0) for cd in new_cooldowns]
            
            # 创建新节点
            new_node = StateNode(new_boss_index, new_current_hp, 
                                new_cooldowns, new_turns, new_sequence)
            
            # 计算剩余总血量：当前Boss剩余 + 后续所有Boss
            if new_node.boss_index < len(boss_hp_list):
                remaining_hp = new_node.current_hp + sum(boss_hp_list[new_node.boss_index+1:])
            else:
                remaining_hp = 0
            
            # 计算代价函数 f(n) = g(n) + h(n)
            # g(n) = 已用回合数
            # h(n) = 预估剩余回合数 = 剩余总血量 / 平均伤害
            new_node.cost = new_turns + (remaining_hp / avg_damage)
            
            # 剪枝2: 新代价已超过已知最优解
            if new_node.cost >= best_turns:
                continue
            
            # 将新节点加入优先队列
            heapq.heappush(priority_queue, new_node)
    
    return best_turns, best_sequence

# 测试样例
if __name__ == "__main__":
    # 输入数据
    input_data = {
        "B": [11, 13, 8, 17],
        "PlayerSkills": [[6, 2], [2, 0], [4, 1]]
    }
    
    # 求解最优策略
    min_turns, best_sequence = branch_and_bound_boss_battle(
        input_data["B"], input_data["PlayerSkills"]
    )
    print(1111)
    # 输出结果
    print(f"击败所有BOSS的最小回合数: {min_turns}")
    print(f"最优技能序列: {best_sequence}")
    print(f"技能说明:")
    for i, skill in enumerate(input_data["PlayerSkills"]):
        print(f"  技能{i}: 伤害={skill[0]}, 冷却={skill[1]}")
    
    # 验证样例
    expected = {"min_turns": 13, "actions": [0,2,1,2,0,2,1,0,1,2,0,1,2]}
    print("\n预期结果:")
    print(f"  最小回合数: {expected['min_turns']}")
    print(f"  技能序列: {expected['actions']}")