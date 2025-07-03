import json

from test_and_manual.样例.Lock import PasswordLock
from input_output import load_data_from_json
import os
# import ast

def is_prime(d):
    return d in [2, 3, 5, 7]


def is_valid(pwd_digits, clues):
    d1, d2, d3 = pwd_digits
    for clue in clues:
        if len(clue) == 3:
            # 固定某一位的数字
            for i in range(3):
                if clue[i] != -1 and pwd_digits[i] != clue[i]:
                    return False
        elif len(clue) == 2:
            if clue == [-1, -1]:
                # 每位为素数且不重复
                if not (is_prime(d1) and is_prime(d2) and is_prime(d3)):
                    return False
                if len(set(pwd_digits)) != 3:
                    return False
            else:
                pos, kind = clue
                digit = pwd_digits[pos - 1]
                if kind == 0 and digit % 2 != 0:  # 要求偶数
                    return False
                if kind == 1 and digit % 2 != 1:  # 要求奇数
                    return False
    return True


def solve_with_backtracking(clues, target_hash):
    lock = PasswordLock()
    result = []
    tries = [0]
    found = [False]
    gets = [0]

    def dfs(pos, path):
        if found[0]:
            return

        if pos == 3:
            if is_valid(path, clues):
                tries[0] += 1
                pwd_str = ''.join(map(str, path))
                if lock.hash_password(pwd_str) == target_hash:
                    print(f"找到了密码: {pwd_str}")
                    result.append(pwd_str)
                    found[0] = True
                    gets[0] += 100  # 破解成功加100金币
                else:
                    gets[0] -= 1  # 符合条件但是没输入正确依然扣金币
            # else: 不符合线索的路径不算尝试，不扣金币
            return

        for digit in range(10):
            path.append(digit)
            dfs(pos + 1, path)
            path.pop()

    dfs(0, [])
    print(f"总共尝试次数: {tries[0]}")
    print(f"最终金币变化数: {gets[0]}")
    if not result:
        print("没有找到密码")
    return result, gets[0], tries[0]


def L_generator():
    locker = PasswordLock()
    password = input("请输入一个3位数字密码：")
    L = locker.hash_password(password)
    return L

# 示例输入
if __name__ == "__main__":
    # 多文件文件输入输出
    input_dir = 'test_and_manual/password测试集/password_test'  # 原始文件所在的目录
    output_json_dir = 'password_result_student'  # 每个文件的结果保存的目录
    summary_file = 'summary.txt'  # 汇总结果文件

    os.makedirs(output_json_dir, exist_ok=True)

    total_tries = 0

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            C = load_data_from_json(filepath, "C")
            L = load_data_from_json(filepath, "L")
            password, coins, tries = solve_with_backtracking(C, L)

            result = {
                "C": C,
                "L": L,
                "password": password,
                "tries": tries
            }
            json_path = os.path.join(output_json_dir, filename + '.json')
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(result, jf, ensure_ascii=False, indent=2)

            total_tries += tries

    with open(summary_file, 'w', encoding='utf-8') as sf:
        sf.write(f"次数总和：{total_tries}\n")

  #   # 单独的情况
  #   position = (0, 0)
  #   C = [
  #   [-1,-1],
  #   [-1,2,-1],
  #   [3,1]
  # ]
  #   # C = [
  #   #     [-1, 7, -1],
  #   #     [1, 1],
  #   #     [2, 1]
  #   # ]
  #   L = L_generator()
  #   # L = "ef489e31e9f932ff343749a1f66f5132e4392161979ab6c75f7958b2107aa3aa"
  #   password, coins, tries = solve_with_backtracking(C, L)
  #   print(f"密码：{password[0]}, 金币变化：{coins}")
