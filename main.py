import argparse
import random

import numpy as np


# 与えられたマップを90°回転させるメソッド
def rotate_map(small_map):
    # 転置行列を求めるプログラム
    h = len(small_map)
    w = len(small_map[0])
    trans_map = np.zeros((w, h))
    for i in range(h):
        for j in range(w):
            trans_map[j][i] = small_map[i][j]
    # 最後に上下をひっくり返す
    rotate_map = invers_map(trans_map)
    return rotate_map


# 与えられたマップの上下を反転させるメソッド
def invers_map(small_map):
    h = len(small_map)
    w = len(small_map[0])
    invers_map = np.zeros((h, w))
    for i in range(h):
        invers_map[h - 1 - i] = small_map[i]
    return invers_map


# 与えられたマップを結合して大きいマップを作るメソッド
# ↓マップを結合する順番
# 0 3
# 1 2
def joint_1517map(small_map0, gap_map0):
    s_h = len(small_map0)
    s_w = len(small_map0[0])
    h = 17
    w = 15
    small_map1 = rotate_map(small_map0)
    small_map2 = rotate_map(small_map1)
    small_map3 = rotate_map(small_map2)
    gap_map1 = rotate_map(rotate_map(gap_map0))
    big_map = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            if i < s_w:  # upper
                if j < s_w:  # area 0
                    big_map[i][j] = small_map0[i][j]
                else:  # area3
                    big_map[i][j] = small_map3[i][j - s_w]
            elif i > h - s_h:  # lower
                if j < s_h:  # area 1
                    big_map[i][j] = small_map1[i - (h - s_w)][j]
                else:  # area 2
                    big_map[i][j] = small_map2[i - (h - s_h)][j - s_h]
            elif i == 7:  # area 0, 2 and gap
                if j < s_w:
                    big_map[i][j] = small_map0[i][j]
                else:
                    big_map[i][j] = gap_map1[0][j - s_w]
            elif i == 8:
                if j < s_w:
                    big_map[i][j] = gap_map0[0][j]
                elif j > w - s_h:
                    big_map[i][j] = gap_map1[1][j - (s_h - 1)]
                else:
                    big_map[i][j] = 3
            elif i == 9:
                if j > w - s_h:
                    big_map[i][j] = small_map2[i - (h - s_h)][j - s_h]
                else:
                    big_map[i][j] = gap_map0[1][j]

    return big_map


# ランダムに壁とアイテムを配置するメソッド
def random_map(small_map, block, item):
    h = len(small_map)
    w = len(small_map[0])
    block_num = random.randint(block[0], block[1])
    item_num = random.randint(item[0], item[1])
    rs_map = np.zeros((h, w))

    # アイテムの配置
    counter = 0
    while True:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if rs_map[y][x] == 0:
            rs_map[y][x] = 3
            counter += 1
        if counter >= item_num:
            break

    # ブロックの配置
    counter = 0
    while True:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if rs_map[y][x] == 0 and x != 0 and y != 0:
            rs_map[y][x] = 2
            counter += 1
        if counter >= block_num:
            break

    return rs_map


def setAgent(map):
    agent_position = np.zeros((2, 2))
    # Cool
    agent_position[0][0] = random.randint(0, 6)  # x
    agent_position[0][1] = random.randint(0, 16)  # y
    # Hot
    agent_position[1][0] = 14 - agent_position[0][0]  # x
    agent_position[1][1] = 16 - agent_position[0][1]  # y
    agent_position = agent_position.astype(int)
    if agent_position[0][1] < 7:
        map[agent_position[0][1]][agent_position[0][0]] = 0
        map[agent_position[1][1]][agent_position[1][0]] = 0
        map[agent_position[0][1] + 9][agent_position[0][0]] = 0
        map[agent_position[1][1] - 9][agent_position[1][0]] = 0
    elif agent_position[0][1] > 9:
        map[agent_position[0][1]][agent_position[0][0]] = 0
        map[agent_position[1][1]][agent_position[1][0]] = 0
        map[agent_position[0][1] - 9][agent_position[0][0]] = 0
        map[agent_position[1][1] + 9][agent_position[1][0]] = 0
    return map, agent_position


# マップを作るメソッド
def make_map(block_max, item_max):
    # 元となる小さいマップを作りそれを回転させて結合することでランダムマップを実現する
    # 隙間が開くためそれを埋める, 隙間マップも作成する

    # 小マップの大きさ
    small_w = 7
    small_h = 8
    # 隙間マップの大きさ
    gap_w = 8
    gap_h = 2

    # 小マップのブロック, アイテムの数
    small_block = [5, 8]
    small_item = [6, 10]
    # 隙間マップのブロック, アイテムの数
    gap_block = [0, 3]
    gap_item = [0, 4]

    # 小マップの生成
    small_map = np.zeros((small_h, small_w))
    small_map = random_map(small_map, small_block, small_item)
    # 隙間マップの生成
    gap_map = np.zeros((gap_h, gap_w))
    gap_map = random_map(gap_map, gap_block, gap_item)
    gap_map[0][7] = 3

    # マップを結合して完成させる
    entire_map = joint_1517map(small_map, gap_map)
    entire_map, agent_position = setAgent(entire_map)
    entire_map = entire_map.astype(int)
    return entire_map, agent_position


# マップファイル出力
def output_map(file_path, file_num, map, time, agent_position):
    with open(f"{file_path}{file_num}.map", "w") as f:
        f.write(f"N:generated{file_num}\n")
        f.write(f"T:{time}\n")
        f.write("S:15,17\n")
        for i in range(17):
            f.write(f"D:{map[i][0]}")
            for j in range(14):
                f.write(f",{map[i][j+1]}")
            f.write("\n")
        f.write(f"C:{agent_position[0][0]},{agent_position[0][1]}\n")
        f.write(f"H:{agent_position[1][0]},{agent_position[1][1]}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("generateNum", help="")
    parser.add_argument("-b", "--blockNum", help="")
    parser.add_argument("-i", "--itemNum", help="")
    args = parser.parse_args()

    try:
        generate_num = int(args.generateNum)
    except Exception as e:
        print(f"エラーが発生しました : {e}")

    if args.blockNum is None:
        block_num = 9
    else:
        block_num = args.blockNum
    if args.itemNum is None:
        item_num = 10
    else:
        item_num = args.itemNum

    for i in range(generate_num):
        entire_map, agent_position = make_map(block_num, item_num)
        output_map("./generated_map/", f"RandMap_{i}", entire_map, 120, agent_position)


if __name__ == "__main__":
    main()
