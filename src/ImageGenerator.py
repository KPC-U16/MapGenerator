import re
import os
import sys
from PIL import Image
from typing import List


#mapファイルのテキストデータを2次元配列に変換するメソッド
def _change2arr(map_data: str) -> List:
    map_list = []
    #各行を一マスごとに分割して配列に格納
    for i in range(len(map_data)):
        if map_data[i] != "" and map_data[i][0] == "D":
            map_list.append(re.split(",|\n", map_data[i].replace("D:", "")))
        elif map_data[i] != "" and map_data[i][0] == "H":
            hot = re.split(",|\n", map_data[i].replace("H:", ""))
        elif map_data[i] != "" and map_data[i][0] == "C":
            cool = re.split(",|\n", map_data[i].replace("C:", ""))

    map_list[int(cool[1])][int(cool[0])] = "C"
    map_list[int(hot[1])][int(hot[0])] = "H"

    return map_list



#一つのmapファイルをpngに変換するメソッド
def _draw_png(file_name: str) -> None:
    #mapファイルを開いてmap_dataにテキストを格納
    #print(file_name)
    file = open("../" + file_name, "r")
    map_data = file.read().split("\n")
    file.close

    map_list = _change2arr(map_data)

    #アイコン用の画像を開く
    yuka = Image.open("../../icons/yuka.png")
    kabe = Image.open("../../icons/kabe.png")
    item = Image.open("../../icons/item.png")
    hot = Image.open("../../icons/hot.png")
    cool = Image.open("../../icons/cool.png")

    icon_size = yuka.width

    #画像の下地を描く
    size = (len(map_list[0])*icon_size,len(map_list)*icon_size)
    img = Image.new("RGB", size, (255,255,255))

    #各マスのデータに応じて画像を敷き詰める
    for i in range(len(map_list)):
        for j in range(len(map_list[i])):
            if map_list[i][j] == "2":
                #壁
                img.paste(kabe, (j*icon_size, i*icon_size))
            elif map_list[i][j] == "3":
                #アイテム
                img.paste(item, (j*icon_size, i*icon_size))
            elif map_list[i][j] == "C":
                #cool
                img.paste(cool, (j*icon_size, i*icon_size))
            elif map_list[i][j] == "H":
                #hot
                img.paste(hot, (j*icon_size, i*icon_size))
            else:
                #それ以外(床)
                img.paste(yuka, (j*icon_size, i*icon_size))



    #画像を保存
    img.save(file_name.split(".")[0] + ".png")
    #img.show("test.png")

    
#全てのmapファイルをpngに変換するメソッド
def _draw_all() -> None:


    dir_name = sys.argv[1]
    file_list = os.listdir(dir_name)

    #mapファイルが入ったディレクトリに移動
    os.chdir(dir_name)

    #画像を格納するディレクトリを作成し移動
    os.mkdir("map_images")
    os.chdir("map_images")

    for i in range(len(file_list)):
        _draw_png(file_list[i])


    #もとのディレクトリに戻る
    os.chdir("../../")
    print("完了しました")

_draw_all()