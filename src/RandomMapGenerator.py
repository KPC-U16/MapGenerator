import argparse
import os
import random

import numpy as np
import numpy.typing as npt


# 与えられたマップを90°回転させるメソッド
def rotateMap(
    small_map: npt.NDArray[npt.NDArray[int]],
) -> npt.NDArray[npt.NDArray[int]]:
    # 転置行列を求めるプログラム
    h = len(small_map)
    w = len(small_map[0])
    trans_map = np.zeros((w, h), dtype="int64")
    for i in range(h):
        for j in range(w):
            trans_map[j][i] = small_map[i][j]
    # 最後に上下をひっくり返す
    rotate_map = inversMap(trans_map)
    return rotate_map


# 与えられたマップの上下を反転させるメソッド
def reverseMap(
    small_map: npt.NDArray[npt.NDArray[int]],
) -> npt.NDArray[npt.NDArray[int]]:
    h = len(small_map)
    w = len(small_map[0])
    invers_map = np.zeros((h, w), dtype="int64")
    for i in range(h):
        invers_map[h - 1 - i] = small_map[i]
    return invers_map


# 与えられたマップを結合して大きいマップを作るメソッド
# ↓マップを結合する順番
# 0 3
# 1 2
def jointMap(
    small_map0: npt.NDArray[npt.NDArray[int]], gap_map0: npt.NDArray[npt.NDArray[int]]
) -> npt.NDArray[npt.NDArray[int]]:
    s_h = len(small_map0)
    s_w = len(small_map0[0])
    h = 17
    w = 15
    small_map1 = rotateMap(small_map0)
    small_map2 = rotateMap(small_map1)
    small_map3 = rotateMap(small_map2)
    gap_map1 = rotateMap(rotateMap(gap_map0))
    big_map = np.zeros((h, w))

    # 2次元配列のインデックスによって, 結合するリストを変更するプログラム
    # 結合する場所については, このメソッド定義場所のコメントを参照
    # 上側, 下側, 真ん中(3行)のそれぞれに別れている

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
            elif i == 7:  # area 2 and gap
                if j < s_w:
                    big_map[i][j] = small_map0[i][j]
                else:
                    big_map[i][j] = gap_map1[0][j - s_w]
            elif i == 8:  # area gap and center
                if j < s_w:
                    big_map[i][j] = gap_map0[0][j]
                elif j > w - s_h:
                    big_map[i][j] = gap_map1[1][j - (s_h - 1)]
                else:
                    big_map[i][j] = 3
            elif i == 9:  # area 2 and gap
                if j > w - s_h:
                    big_map[i][j] = small_map2[i - (h - s_h)][j - s_h]
                else:
                    big_map[i][j] = gap_map0[1][j]

    return big_map


# ランダムに壁とアイテムを配置するメソッド
def layoutRandomMap(
    small_map: npt.NDArray[npt.NDArray[int]], block: list[int], item: list[int]
) -> npt.NDArray[npt.NDArray[int]]:
    h = len(small_map)
    w = len(small_map[0])
    block_num = random.randint(block[0], block[1])
    item_num = random.randint(item[0], item[1])
    rs_map = np.zeros((h, w))

    # アイテムの配置
    # アイテムの位置をランダムに決定し, 配置する
    # もし, ランダムに選んだ地点に既に何かしらがある場合は処理を飛ばす
    # 規定の数のアイテムを設置するまでループする
    item_counter = 0
    while True:
        item_position_x = random.randint(0, w - 1)
        item_position_y = random.randint(0, h - 1)
        if rs_map[item_position_y][item_position_x] == 0:
            rs_map[item_position_y][item_position_x] = 3
            item_counter += 1
        if item_counter >= item_num:
            break

    # ブロックの配置
    # ブロックの位置をランダムに決定し, 配置する
    # もし, ランダムに選んだ地点に既に何かしらがある場合は処理を飛ばす
    # 規定の数のブロック設置するまでループする
    # ルール上, 最外周にはブロックを設置できないため, ランダムで0が選択されないようにする
    block_counter = 0
    while True:
        block_position_x = random.randint(1, w - 1)
        block_position_y = random.randint(1, h - 1)
        if rs_map[block_position_y][block_position_x] == 0:
            rs_map[block_position_y][block_position_x] = 2
            block_counter += 1
        if block_counter >= block_num:
            break

    return rs_map


def setAgent(
    entire_map: npt.NDArray[npt.NDArray[int]],
) -> tuple[npt.NDArray[npt.NDArray[int]], npt.NDArray[npt.NDArray[int]]]:
    agent_position = np.zeros((2, 2))
    # Cool
    agent_position[0][0] = random.randint(0, 6)  # x
    agent_position[0][1] = random.randint(0, 16)  # y
    # Hot
    agent_position[1][0] = 14 - agent_position[0][0]  # x
    agent_position[1][1] = 16 - agent_position[0][1]  # y
    agent_position = agent_position.astype(int)
    if agent_position[0][1] < 7:
        entire_map[agent_position[0][1]][agent_position[0][0]] = 0
        entire_map[agent_position[1][1]][agent_position[1][0]] = 0
        entire_map[agent_position[0][1] + 9][agent_position[0][0]] = 0
        entire_map[agent_position[1][1] - 9][agent_position[1][0]] = 0
    elif agent_position[0][1] > 9:
        entire_map[agent_position[0][1]][agent_position[0][0]] = 0
        entire_map[agent_position[1][1]][agent_position[1][0]] = 0
        entire_map[agent_position[0][1] - 9][agent_position[0][0]] = 0
        entire_map[agent_position[1][1] + 9][agent_position[1][0]] = 0
    return entire_map, agent_position


# マップを作るメソッド
def makeMap(
    block_max: int, item_max: int
) -> tuple[npt.NDArray[npt.NDArray[int]], npt.NDArray[npt.NDArray[int]]]:
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
    small_map = layoutRandomMap(small_map, small_block, small_item)
    # 隙間マップの生成
    gap_map = np.zeros((gap_h, gap_w))
    gap_map = layoutRandomMap(gap_map, gap_block, gap_item)
    gap_map[0][7] = 3

    # マップを結合して完成させる
    entire_map = jointMap(small_map, gap_map)
    entire_map, agent_position = setAgent(entire_map)
    entire_map = entire_map.astype(int)
    return entire_map, agent_position


# マップファイル出力
def outputMap(
    file_path: str,
    file_name: str,
    entire_map: npt.NDArray[npt.NDArray[int]],
    time: int,
    agent_position: npt.NDArray[npt.NDArray[int]],
) -> None:
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(f"{file_path}{file_name}.map", "w") as f:
        f.write(f"N:generated{file_name}\n")
        f.write(f"T:{time}\n")
        f.write("S:15,17\n")
        for i in range(17):
            f.write(f"D:{entire_map[i][0]}")
            for j in range(14):
                f.write(f",{entire_map[i][j+1]}")
            f.write("\n")
        f.write(f"C:{agent_position[0][0]},{agent_position[0][1]}\n")
        f.write(f"H:{agent_position[1][0]},{agent_position[1][1]}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("generateNum", help="")
    parser.add_argument("-b", "--blockNum", help="")
    parser.add_argument("-i", "--itemNum", help="")
    args = parser.parse_args()

    try:
        generate_num = int(args.generateNum)
    except ValueError:
        print(
            "error: Expected an integer for 'generateNum', "
            "but received a different type."
        )
        print(f"generateNum type: {type(args.generateNum)}")

    try:
        block_num = int(args.blockNum) if args.blockNum else 9
    except ValueError:
        print(
            "error: Expected an integer for option '--blockNum', "
            "but received a different type."
        )
        print(f"blockNum type: {type(args.blockNum)}")

    try:
        item_num = int(args.itemNum) if args.itemNum else 10
    except ValueError:
        print(
            "error: Expected an integer for option '--itemNum', "
            "but received a different type."
        )
        print(f"itemNum type: {type(args.generateNum)}")

    for i in range(generate_num):
        entire_map, agent_position = makeMap(block_num, item_num)
        outputMap(os.path.join(os.getcwd(), "generated_map"), f"RandMap_{i}", entire_map, 120, agent_position)


if __name__ == "__main__":
    main()
