# MapGenerator
CHaserの対戦マップを自動で生成する機能の開発

## 使用技術
python 3.12.2  
poetry 2.1.1  

# 開発方法
コードを書いた場合, fmtとlintを適宜実行する.  
実行のためにMakefileが用意されている.  
実行例:  
```
make fmt
make lint

# fmtとlintの両方を実行する
make check
```

## 実行方法
このプログラムを実行するには以下のコマンドを実行してください.
```
poetry run python main.py {生成マップ数} -b {マップ中のブロックの数} -i {マップ中のアイテムの数}
```

例 :  
```
poetry run python main.py 15 -b 9 -i
```

