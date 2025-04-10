# MapGenerator
CHaserの対戦マップを自動で生成する機能の開発

## 使用技術
python 3.12.2  
poetry 2.1.1  

## 実行方法
このプログラムを実行するには以下のコマンドを実行してください.
```
poetry run python main.py {生成マップ数} -b {マップ中のブロックの数} -i {マップ中のアイテムの数}
```

例 :  
```
poetry run python main.py 15 -b 9 -i
```
