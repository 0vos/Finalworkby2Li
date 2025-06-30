import heapq

# 定义技能
class Skill:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown

# 玩家技能配置
skills = [
    Skill("普通攻击", damage=5, cooldown=0),
    Skill("大招", damage=10, cooldown=2)
]

# 状态节点
class Node:
    def __init__(self, turn, boss_hp, cooldowns, sequence):
        self.turn = turn                  # 当前回合
        self.boss_hp = boss_hp            # BOSS 剩余血量
        self.cooldowns = cooldowns[:]     # 技能冷却状态
        self.sequence = sequence[:]       # 技能使用序列

    def __lt__(self, other):
        # 优先队列比较函数：估价函数越小越优先
        return self.cost() < other.cost()

    def cost(self):
        avg_damage = 7  # 简化估计平均伤害（可改进）
        return self.turn + self.boss_hp / avg_damage

# 分支限界主函数
def boss_battle_branch_and_bound(boss_hp_init=25):
    min_turns = float('inf')
    best_sequence = None

    # 初始节点：0回合，BOSS满血，技能全冷却0
    initial_node = Node(
        turn=0,
        boss_hp=boss_hp_init,
        cooldowns=[0 for _ in skills],
        sequence=[]
    )

    heap = []
    heapq.heappush(heap, initial_node)

    while heap:
        current = heapq.heappop(heap)

        # 如果 boss 被击败
        if current.boss_hp <= 0:
            if current.turn < min_turns:
                min_turns = current.turn
                best_sequence = current.sequence
            continue

        # 剪枝：如果已经用了的回合 >= 当前最优回合数
        if current.turn >= min_turns:
            continue

        # 每种技能尝试分支
        for idx, skill in enumerate(skills):
            if current.cooldowns[idx] == 0:  # 技能可用
                next_boss_hp = current.boss_hp - skill.damage
                next_cooldowns = [max(cd - 1, 0) for cd in current.cooldowns]
                next_cooldowns[idx] = skill.cooldown  # 重置该技能冷却
                next_sequence = current.sequence + [skill.name]

                next_node = Node(
                    turn=current.turn + 1,
                    boss_hp=next_boss_hp,
                    cooldowns=next_cooldowns,
                    sequence=next_sequence
                )

                heapq.heappush(heap, next_node)

    return min_turns, best_sequence


# 调用示例
if __name__ == "__main__":
    turns, sequence = boss_battle_branch_and_bound(boss_hp_init=25)
    print("击败BOSS所需最少回合数：", turns)
    print("技能使用顺序：", " → ".join(sequence))
